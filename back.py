from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *
import datetime
app = Flask(__name__)
# CreationBDD
engine = create_engine('sqlite:///mabase.db', echo=True)

metadata = MetaData()


cheval = Table('cheval', metadata,
            Column('idCheval', Integer, autoincrement=True, primary_key=True),
            Column('nomCheval', String),
            Column('age',Integer),
            Column('race', String),
            Column('description', String),
            Column('photo', String),
            Column('typ', String)
            )

prestation = Table('prestation', metadata,
                   Column('idPrestation', Integer, autoincrement=True, primary_key=True),
                   Column('nomCheval', String),
                   Column('activite', String),
                   Column('public', String),
                   Column('periode', String),
                   Column('prix', Integer)
                   )

date = Table('date', metadata,
                      Column('numLocation', Integer, autoincrement=True, primary_key=True),
                      Column('nomCheval', String),
                      Column('dateDebut', String),
                      Column('dateFin', String),
                      Column('prestation',String),
                      Column('prix',Integer),
                      Column('idUtilisateur',Integer)
                      )

utilisateur = Table('utilisateur', metadata,
                    Column('idUtilisateur', Integer, autoincrement=True, primary_key=True),
                    Column('nom', String),
                    Column('prenom', String),
                    Column('mail', String),
                    Column('telephone', Numeric),
                    Column('numLocation', Numeric),
                    Column('mdp', Integer)
                    )


commandes = Table('commandes', metadata,
                    Column('idcommande', Integer, autoincrement=True, primary_key=True),
                    Column('idCheval', Integer),
                    Column('datecommande', Date),
                    Column('idUtilisateur', Integer),
                    Column('montant', Integer)
                    )

temoignage = Table('temoignage', metadata,
            Column('idTemoignage', Integer, autoincrement=True, primary_key=True),
            Column('nom', String),
            Column('mail', String),
            Column('telephone', String),
            Column('message', String)
            )

actualite = Table('actualite', metadata,
            Column('idActualite', Integer, autoincrement=True, primary_key=True),
            Column('date', String),
            Column('titre', String),
            Column('descr', String),
            Column('image', String),
            )

metadata.create_all(engine)
ch_ins = cheval.insert()
te_ins=temoignage.insert()
ac_ins=actualite.insert()
da_ins=date.insert()

connection = engine.connect()

#------------------------------------------------------------ REQUETES INSERT POUR LES TESTS ---------------------------
#ENREGISTREMENT TEST POUR UTILISATEUR + PROFIL ADMIN

#connection.execute(utilisateur.insert(), [
#    {"nom":"admin","prenom": "", "mail":"admin@admin.com", "telephone":722938743, "numLocation": 69100, "mdp":"TCINSA"},
#    {"nom":"Amhache","prenom": "Hind", "mail":"hind_amhache@hotmail.com", "telephone":722235643, "numLocation": 69100, "mdp":"hind"}
#])
#ENREGISTREMENT DE TEST POUR COMMANDES
#connection.execute(commandes.insert(), [{"idCheval":1,"datecommande":datetime.datetime(2018,12,13), "idUtilisateur":1, "montant":200}])
#ENREGISTREMENT DE TEST POUR CHEVAL
#connection.execute(cheval.insert(), [{"nomCheval":"chevaltest","age": 10, "race":"orange", "description":"test","photo": "test","typ": "male"}])
#------------------------------------------------------------ FIN REQUETES TEST ----------------------------------------

session = {'nom': '', 'mail': '', 'mdp': '', 'tel': '', 'loc': ''}

    
#connection.execute(ch_ins.values(nomCheval= 'Nougat',age=15,race="Anglo arabe",description="Cheval d’école, facile et gentil. Convient parfaitement à un niveau débutant comme confirmé. Idéal pour se faire plaisir à cheval.",photo="static/img/pages/caramel.jpg",typ="Location"))
#connection.execute(ch_ins.values(nomCheval="Alaska",age=4,race="Mustang espagnol",description="Caractère calme et sûre.Excellente jument idéale débutants et enfants.",photo="static/img/pages/alaska.jpg",typ="Location / Vente"))
#connection.execute(ch_ins.values(nomCheval="Volcanic",age=12,race="Pur sang",description="C est un cheval calin et attachant.Cavalier confirmé.Il aime beaucoup les sauts d obstacle.",photo="static/img/pages/volcanic.jpg",typ="Location"))
#connection.execute(ch_ins.values(nomCheval="Ukon",age=7,race="Camargue",description="Excellent au concours de dressage. Il a beaucoup d énergie. Cavalier confirmé.",photo="static/img/pages/ukon.jpg",typ="Vente"))
#connection.execute(ch_ins.values(nomCheval="Lady",age=13,race="Trotteur français",description="Idéale pour la randonnée cette jument est énergique. Cavalier confirmé.",photo="static/img/pages/lady.jpg",typ="Location"))
#connection.execute(ch_ins.values(nomCheval="Rebelle",age=15,race="Pure race espagnol",description="Agréable jument. Idéale pour les loisirs. Habituée aux enfants.",photo="static/img/pages/rebelle.jpg",typ="Location"))
#connection.execute(ch_ins.values(nomCheval="Bambou",age=4,race="Welsh cob",description="Poney adapté au sport qui combine souplesse et sport. Idéal pour promenade en forêt.",photo="static/img/pages/bambou.jpg",typ="Location / Vente"))
#connection.execute(ch_ins.values(nomCheval="Castor",age=12,race="New Forest",description="Poney très gentil, passe partout. Idéal enfants et débutants.",photo="static/img/pages/castor.jpg",typ="Location"))
#connection.execute(ch_ins.values(nomCheval="Perle",age=2,race="Shetland",description="Très gentil, adapté aux familles.Bonnes conditions de vie exigées.",photo="static/img/pages/perle.jpg",typ="Vente"))

