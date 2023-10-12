from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL
from random import randint

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'proj'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/produits/<req>/', methods=['GET', 'POST'])
def produits(req):
    cur = mysql.connection.cursor()
    cur.execute('SELECT label, Id_Produit, PU, Restants, Id_Produit FROM produits')
    data = cur.fetchall()
    return render_template('list.html', pagename="produits", type="p", data=data, req=req)

@app.route('/commandes/<req>/', methods=['GET', 'POST'])
def commandes(req):
    cur = mysql.connection.cursor()
    if req == 'list':
        cur.execute('SELECT l.Id_Commande, p.Label, p.PU, l.Quantite, l.Statut FROM ligne_commande l '
                'JOIN produits p ON l.Id_Produit = p.Id_Produit ')
    elif req == 'select':
        cur.execute('SELECT l.Id_Commande, p.Label, p.PU, l.Quantite, l.Statut FROM ligne_commande l '
                    'JOIN produits p ON l.Id_Produit = p.Id_Produit '
                    'LEFT JOIN comm_fact lf ON lf.Id_Commande = l.Id_Commande '
                    'WHERE lf.Id_Commande IS NULL')
    data = cur.fetchall()
    if request.method == 'POST':
        fact_id = 'F' + str(randint(1000000,9999999)) # 8 characters
        commlist = request.form.getlist('commandes')
        mht = 0
        tva = 0
        prodlist = ''
        for comm in commlist:
            cur.execute("SELECT p.label FROM produits p JOIN ligne_commande l on p.Id_Produit = l.Id_Produit WHERE l.Id_Commande = '%s'" % comm)
            labelq = cur.fetchone()
            cur.execute("SELECT p.PU FROM produits p JOIN ligne_commande l on p.Id_Produit = l.Id_Produit WHERE l.Id_Commande = '%s'" % comm)
            puq = cur.fetchone()
            cur.execute("SELECT Quantite FROM ligne_commande WHERE Id_Commande = '%s'" % comm)
            qteq = cur.fetchone()
            for label in labelq:
                for pu in puq:
                    for qte in qteq:
                        mht = mht + pu*qte
                        prodlist = prodlist + ("%sx %s <br> " % (str(qte), label))
        prodlist = prodlist[:-5]
        ttc = mht*1.3
        cur.execute("INSERT INTO facture (Id_Facture, Produits, HT, TTC, Statut) VALUES ('%s', '%s', '%s', '%s', 0)" % (fact_id, prodlist, mht, ttc))
        mysql.connection.commit()
        for comm in commlist:
            cur.execute("INSERT INTO comm_fact VALUES ('%s', '%s')" % (comm, fact_id))
            mysql.connection.commit()
            cur.execute("UPDATE ligne_commande SET Statut = '1' WHERE Id_Commande = '%s'" % comm)
            mysql.connection.commit()
        return redirect(url_for('factures'))
    else:
        return render_template('list.html', pagename="lignes de commande", type="l", data=data, req=req)

@app.route('/factures', methods=['GET', 'POST'])
def factures():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Facture')
    data = cur.fetchall()
    """
    cur.execute("SELECT p.Label, p.PU, l.Quantite FROM ligne_commande l "
                "INNER JOIN comm_fact lf ON l.Id_Commande = lf.Id_Commande "
                "INNER JOIN produits p ON l.Id_Produit = p.Id_Produit "
                "WHERE lf.Id_Facture = '%s'" % id)
    datapop = cur.fetchall()
    cur.execute("SELECT TTC FROM facture WHERE Id_Facture = '%s'" % id)
    ttc = cur.fetchone()
    """
    return render_template('list.html', pagename="factures", type="f", data=data)

@app.route('/delete/<type>/<id>', methods=['GET', 'POST'])
def delete(type, id):
    cur = mysql.connection.cursor()
    if type=="p":
        redir='produits'
        db="produits"
        id_db="Id_Produit"
    elif type=="l":
        redir = 'commandes'
        db="ligne_commande"
        id_db = "Id_Commande"
        cur.execute("DELETE f FROM facture f INNER JOIN comm_fact lf ON f.Id_Facture = lf.Id_Facture "
                    "INNER JOIN ligne_commande l ON lf.Id_Commande = l.Id_Commande "
                    "WHERE l.Id_Commande = '%s'" % id)
    cur.execute("DELETE FROM " + db + " WHERE " + id_db + " = '" + id + "'")
    mysql.connection.commit()
    return redirect(url_for(redir, req='list'))

@app.route('/delete/fact/<id>/<stat>', methods=['GET', 'POST'])
def delfact(id, stat):
    cur = mysql.connection.cursor()
    if stat=='1':
        cur.execute(
            "DELETE l FROM ligne_commande l INNER JOIN comm_fact lf ON l.Id_Commande = lf.Id_Commande WHERE lf.Id_Facture = '" + id + "'")
        mysql.connection.commit()
    elif stat=='0':
        cur.execute(
            "UPDATE ligne_commande l INNER JOIN comm_fact lf ON l.Id_Commande = lf.Id_Commande SET Statut='0' WHERE lf.Id_Facture = '" + id + "'")
        mysql.connection.commit()
    cur.execute("DELETE FROM facture WHERE Id_Facture = '" + id + "'")
    mysql.connection.commit()
    return redirect(url_for('factures'))

