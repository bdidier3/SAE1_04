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


#PAGE DE BASE
@app.route('/maraicher/layout')
def show_layout_maraicher():
    return render_template('layout.html')


#PAGE BAPTISTE (TYPE-MARCHE)
@app.route('/type-marche/show')
def show_typemarche():

    mycursor = get_db().cursor()
    sql = """SELECT typem.id_type_marche, typem.Libelle_type_marche, typem.nombre_place_type_marche, 
               typem.surface_type_marche, lieu.id_lieu, lieu.Libelle_lieu
        FROM type_marche typem
        JOIN Lieu lieu ON typem.id_lieu = lieu.id_lieu
    """
    mycursor.execute(sql)
    typemarche = mycursor.fetchall()

    return render_template('typemarche/show_typemarche.html', typemarche=typemarche)

@app.route('/type-marche/add', methods=['GET'])
def add_typemarche():

    mycursor = get_db().cursor()

    sql = "SELECT * FROM type_marche ORDER BY id_type_marche"
    mycursor.execute(sql)
    type_marche = mycursor.fetchall()
    print(type_marche)

    sql = "SELECT * FROM Lieu ORDER BY id_lieu"
    mycursor.execute(sql)
    lieux = mycursor.fetchall()
    print(lieux)

    return render_template('typemarche/add_typemarche.html', type_marche=type_marche, lieux=lieux)

@app.route('/type-marche/add', methods=['POST'])
def valid_add_typemarche():
        mycursor = get_db().cursor()

        Libelle_type_marche = request.form.get('Libelle_type_marche', '')
        id_type_marche = request.form.get('id_type_marche','')
        id_lieu = request.form.get('id_lieu', '')
        nombre_place_type_marche = request.form.get('nombre_place_type_marche', '')
        surface_type_marche = request.form.get('surface_type_marche', '')
        tuple_insert = (Libelle_type_marche, id_lieu, nombre_place_type_marche, surface_type_marche)
        sql = "INSERT INTO type_marche (Libelle_type_marche, id_lieu, nombre_place_type_marche, surface_type_marche) VALUES (%s, %s, %s, %s);"
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
        message = u'type ajouté , libellé :' + Libelle_type_marche + 'id type_marche : ' + id_type_marche + ' nombre_place_type_marche : ' + nombre_place_type_marche + ' surface_type_marche' + surface_type_marche
        flash(message, 'alert-success')
        return redirect('/type-marche/show')


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

@app.route('/type-marche/delete')
def delete_typemarche():
    print('''suppression d'un type de marché''')
    print(request.args)
    print(request.args.get('id'))
    id = request.args.get('id')
    # delete
    mycursor = get_db().cursor()
    sql = "DELETE FROM type_marche WHERE id_type_marche=%s;"
    tuple_param = (id)
    mycursor.execute(sql, tuple_param)  # Un tuple avec une virgule
    get_db().commit()
    return redirect('/type-marche/show')

@app.route('/type-marche/edit', methods=['GET'])
def edit_typemarche():
    mycursor = get_db().cursor()
    id_type_marche = request.args.get('id_type_marche', '')
    sql = """
        SELECT id_type_marche, Libelle_type_marche, nombre_place_type_marche, surface_type_marche, id_lieu 
        FROM type_marche 
        WHERE id_type_marche = %s
        """
    mycursor.execute(sql, (id_type_marche,))
    type_marche = mycursor.fetchone()
    sql_lieux = "SELECT id_lieu, Libelle_lieu FROM Lieu"
    mycursor.execute(sql_lieux)
    lieux = mycursor.fetchall()
    return render_template('typemarche/edit_typemarche.html', type_marche=type_marche, lieux=lieux)

@app.route('/type-marche/edit', methods=['POST'])
def valid_edit_typemarche():
    mycursor = get_db().cursor()
    Libelle_type_marche = request.form.get('Libelle_type_marche', '')
    id_type_marche = request.form.get('id_type_marche', '')  # Utilisez form pour récupérer la valeur depuis le formulaire
    id_lieu = request.form.get('id_lieu', '')
    nombre_place_type_marche = request.form.get('nombre_place_type_marche', '')
    surface_type_marche = request.form.get('surface_type_marche', '')
    tuple_update = (Libelle_type_marche, id_lieu, nombre_place_type_marche, surface_type_marche, id_type_marche)
    sql = "UPDATE type_marche SET Libelle_type_marche = %s, id_lieu = %s, nombre_place_type_marche = %s, surface_type_marche = %s WHERE id_type_marche = %s;"
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'type de marché modifié, id : ' + id_type_marche + "libelle : " + Libelle_type_marche + " id_lieu : " + id_lieu + "nombre de place : " + nombre_place_type_marche + "surface : " + surface_type_marche, 'alert-success')
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