connection.execute(ac_ins.values(date="Dimanche 09 septembre",titre="Stand Informations !",descr="Nous tenons à vous informer que le dimanche 09 septembre nous serons présents à la Foire de la Vigne de Charly Sur Marne. Pour l’occasion, nous tiendrons un stand d’informations pour ceux intéressés par notre centre équestre, nos cours et stages.",image="static/img/b1.jpg"))
connection.execute(ac_ins.values(date="Samedi 08 Septembre",titre="Baptêmes Poney",descr="Nous tenons à vous informer que le samedi 08 septembre 2018 se tiendra les baptêmes des poneys. L’événement aura lieu de 14h00 à 18h00 au magasin Décathlon à Château Thierry. Nous espérons vous voir nombreux !",image="static/img/b2.jpg"))


@app.route('/')
def accueil():
    connection = engine.connect()

    data=[]
    dataAct=[]
    for j in connection.execute(select([actualite.c.date, actualite.c.titre, actualite.c.descr, actualite.c.image])):
        dataAct.append(j)
    print (dataAct)
    for i in connection.execute(select([temoignage.c.nom, temoignage.c.message])):
        data.append(i)
    print (data)
    return render_template('accueil.html', title='Accueil', liste=data, liste2=dataAct, mail=session["mail"])

@app.route("/ajoutertemoi", methods=['GET', 'POST'])
def ajoutertemoi():
    connection = engine.connect()

    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['email']
        tel = request.form['phone']
        msg = request.form['message']

    connection.execute(te_ins.values(nom=name, mail=mail, telephone=tel,message=msg))
    return redirect('/')

@app.route("/ajouterActualite")
def ajouterActualite():
    return render_template("ajouterActualite.html")


@app.route("/ajouteAct", methods=['GET', 'POST'])
def ajouteAct():
    connection = engine.connect()
    if request.method == 'POST':

        date = request.form['date']
        titre = request.form['titre']
        descr = request.form['descr']
        img = request.form['image']

#on ajoute les valeurs dans la table
    connection.execute(ac_ins.values(date=date, titre=titre, descr=descr, image=img))
    return redirect('/')


@app.route("/supprimerActualite")
def supprimerActualite():
    return render_template("supprimerActualite.html")

@app.route("/supprimeAct",methods=['GET', 'POST'])
def supprimeAct():
    conn = engine.connect()
    if request.method == 'POST':
        titre = request.form['titre']

#on supprime au nom :
    conn.execute(actualite.delete().where(actualite.c.titre == titre))
    return redirect('/')

@app.route("/modifierActualite")
def modifierActualite():
    return render_template("modifierActualite.html")

@app.route("/modifAct",methods=['GET', 'POST'])
def modifAct():
    connection = engine.connect()


    if request.method == 'POST':
        titre = request.form['titre']
        date = request.form['date']
        descr = request.form['descr']
        image = request.form['img']

#on modifie la table :

    if date != "":

        stmt = actualite.update().\
                    where(actualite.c.titre == titre).\
                    values(date=date)
        connection.execute(stmt)

    if descr != "":

        stmt = actualite.update().\
                    where(actualite.c.titre == titre).\
                    values(descr=descr)
        connection.execute(stmt)

    if image!= "":
        stmt = actualite.update().\
                    where(actualite.c.titre == titre).\
                    values(image=image)
        connection.execute(stmt)

    return redirect('/')

@app.route('/contact')
def Contact():
    return render_template('contact.html', title='contact')


@app.route('/presentation')
def Presentation():
    return render_template('presentation.html', title='présentation')


