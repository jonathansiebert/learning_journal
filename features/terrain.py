# -*- coding: utf-8 -*-

from contextlib import closing
import os
import lettuce
from journal import app
from journal import connect_db
from journal import get_database_connection
from journal import init_db


# used in test_app
TEST_DSN = 'dbname=test_learning_journal user=' + os.environ.get('USER')


lettuce.world.entry_data = {
    u'title': u'Hello',
    u'text': u'''#This is a post
    :::python
    with some code''',
}


@lettuce.before.all
def test_app():
    """configure our app for use in testing"""
    app.config['DATABASE'] = TEST_DSN
    app.config['TESTING'] = True
    init_db()

    with app.test_request_context('/'):
        app.test_client().post(
            '/add', data=lettuce.world.entry_data, follow_redirects=True)
        # manually commit transaction here to avoid rollback
        # due to handled Exception
        get_database_connection().commit()


@lettuce.after.all
def teardown(total):
    with app.test_request_context('/'):
        con = get_database_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM entries")
        # and here as well
        con.commit()
    with closing(connect_db()) as db:
        db.cursor().execute("DROP TABLE entries")
        db.commit()
