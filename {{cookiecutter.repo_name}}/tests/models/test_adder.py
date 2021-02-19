"""Test adder model"""

import pytest

from {{ cookiecutter.repo_name }}.models import adder

@pytest.fixture
def dummy_data():
    return {"name": "dummy_model", "value": 28.1, "zero": 0}


def test_numbers_are_added(dummy_data):
    actual = adder.add(dummy_data, number=42)["value"]
    expected = pytest.approx(70.1)

    assert actual == expected


def test_ignores_are_not_added(dummy_data):
    actual = adder.add(dummy_data, number=42, ignore_keys=["name", "zero"])["zero"]
    expected = 0

    assert actual == expected