@app.route('/activites')
def Activites():
    return render_template('activite.html', title='Activités')

@app.route('/achat')
def AvendreAlouer():
    connection = engine.connect()
    data = []
    for row in connection.execute(select([cheval.c.nomCheval, cheval.c.age,cheval.c.typ, cheval.c.race,cheval.c.description,cheval.c.photo])):
        data.append(row)
    logged = "logged" in session
    if logged:
        if session['logged']== True:
            return render_template('achat.html', title='A vendre / A louer',liste=data, mail=session["mail"])
    else:
        return render_template('achat.html', title='A vendre / A louer',liste=data)

#route calendrier

@app.route("/calendrier/<nomChe>")
def calendrier(nomChe):
    
    info1=[]
    info2=[]
    connection = engine.connect()
    for row in connection.execute(select([date.c.dateDebut]).where(date.c.nomCheval == nomChe)):
        info1.append(row[0])

    for row in connection.execute(select([date.c.dateFin]).where(date.c.nomCheval == nomChe)):
        info2.append(row[0])
    
    return render_template("demos/background-events.html", liste = info1, liste2=info2)

@app.route("/resa",methods=['GET', 'POST'])
def resa():   
    connection = engine.connect()
    if request.method == 'POST':
        
        name = request.form['nom']
        dated = request.form['dd']
        datef= request.form['df']
        pres = request.form['pre']

    jours = calcul_jour(dated,datef)
#on ajoute les valeurs dans la table
    connection.execute(da_ins.values(nomCheval=name,dateDebut=dated,dateFin=datef,prestation=pres))
    return(redirect(url_for('calendrier', nomChe=name)))
    


@app.route("/resa2",methods=['GET', 'POST'])
def resa2():   
    connection = engine.connect()
    if request.method == 'POST':
        name = request.form['nom']
        
    return(redirect(url_for('calendrier', nomChe=name)))

from datetime import datetime   
def calcul_jour(date1,date2):
    DATETIME_FORMAT = "%Y-%m-%d"
    from_dt =datetime.strptime(date1, DATETIME_FORMAT)
    to_dt = datetime.strptime(date2, DATETIME_FORMAT)
    timedelta = to_dt - from_dt
    diff_day = timedelta.days + float(timedelta.seconds) / 86400
    print (diff_day)
    return(diff_day)

# route pour formulaire
@app.route("/ajouterCheval")
def ajouterCheval():
    return render_template("ajouterCheval.html")

@app.route("/supprimerCheval")
def supprimerCheval():
    return render_template("supprimerCheval.html")

@app.route("/modifierCheval")
def modifierCheval():
    return render_template("modifierCheval.html")

@app.route("/ajoute",methods=['GET', 'POST'])
def ajoute():   
    connection = engine.connect()
    if request.method == 'POST':
        
        name = request.form['nom']
        nb = request.form['age']
        ra = request.form['race']
        ty = request.form['typ']
        des = request.form['des']
        img = request.form['img']
     
#on ajoute les valeurs dans la table
    connection.execute(ch_ins.values(nomCheval=name,typ=ty,age=nb,race=ra,description=des, photo=img))
    return redirect('/achat')

@app.route("/supprime",methods=['GET', 'POST'])
def supprime():   
    conn = engine.connect()
    if request.method == 'POST':
        nom = request.form['nom']
     
#on supprime au nom :
    conn.execute(cheval.delete().where(cheval.c.nomCheval == nom))
    return redirect('/achat')

@app.route("/modif",methods=['GET', 'POST'])
def modif():
    connection = engine.connect()
    
    
    if request.method == 'POST':
        nom = request.form['nom']
        nb = request.form['age']
        ra = request.form['race']
        ty = request.form['typ']
        des = request.form['des']
        img= request.form['img']
     
#on modifie la table :
        
    if nb != "":
        stmt = cheval.update().\
                    where(cheval.c.nomCheval == nom).\
                    values(age=nb)
        connection.execute(stmt)
        
       
    if ra != "":
        
        stmt = cheval.update().\
                    where(cheval.c.nomCheval == nom).\
                    values(race=ra)
        connection.execute(stmt)
        
    if des != "":

        stmt = cheval.update().\
                    where(cheval.c.nomCheval == nom).\
                    values(description=des)
        connection.execute(stmt)
        
    if ty!= "":
        stmt = cheval.update().\
                    where(cheval.c.nomCheval == nom).\
                    values(typ=ty)
        connection.execute(stmt)
        
    if img != "":
        sstmt = cheval.update().\
                    where(cheval.c.nomCheval == nom).\
                    values(photo=img)
        connection.execute(stmt)
    
    return redirect('/achat')     

