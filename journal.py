# -*- coding: utf-8 -*-

import os
import psycopg2
from contextlib import closing
from flask import Flask
from flask import g
from flask import render_template
from flask import abort
from flask import request
from flask import url_for
from flask import redirect
from flask import session
from passlib.hash import pbkdf2_sha256
from TwitterAPI import TwitterAPI
import datetime
import markdown

DB_SCHEMA = """
DROP TABLE IF EXISTS entries;
CREATE TABLE entries (
    id serial PRIMARY KEY,
    title VARCHAR (127) NOT NULL,
    text TEXT NOT NULL,
    created TIMESTAMP NOT NULL
)
"""

DB_ENTRY_INSERT = """
INSERT INTO entries (title, text, created) VALUES (%s, %s, %s)
"""

DB_ENTRIES_LIST = """
SELECT id, title, text, created FROM entries ORDER BY created DESC
"""

DB_ENTRY_UPDATE = """
UPDATE ONLY entries AS en
SET (title, text) = (%s, %s)
WHERE en.id = %s
"""

DB_GET_ENTRY = """SELECT id, title, text, created FROM entries
WHERE id = %s"""

app = Flask(__name__)

app.config['DATABASE'] = os.environ.get('DATABASE_URL',
                                        "dbname=learning_journal")


app.config['ADMIN_USERNAME'] = os.environ.get('ADMIN_USERNAME', 'admin')

app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASWWORD',
                                              pbkdf2_sha256.encrypt('admin'))

app.config['SECRET_KEY'] = os.environ.get(
    'FLASK_SECRET_KEY', 'sooperseekritvaluenooneshouldknow'
)


def connect_db():
    """Return a connection to the configured database"""
    return psycopg2.connect(app.config['DATABASE'])


def init_db():
    """Initialize the database using DB_SCHEMA

    WARNING: executing this function will drop existing tables.
    """
    with closing(connect_db()) as db:
        db.cursor().execute(DB_SCHEMA)
        db.commit()


def get_database_connection():
    db = getattr(g, 'db', None)
    if db is None or db.closed != 0:
        g.db = db = connect_db()
    return db


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        if exception and isinstance(exception, psycopg2.Error):
            # if there was a problem with the database, rollback any
            # existing transaction
            db.rollback()
        else:
            # otherwise, commit
            db.commit()
        db.close()


def write_entry(title, text):
    if not title or not text:
        raise ValueError("Title and text required for writing an entry")
    con = get_database_connection()
    cur = con.cursor()
    now = datetime.datetime.utcnow()
    cur.execute(DB_ENTRY_INSERT, [title, text, now])


def update_entry(title, text, entry_id):
    if not title or not text:
        raise ValueError("Title and text required for writing an entry")
    con = get_database_connection()
    cur = con.cursor()
    cur.execute(DB_ENTRY_UPDATE, [title, text, entry_id])


def get_entry(entry_id=1):
    con = get_database_connection()
    cur = con.cursor()
    cur.execute(DB_GET_ENTRY, entry_id)
    e = cur.fetchone()
    assert e
    return {'id': e[0], 'title': e[1].strip(),
            'text': e[2].strip(), 'created': e[3]}


def get_all_entries():
    """Return a list all entries as dicts"""
    con = get_database_connection()
    cur = con.cursor()
    cur.execute(DB_ENTRIES_LIST)
    keys = ['id', 'title', 'text', 'created']
    return [dict(zip(keys, row)) for row in cur.fetchall()]


@app.route('/')
def show_entries():
    entries = get_all_entries()
    for entry in entries:
        entry['text'] = markdown.markdown(entry['text'],
                                          extensions=['codehilite'])
    return render_template('list_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if 'logged_in' not in session or session['logged_in'] is False:
        return redirect(url_for('show_entries'))
    try:
        write_entry(request.form['title'], request.form['text'])
    except psycopg2.Error:
        abort(500)
    return redirect(url_for('show_entries'))


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_entry(id=None):
    if id is None:
        id = request.args.get('id')
    if 'logged_in' not in session or session['logged_in'] is False:
        return redirect(url_for('show_entries'))
    entry = get_entry(id)
    if request.method == 'POST':
        try:
            update_entry(request.form['title'], request.form['text'],
                         int(id))
        except psycopg2.Error:
            abort(500)
        else:
            return redirect(url_for('show_entries'))
    return render_template('edit.html', entry=entry)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            do_login(request.form['username'].encode('utf-8'),
                     request.form['password'].encode('utf-8'))
        except ValueError:
            error = "Login Failed"
        else:
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


def do_login(username='', passwd=''):
    if username != app.config['ADMIN_USERNAME']:
        raise ValueError
    if not pbkdf2_sha256.verify(passwd, app.config['ADMIN_PASSWORD']):
        raise ValueError
    session['logged_in'] = True


@app.route('/twit/<tweet_title>', methods=['POST'])
def twitter_post(tweet_title="hi"):
    con_k = u'uEmrTJlrsXcQheimdjilVRgpi'
    con_s = u'xPPpr6kvMqMIOe3cyj0hE4Et8y08AehbFsAJW2qqXR7p7KKMHA'
    acc_k = u'2545183884-MlXG41q8NF0inB1RtpqfSfpokT8fYnUuOBrVf0r'
    acc_s = u'IzPbYqQzRHm5foiA5AWHccYfWYe0FMZ2wG9lCJZGuS2Lq'
    twit = TwitterAPI(con_k, con_s, acc_k, acc_s)
    twit.request('statuses/update', {'status': str(tweet_title +
                 "-Tweeted from " + request.url_root)})
    return redirect(url_for('show_entries'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run(debug=True)
