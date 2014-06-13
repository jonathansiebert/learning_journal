# -*- coding: utf-8 -*-

from contextlib import closing
import os
from flask import session
from lettuce import *
from journal import app
from journal import connect_db
from journal import get_database_connection
from journal import init_db


# used in test_app
TEST_DSN = 'dbname=test_learning_journal user=' + os.environ.get('USER')


@before.all
def test_app():
    """configure our app for use in testing"""
    app.config['DATABASE'] = TEST_DSN
    app.config['TESTING'] = True

    # initialize the entries table and drop it when finished
    init_db()

    def cleanup():
        with closing(connect_db()) as db:
            db.cursor().execute("DROP TABLE entries")
            db.commit()

    request.addfinalizer(cleanup)


# MIGHT NEED FIXING ####################################################
@before.each_scenario
def req_context(scenario):
    """run tests within a test request context so that 'g' is present"""
    with app.test_request_context('/'):
        yield
        con = get_database_connection()
        con.rollback()


def run_independent_query(query, params=[]):
    con = get_database_connection()
    cur = con.cursor()
    cur.execute(query, params)
    return cur.fetchall()


def with_entry():
    from journal import write_entry
    expected = (u'Test Title', u'Test Text')
    with app.test_request_context('/'):
        write_entry(*expected)
        # manually commit transaction here to avoid rollback
        # due to handled Exception
        get_database_connection().commit()

    def cleanup():
        with app.test_request_context('/'):
            con = get_database_connection()
            cur = con.cursor()
            cur.execute("DELETE FROM entries")
            # and here as well
            con.commit()
    request.addfinalizer(cleanup)
    return expected


SUBMIT_BTN = '<input type="submit" value="Share" name="Share"/>'


def login_helper(username, password):
    login_data = {
        'username': username, 'password': password
    }
    client = app.test_client()
    return client.post(
        '/login', data=login_data, follow_redirects=True
    )
