#! /usr/bin/python
# -*- coding:utf-8 -*-
# mysql --user=bdidier3 --host=serveurmysql --password=mdp --database=BDD_bdidier3_tp
from flask import Flask, request, render_template, redirect, flash

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'une cle(token) : grain de sel(any random string)'

                                    ## à ajouter
from flask import session, g
import pymysql.cursors

def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(
            host="localhost",                 # à modifier
            user="bdidier3",                     # à modifier
            password="mdp",                # à modifier
            database="BDD_bdidier3_tp",        # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')

@app.route('/maraicher/layout')
def show_layout_maraicher():
    return render_template('layout.html')


@app.route('/type-marche/show')
def show_typemarche():
    mycursor = get_db().cursor()
    sql = "SELECT * FROM type_marche ORDER BY Libelle_type_marche"
    mycursor.execute(sql)
    typemarche = mycursor.fetchall()
    return render_template('typemarche/show_typemarche.html', typemarche=typemarche )

@app.route('/type-marche/add', methods=['GET'])
def add_typemarche():
    return render_template('typemarche/add_typemarche.html')

@app.route('/type-marche/add', methods=['POST'])
def valid_add_typemarche():
        mycursor = get_db().cursor()
        libelle = request.form.get('libelle', '')
        tuple_insert = (libelle,)
        sql = "INSERT INTO type_marche (Libelle_type_marche) VALUES (%s);"
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
        message = u'type ajouté , libellé :' + libelle
        flash(message, 'alert-success')
        return render_redirect('/type-marche/show')

@app.route('/type-marche/delete', methods=['GET'])
def delete_typemarche():
    mycursor = get_db().cursor()
    id_type_marche = request.form.get('id', '')
    tuple_delete = (id_type_marche,)
    sql = "DELETE FROM type_marche WHERE id_type_marche = '%s';"
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    flash(u'un type de marché supprimé, id : ' + id_type_marche, 'alert-success')
    return redirect('/type-marche/show')

@app.route('/type-marche/edit', methods=['GET'])
def edit_typemarche():
    mycursor = get_db().cursor()
    id_type_marche = request.form.get('id', '')
    sql = "SELECT id, Libelle_type_marche FROM type_marche WHERE id_type_marche = '%s'"
    mycursor.execute(sql, (id_type_marche,))
    typemarche = mycursor.fetchall()
    return render_template('typemarche/edit_typemarche.html', typemarche=typemarche)

@app.route('/type-marche/edit', methods=['POST'])
def valid_edit_typemarche():
    mycursor = get_db().cursor()
    libelle = request.form['libelle']
    id_type_marche = request.form.get('id', '')
    tuple_update = (id_type_marche, libelle)
    sql = "UPDATE type_marche SET Libelle_type_marche = '%s' WHERE id_type_marche = '%s';"
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'type de marché modifié, id : ' + id_type_marche + "libelle : " + libelle , 'alert-success')
    return redirect('/type-marche/show')


@app.route('/etudiant/show')
def show_etudiants():
    mycursor = get_db().cursor()
    sql = '''   SELECT id_etudiant AS id, nom_etudiant AS nom, groupe_etudiant AS groupe
    FROM etudiant
    ORDER BY nom DESC;      '''
    mycursor.execute(sql)

    liste_etudiants = mycursor.fetchall()
    return render_template('etudiant/show_etudiants.html', etudiants=liste_etudiants )


@app.route('/etudiant/add', methods=['GET'])
def add_etudiant():
    print('''affichage du formulaire pour saisir un étudiant''')
    return render_template('etudiant/add_etudiant.html')

@app.route('/etudiant/delete')
def delete_etudiant():
    print('''suppression d'un étudiant''')
    print(request.args)
    print(request.args.get('id'))
    id=request.args.get('id')
    #delete
    mycursor = get_db().cursor()
    sql="DELETE FROM etudiant WHERE id_etudiant=%s;"
    tuple_param=(id)
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/etudiant/show')

@app.route('/etudiant/add', methods=['POST'])
def valid_add_etudiant():
    print('''ajout de l'étudiant dans le tableau''')
    nom = request.form.get('nom')
    groupe = request.form.get('groupe')
    message = 'nom :' + nom + ' - groupe :' + groupe
    print(message)
    # insert
    mycursor = get_db().cursor()
    sql = '''INSERT INTO etudiant (id_etudiant, nom_etudiant, groupe_etudiant) 
    VALUES (NULL, %s, %s);'''
    tuple_param = (nom, groupe)
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/etudiant/show')

@app.route('/etudiant/edit', methods=['GET'])
def edit_etudiant():
    print('''affichage du formulaire pour modifier un étudiant''')
    print(request.args.get('id'))
    id=request.args.get('id')
    if id != None and id.isnumeric():
        indice = int(id)
        mycursor = get_db().cursor()
        sql = '''   SELECT id_etudiant AS id, nom_etudiant AS nom, groupe_etudiant AS groupe
           FROM etudiant
           WHERE id_etudiant=%s;      '''
        mycursor.execute(sql, (id))
        etudiant = mycursor.fetchone()
    else:
        etudiant=[]
    return render_template('etudiant/edit_etudiant.html', etudiant=etudiant)

@app.route('/etudiant/edit', methods=['POST'])
def valid_edit_etudiant():
    print('''modification de l'étudiant dans le tableau''')
    id = request.form.get('id')
    nom = request.form.get('nom')
    groupe = request.form.get('groupe')
    message = 'nom :' + nom + ' - groupe :' + groupe + ' pour l etudiant d identifiant :' + id
    print(message)
    # insert
    mycursor = get_db().cursor()
    sql = '''UPDATE etudiant SET nom_etudiant =%s, groupe_etudiant=%s WHERE id_etudiant=%s;'''
    tuple_param = (nom, groupe, id)
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/etudiant/show')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
