import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'enigma2.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.route('/')
def index():
    print "Hello World -- index"
    return render_template('index.html')

@app.route('/list')
def list():
    try:
        db = get_db()
        entries = db.execute('select * from entries').fetchall()
        return render_template('list.html', entries = entries)
    except sqlite3.Error as e:
        error = "Could not complete query: "+e.args[0]
        return render_template('list.html', error = error)

@app.route('/create')
def create():
    print "Hello World --create"
    return render_template('create.html')

@app.route('/update')
def update():
    print "Hello World --update"
    return render_template('update.html')

@app.route('/delete')
def delete():
    print "Hello World --delete"
    return render_template('delete.html')


#    try:
#        db = get_db()
#        entries = db.execute('select * from entries').fetchall()
#        return render_template('index.html', entries = entries)
#    except sqlite3.Error as e:
#        error = "No se pudo completar la consulta: "+e.args[0]
#        print error
#        return render_template('index.html', error = error)