@app.route('/type-marche/etat')
def show_etat():
    mycursor = get_db().cursor()

    sql_nb_place_total_tm = '''  '''
    mycursor.execute(sql_nb_place_total_tm)
    nb_place_total_tm = mycursor.fetchone()

    sql_nb_surface_total_tm = '''  '''
    mycursor.execute(sql_nb_surface_total_tm)
    nb_surface_total_tm = mycursor.fetchone()


    return render_template('etudiant/show_etat.html', nb_surface_total_tm=nb_surface_total_tm, etat=nb_place_total_tm)

@app.route('/etudiant/add', methods=['GET'])
def add_etudiant():
    print('''affichage du formulaire pour saisir un étudiant''')
    return render_template('etudiant/add_etudiant.html')

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







#PAGE MATHIS (PARTICIPATION)
@app.route('/participations/show')
def show_participations():
    mycursor = get_db().cursor()
    sql = '''
        SELECT Maraicher.nom, Maraicher.prenom, type_marche.Libelle_type_marche, participation.date_participation, participation.duree, participation.prix_place
        FROM participation
        JOIN Maraicher ON Maraicher.id_maraicher = participation.id_maraicher
        JOIN type_marche ON type_marche.id_type_marche = participation.id_type_marche
        ORDER BY participation.id_participation;
        '''
    mycursor.execute(sql)
    participation = mycursor.fetchall()
    return render_template('participation/show_participation.html', participations=participation)

@app.route('/participation/add', methods=['GET'])
def add_participation():
    print('Affichage du formulaire pour saisir une participation')
    return render_template('participation/add_participation.html')

@app.route('/participation/delete')
def delete_participation():
    print('Suppression d\'une participation')
    print(request.args)
    print(request.args.get('id_participation'))
    id_participation = request.args.get('id_participation')
    # Suppression
    mycursor = get_db().cursor()
    sql = "DELETE FROM participation WHERE id_participation=%s;"
    tuple_delete = (id_participation,)
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/participations/show')

@app.route('/participation/add', methods=['POST'])
def valid_add_participation():
    mycursor = get_db().cursor()
    id_participation = request.form.get('id_participation', '')
    id_maraicher = request.form.get('id_maraicher', '')
    id_type_marche = request.form.get('id_type_marche', '')
    date_participation = request.form.get('date_participation', '')
    duree = request.form.get('duree', '')
    prix_place = request.form.get('prix_place', '')
    tuple_insert = (id_participation, id_maraicher, id_type_marche, date_participation, duree, prix_place)
    sql = '''
            INSERT INTO participation (id_participation, id_maraicher, id_type_marche, date_participation, duree, prix_place) 
            VALUES (NULL, %s, %s, %s, %s, %s);
        '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    message = u'id_participation :' + id_participation +'id_maraicher :' + id_maraicher +'id_type_marche :' + id_type_marche +'date_participation :' + date_participation + ' - duree :' + duree + ' - prix_place :' + prix_place
    flash(message, 'alert-success')
    return redirect('/participations/show')


@app.route('/participation/edit', methods=['GET'])
def edit_participation():
    mycursor = get_db().cursor()
    id_participation = request.args.get('id_participation', '')
    sql = '''
                SELECT id_participation, id_maraicher, id_type_marche, date_participation, duree, prix_place
                FROM participation
                WHERE id_participation=%s;
            '''
    mycursor.execute(sql, (id_participation,))
    participation = mycursor.fetchone()
    sql_maraicher = "SELECT id_maraicher, nom, prenom, age, numero, mail FROM Maraicher"
    mycursor.execute(sql_maraicher)
    sql_type_marche = "SELECT id_type_marche, Libelle_type_marche, id_lieu, nombre_place_type_marche, surface_type_marche FROM type_marche"
    mycursor.execute(sql_type_marche)
    type_marche = mycursor.fetchall()
    return render_template('participation/edit_participation.html', participation=participation, type_marche=type_marche, maraicher=Maraicher)

@app.route('/participation/edit', methods=['POST'])
def valid_edit_participation():
    mycursor = get_db().cursor()
    id_participation = request.form.get('id_participation', '')
    id_maraicher = request.form.get('id_maraicher', '')
    date_participation = request.form.get('date_participation', '')
    id_type_marche = request.form.get('id_type_marche', '')
    duree = request.form.get('duree', '')
    prix_place = request.form.get('prix_place', '')
    tuple_update = (id_participation, id_maraicher, id_type_marche, date_participation, duree, prix_place)
    sql = '''
        UPDATE participation 
        SET id_maraicher=%s, id_type_marche=%s, date_participation=%s, duree=%s, prix_place=%s 
        WHERE id_participation=%s;
    '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'date_participation :' + date_participation + ' - duree :' + duree + ' - prix_place :' + prix_place, 'alert-success')
    return redirect('/participations/show')