@app.route('/add/<type>/<id>', methods=['GET', 'POST'])
def add(type, id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        if type=="p":
            prod_id = 'P' + str(randint(1000000, 9999999))
            inputf = request.form
            label = inputf['label']
            pu = inputf['pu']
            qte = inputf['qte']
            cur.execute('INSERT INTO produits VALUES (%s, %s, %s, %s)',
                        (prod_id, label, pu, qte))
            mysql.connection.commit()
            return redirect(url_for('produits', req='list'))
        elif type=="l":
            ligne_id = 'L' + str(randint(1000000, 9999999))
            inputf = request.form
            qte = inputf['qte']
            cur.execute("SELECT Restants FROM produits WHERE Id_Produit = '%s'" % id)
            rest = cur.fetchone()
            for restval in rest:
                if int(qte) > restval:
                    return ('Erreur: quantité insérée (%s) surpasse la quantité restante de produits (%s)'
                            % (qte, restval))
                else:
                    cur.execute("INSERT INTO ligne_commande VALUES ('%s', '%s', %s, 0)" % (ligne_id, id, qte))
                    mysql.connection.commit()
                    cur.execute("UPDATE produits SET Restants = %i "
                                "WHERE Id_Produit = '%s'" % (restval - int(qte), id))
                    mysql.connection.commit()
                    return redirect(url_for('commandes', req='list'))
    elif type=='f':
        cur = mysql.connection.cursor()
        cur.execute("")
        return redirect(url_for('factures'))
    elif type=='l':
        cur = mysql.connection.cursor()
        cur.execute("SELECT Restants FROM produits WHERE Id_Produit = '%s'" % id)
        rest = cur.fetchone()
        for restval in rest:
            return render_template('input.html', type=type, req='add', rest=restval)
    else:
        return render_template('input.html', type=type, req='add')

@app.route('/input/<type>/<id>/', methods=['GET', 'POST'])
def edit(type, id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        input = request.form
        if type == "p":
            redir = 'produits'
            label = input['label']
            pu = input['pu']
            qte = input['qte']
            cur.execute("UPDATE produits SET label= '%s', pu= '%s', restants= '%s' WHERE Id_Produit='%s'" %
                        (label, pu, qte, id))
            mysql.connection.commit()
            return redirect(url_for('produits', req='list'))
        elif type == "l":
            qtein = int(input['qte'])
            print(qtein)
            if input['stat'] == "traite":
                stat = 1
            else:
                stat = 0
            cur.execute("SELECT Quantite FROM ligne_commande "
                        "WHERE Id_Commande = '%s'" % id)
            qtecom = cur.fetchone()
            cur.execute("SELECT p.Id_Produit FROM produits p JOIN ligne_commande l ON l.Id_Produit = p.Id_Produit "
                        "WHERE l.Id_Commande = '%s'" % id)
            pid = cur.fetchone()
            cur.execute("SELECT p.Restants FROM produits p JOIN ligne_commande l ON l.Id_Produit = p.Id_Produit "
                        "WHERE l.Id_Commande = '%s'" % id)
            restprod = cur.fetchone()
            cur.execute("UPDATE ligne_commande SET Quantite = '%s', Statut = '%s' "
                        "WHERE Id_Commande = '%s'" % (qtein, stat, id))
            mysql.connection.commit()
            for qtecomval in qtecom:
                for pidval in pid:
                    for restprodval in restprod:
                        qtediff = qtein - qtecomval
                        cur.execute("UPDATE produits SET Restants = %i "
                                    "WHERE Id_Produit = '%s'" % ((restprodval-qtediff), pidval))
                        mysql.connection.commit()
            return redirect(url_for('commandes', req='list'))
    elif type == 'f':
        cur = mysql.connection.cursor()
        cur.execute("UPDATE facture SET Statut = 1 "
                    "WHERE Id_Facture = '%s'" % id)
        mysql.connection.commit()
        return redirect(url_for('factures'))
    else:
        if type == 'p':
            cur = mysql.connection.cursor()
            cur.execute("SELECT label, PU, Restants FROM produits WHERE Id_Produit= '%s'" % id)
            data = cur.fetchall()
            return render_template('input.html', type=type, req='edit', data=data)
        elif type == 'l':
            cur = mysql.connection.cursor()
            cur.execute("SELECT Quantite, Statut FROM ligne_commande WHERE Id_Commande = '%s'" % id)
            data = cur.fetchall()
            cur.execute("SELECT p.Restants FROM produits p JOIN ligne_commande l ON l.Id_Produit = p.Id_Produit "
                        "WHERE l.Id_Commande = '%s'" % id)
            rest = cur.fetchone()
            for restval in rest:
                return render_template('input.html', type=type, req='edit', data=data, rest=restval)

@app.route('/factdoc/<id>', methods=['GET', 'POST'])
def factdoc(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT p.Label, p.PU, l.Quantite FROM ligne_commande l "
                "INNER JOIN comm_fact lf ON l.Id_Commande = lf.Id_Commande "
                "INNER JOIN produits p ON l.Id_Produit = p.Id_Produit "
                "WHERE lf.Id_Facture = '%s'" % id)
    data = cur.fetchall()
    cur.execute("SELECT TTC FROM facture WHERE Id_Facture = '%s'" % id)
    ttc = cur.fetchone()
    return render_template('facture.html', id=id, data=data, ttc=ttc)


if __name__ == '__main__':
    app.run(debug=True)
