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

@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    elif request.method == 'POST':
        try:
            db = get_db()
            # vals = [request.form['originNode'], request.form['destinationNode'],request.form['pwId'],request.form['localInterface'],request.form['remoteInterface'],request.form['vlan'],request.form['vplsId']
            db.execute('insert into entries (originNode, destinationNode, pwID, localInterface, remoteInterface, vlanID, vplsID, customerName) values (?,?,?,?,?,?,?,?)',[request.form['originNode'], request.form['destinationNode'],request.form['pwID'],request.form['localInterface'],request.form['remoteInterface'],request.form['vlanID'],request.form['vplsID'],request.form['customerName']])
            db.commit()
            if  request.form['vplsID'] == '':
                print 'Crear Servicio como PW'
                # createPw(vals)
            else:
                print 'Crear Servicio como VPLS'
                # createVpls(vals)

            flash('Created successfully')
            return redirect(url_for('list'))
        except sqlite3.Error as e:
            error = "Could not create the service: "+e.args[0]
            return render_template('create.html', error = error)

@app.route('/update')
def update():
    print "Hello World --update"
    return render_template('update.html')

@app.route('/delete', methods=['GET','POST'])
def delete():
    if request.method == 'GET':
        return render_template('delete.html')
    elif request.method == 'POST':
        try:
            db = get_db()
            db.execute('delete from entries where '+ request.form['filter'])
            db.commit()
            flash('Deleted successfully')
            return redirect(url_for('list'))
        except sqlite3.Error as e:
            error = "Could not delete service: "+e.args[0]
            return render_template('delete.html', error = error)


@app.route('/applyFilter', methods=['POST'])
def applyFilter():
    try:
        db = get_db()
        entries = db.execute('select * from entries where '+ request.form['filter']).fetchall()
        return render_template('list.html', entries = entries)
    except sqlite3.Error as e:
        error = "Could not complete query: "+e.args[0]
        return render_template('list.html', error = error)





#    try:
#        db = get_db()
#        entries = db.execute('select * from entries').fetchall()
#        return render_template('index.html', entries = entries)
#    except sqlite3.Error as e:
#        error = "No se pudo completar la consulta: "+e.args[0]
#        print error
#        return render_template('index.html', error = error)