#fd74a08fcc14617a4e5614b5effc49cdf8ee94f8

# LOGGING DE l'UTILISATEUR-----------------------------------------------------------------------------------------
app.secret_key = 'iswuygdedgv{&75619892__01;;>..zzqwQIHQIWS'
@app.route('/espaceclient')
def index():
    cmd = {'idcmd': '', 'nomcheval': '', 'datecmd': '', 'montant': ''}
    connection = engine.connect()
    logged= "logged" in session
    #si utilisateur connecté:
    if logged:
        if session["logged"] == True:
            # chercher ses informations et les remplir dans la page
            s = text(
                'SELECT utilisateur.telephone, utilisateur.numLocation FROM utilisateur WHERE utilisateur.mail==:x and utilisateur.mdp==:y')
            resultats = connection.execute(s, x=session["mail"], y=session["mdp"])
            if resultats != None:
                for resultat in resultats:
                    session['tel'] = resultat[0]
                    session['loc'] = resultat[1]
            s2= text ('SELECT commandes.idcommande, cheval.nomCheval, commandes.datecommande, commandes.montant FROM utilisateur inner join commandes on utilisateur.idUtilisateur = commandes.idUtilisateur inner join cheval on cheval.idCheval = commandes.idCheval WHERE utilisateur.mail==:x')
            resultats2 = connection.execute(s2,x= session["mail"])
            if resultats2 != None:
                for resultat in resultats2:
                    cmd= {'idcmd': resultat[0], 'nomcheval' : resultat[1], 'datecmd' : resultat[2], 'montant' : resultat[3]}
            return render_template('espaceclient.html', message=[session["nom"],session["mail"], session['tel'],session['loc'], cmd['idcmd'], cmd['nomcheval'], cmd['datecmd'],cmd['montant']], logged=logged)
        if session['logged'] == False:
            txt = "Mauvais identifiants. Veuillez réessayer"
            return render_template('espaceclient.html', mauvaisid=txt)
    else:
        return render_template('espaceclient.html')

@app.route('/login', methods=['POST'])
def login():
    connection = engine.connect()
    if request.method == 'POST':
        session["mail"]= escape(request.form['mail'])
        session["mdp"] = escape(request.form['mdp'])
    #On cherche la correspondance entre la bdd et les données saisies par l'utilisateur
        s = text('SELECT utilisateur.nom, utilisateur.prenom FROM utilisateur WHERE utilisateur.mail==:x and utilisateur.mdp==:y')
        resultats = connection.execute(s, x=session["mail"], y=session["mdp"])
        if resultats != None:
            for resultat in resultats:
                result = str(resultat[0]+ " " + resultat[1]) #on n'a qu'un seul résultat #tableau de 2 valeurs
                session["logged"] = True
                session["nom"] = result
        else: # si mauvais id:
            session["logged"] = False

        return redirect("/espaceclient")

# FIN LOGGING DE l'UTILISATEUR-----------------------------------------------------------------------------------------

# INSCRIPTION DE l'UTILISATEUR-----------------------------------------------------------------------------------------

@app.route('/inscription')
def inscription():
    return render_template("inscription.html")

@app.route('/enregistrement', methods=['POST'])
def entregistrement():
    connection = engine.connect()
    if request.method == 'POST':
        session['nom'] = escape(request.form['nom'])
        session['prenom']= escape(request.form['prenom'])
        session['loc'] = escape(request.form['ville'])
        session['tel'] = escape(request.form['tel'])
        session["mail"] = escape(request.form['mail'])
        session["mdp"] = escape(request.form['mdp'])
        # VERIFICATION SI MAIL DEJA PRIS
        s = text('SELECT utilisateur.mail FROM utilisateur WHERE utilisateur.mail==:x')
        resultats = connection.execute(s, x=session["mail"])
        if resultats == session["mail"]:
            msg = "adresse mail déjà prise!"
            return render_template("inscription.html", message = msg)
        else:
            session['logged'] = True
            connection.execute(utilisateur.insert(), [
                {'nom': session['nom'], 'prenom': session['prenom'], "mail": session["mail"], "telephone": session["tel"], "numLocation": session["loc"], "mdp": session["mdp"]}
            ])
            return redirect("/espaceclient")


# FIN INSCRIPTION UTILISATEUR-----------------------------------------------------------------------------------------




# DEBUT PAIEMENT-----------------------------------------------------------------------------------------


@app.route('/annuler')
def annulation():
    render_template('annuler.html')


@app.route('/succes')
def succes():
    render_template('succes.html')


# FIN PAIEMENT-----------------------------------------------------------------------------------------



# LOGOUT DE l'UTILISATEUR-----------------------------------------------------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# FIN LOGOUT DE l'UTILISATEUR-----------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
