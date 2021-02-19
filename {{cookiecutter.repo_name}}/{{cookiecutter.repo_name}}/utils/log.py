"""Set up logging for {{ cookiecutter.project_name }}

Logging is based on the Loguru library: https://github.com/Delgan/loguru/
"""

# Standard library imports
import functools
import logging
import sys
from typing import Union

# Third party imports
from loguru import logger
from loguru._logger import Level
from pyconfs import Configuration

# {{ cookiecutter.project_name }} imports
from {{ cookiecutter.repo_name }} import config

# Configuration of logs
CFG = config.{{ cookiecutter.repo_name }}.log


def init(level: Union[str, int] = CFG.console.level.upper()) -> None:
    """Initialize a logger based on configuration settings and options"""
    # Remove the default logger
    logger.remove()

    # Wrap standard library logging calls with loguru
    if CFG.console.include_3rd_party:
        _wrap_stdlib_logging(level)

    # Set log level
    logger.add(
        sys.stdout,
        level=level,
        format=CFG.console.format,
        serialize=CFG.console.json_logs,
    )


def show_log_levels():
    """Log to each level for a simple visual test"""

    # Add a new logger that logs all levels
    init(level="TRACE")

    # Log to each level
    for name, level in sorted(logger._core.levels.items(), key=lambda lvl: lvl[1].no):
        log_func = getattr(logger, name.lower())
        log_func(f"Use logger.{name.lower()}() to write to {name} ({level.no})")


def _add_levels(additional_levels: Configuration) -> None:
    """Add custom log levels"""
    for level_cfg in additional_levels.sections:
        # Validate configuration
        level = level_cfg.as_named_tuple(Level)

        # Add level and corresponding method to logger
        logger.level(**level_cfg)
        setattr(
            logger.__class__,
            level.name.lower(),
            functools.partial(logger.log, level.name),
        )

    def blank(self):
        """Write a blank line to the logger"""
        for handler in self._core.handlers.values():
            handler._sink.write("\n")

    setattr(logger.__class__, "blank", functools.partial(blank, logger))


def _wrap_stdlib_logging(level: str):
    """Wrap log messages using logging in the standard library with loguru logger

    Based on https://github.com/Delgan/loguru#entirely-compatible-with-standard-logging
    """

    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    # Set up InterceptHandler to handle logs written using logging
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(logger.level(level).no)

    # Remove other log handlers and propagate to root handler
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True


# Add custom levels at import
_add_levels(CFG.custom_levels)
