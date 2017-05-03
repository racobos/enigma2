@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    elif request.method == 'POST':
        try:
            db = get_db()
            vals = [request.form['originNode'], request.form['destinationNode'],request.form['pwId'],request.form['localInterface'],request.form['remoteInterface'],request.form['vlan'],request.form['vplsId']
            db.execute('insert into services (nodoOrigen, nodoDestino, pwId, localInterface, remoteInterface, vlan, vplsId) values (?,?,?,?,?,?,?)',vals])
            db.commit()

            if  request.form['vplsId'] == '':
                print 'Crear Servicio como PW'
                createPw(vals)
            else:
                print 'Crear Servicio como VPLS'
                createVpls(vals)


            flash('Created successfully')
            return redirect(url_for('list'))
        except sqlite3.Error as e:
            error = "Could not create the service: "+e.args[0]
            return render_template('create.html', error = error)
