# -*- coding: utf-8 -*-
from contextlib import closing
import pytest
import os

from journal import app
from journal import connect_db
from journal import get_database_connection
from journal import init_db


TEST_DSN = 'dbname=test_learning_journal user=' + os.environ.get('USER')


def clear_db():
    with closing(connect_db()) as db:
        db.cursor().execute("DROP TABLE entries")
        db.commit()

pytest.fixture(scope='session')
def test_app():
    """configure our app for use in testing"""
    app.config['DATABASE'] = TEST_DSN
    app.config['TESTING'] = True

@pytest.fixture(scope='session')
def db(test_app, request):
    """initialize the entries table and drop it when finished"""
    init_db()

    def cleanup():
        clear_db()

    request.addfinalizer(cleanup)