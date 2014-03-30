__author__ = 'Yelite'

import pytest

from db import Session
from _db import Session as _Session


@pytest.fixture(scope='session')
def session():
    return Session()


@pytest.fixture(scope='session')
def test_session():
    return _Session()
