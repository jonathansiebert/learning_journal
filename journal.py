# -*- coding: utf-8 -*-

import os
import psycopg2
from contextlib import closing
from flask import Flask

DB_SCHEMA = """
DROP TABLE IF EXISTS entries;
CREATE TABLE entries (
    id serial PRIMARY KEY,
    title VARCHAR (127) NOT NULL,
    text TEXT NOT NULL,
    created TIMESTAMP NOT NULL
)
"""

app = Flask(__name__)

app.config['DATABASE'] = os.environ.get(
    'DATABASE_URL',
    'dbname=learning_journal user=' + os.getenv('DATABASE_USER')
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

@app.route('/')
def hello():
    return u'Hello world!'

if __name__ == '__main__':
    app.run(debug=True)