#PAGE ANTOINE (VENTES)
@app.route('/ventes/show')
def show_ventes():
    mycursor = get_db().cursor()
    sql = ("""SELECT Maraicher.nom ,Quantitee_vendue.date_vente, type_marche.Libelle_type_marche, Produit.libelle_produit, Quantitee_vendue.quantitee
           FROM Quantitee_vendue 
           JOIN Maraicher ON Maraicher.id_maraicher = Quantitee_vendue.id_maraicher
           JOIN type_marche ON type_marche.id_type_marche = Quantitee_vendue.id_type_marche
           JOIN Produit ON Produit.id_produit = Quantitee_vendue.id_produit
           ORDER BY Quantitee_vendue.id_maraicher""")
    mycursor.execute(sql)
    ventes = mycursor.fetchall()
    return render_template('ventes/show_ventes.html', ventes=ventes )

@app.route('/ventes/delete', methods=['GET'])
def delete_ventes():
    mycursor = get_db().cursor()
    id_vente = request.form.get('id', '')
    tuple_delete = (id_vente,)
    sql = "DELETE FROM Quantitee_vendue WHERE id_vente = %s ;"
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    flash(u'une vente supprimé, id : ' + id_vente, 'alert-success')
    return redirect('/ventes/show')

@app.route('/ventes/add', methods=['GET'])
def add_vente():

    mycursor = get_db().cursor()

    sql = "SELECT * FROM Quantitee_vendue ORDER BY id_vente"
    mycursor.execute(sql)
    ventes = mycursor.fetchall()
    print(ventes)

    sql = "SELECT * FROM Maraicher ORDER BY id_maraicher"
    mycursor.execute(sql)
    maraicher = mycursor.fetchall()
    print(maraicher)

    sql = "SELECT * FROM type_marche ORDER BY id_type_marche"
    mycursor.execute(sql)
    type_marche = mycursor.fetchall()
    print(type_marche)

    sql = "SELECT * FROM Produit ORDER BY id_produit"
    mycursor.execute(sql)
    produit = mycursor.fetchall()
    print(produit)

    return render_template('ventes/add_ventes.html', ventes=ventes, maraicher=maraicher, type_marche=type_marche, produit=produit)

@app.route('/ventes/add', methods=['POST'])
def valid_add_vente():
        mycursor = get_db().cursor()

        id_maraicher = request.form.get('id_maraicher', '')
        id_vente = request.form.get('id_vente', '')
        date_vente = request.form.get('date_vente', '')
        id_type_marche = request.form.get('id_type_marche', '')
        id_produit = request.form.get('id_produit', '')
        quantitee = request.form.get('quantitee', '')
        tuple_insert = (id_maraicher, date_vente, id_type_marche, id_produit, quantitee, id_vente)
        sql = "INSERT INTO Quantitee_vendue (id_maraicher , date_vente , id_type_marche, id_produit, quantitee) VALUES ( %s, %s, %s, %s, %s);"
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
        message = u'type ajouté , id maraiche :' + id_maraicher+ 'date vente : ' + date_vente + ' id_type_marche : ' + id_type_marche + ' id_produit' + id_produit + ' quantitee: ' + quantitee
        flash(message, 'alert-success')
        return redirect('/ventes/show')

@app.route('/ventes/edit', methods=['GET'])
def edit_ventes():
    mycursor = get_db().cursor()
    id_vente = request.args.get('id_vente', '')
    sql = """
        SELECT id_vente, id_maraicher, date_vente, id_produit, id_type_marche, quantitee, recette 
        FROM Quantitee_vendue 
        WHERE id_type_marche = %s
        """
    mycursor.execute(sql, (id_vente,))
    ventes = mycursor.fetchall()
    sql_maraicher = "SELECT id_maraicher, nom FROM Maraicher"
    mycursor.execute(sql_maraicher)
    maraicher = mycursor.fetchall()
    sql_produit = "SELECT id_produit, libelle_produit FROM Produit"
    mycursor.execute(sql_produit)
    produit = mycursor.fetchall()
    sql_type_marche = "SELECT id_type_marche,Libelle_type_marche  FROM type_marche"
    mycursor.execute(sql_type_marche)
    type_marche = mycursor.fetchall()
    return render_template('ventes/edit_ventes.html', ventes=ventes, maraicher=maraicher, type_marche=type_marche, produit=produit)

@app.route('/ventes/edit', methods=['POST'])
def valid_edit_ventes():
    mycursor = get_db().cursor()
    id_vente = request.form.get('id_vente', '')  # Utilisez form pour récupérer la valeur depuis le formulaire
    id_maraicher = request.form.get('id_maraicher', '')
    date_vente = request.form.get('date_vente', '')
    id_type_marche = request.form.get('id_type_marche', '')
    id_produit = request.form.get('id_produit', '')
    quantitee = request.form.get('quantitee', '')
    tuple_update = (id_maraicher, date_vente,id_type_marche, id_produit, quantitee, id_vente)
    sql = "UPDATE type_marche SET id_maraicher = %s, date_vente = %s,id_type_marche = %s, id_produit = %s, quantitee = %s WHERE id_vente = %s;"
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'vente modifié, id : ' + id_vente + "id maraicher : " + id_maraicher + " date : " + date_vente + "id produit : " + id_produit + "quantitee : " + quantitee, 'alert-success')
    return redirect('/ventes/show')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
