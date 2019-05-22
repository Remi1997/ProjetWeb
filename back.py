from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *
from flask_mail import Mail
from flask_mail import Message
import datetime
import paypalrestsdk
import logging
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
                   Column('activite', String, primary_key=True),
                   Column('prix', Integer)
                   )

dates = Table('dates', metadata,
                      Column('numLocation', Integer, autoincrement=True, primary_key=True),
                      Column('nomCheval', String),
                      Column('dateDebut', String),
                      Column('dateFin', String),
                      Column('prestation',String),
                      Column('prix',Integer),
                      Column('idUtilisateur',Integer),
                      Column('paye', Integer, default=0)
                      )

utilisateur = Table('utilisateur', metadata,
                    Column('idUtilisateur', Integer, autoincrement=True, primary_key=True),
                    Column('nom', String),
                    Column('prenom', String),
                    Column('mail', String),
                    Column('telephone', String),
                    Column('numLocation', VARCHAR(5)),
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
ut_ins=utilisateur.insert()
pres_ins=prestation.insert()
da_ins=dates.insert()
connection = engine.connect()



session = {'nom': '', 'mail': '', 'mdp': '', 'tel': '', 'loc': '', 'change' : '0', 'message' : ''}

cmd = []


#------------------------------------------------------------ REQUETES INSERT POUR LES TESTS ---------------------------------------------------------------
#ENREGISTREMENT TEST POUR UTILISATEUR + PROFIL ADMIN

#connection.execute(utilisateur.insert(), [
#    {"nom":"admin","prenom": "", "mail":"admin@admin.com", "telephone":722938743, "numLocation": 69100, "mdp":"TCINSA"},
#    {"nom":"Amhache","prenom": "Hind", "mail":"hind_amhache@hotmail.com", "telephone":722235643, "numLocation": 69100, "mdp":"hind"}
#])
#ENREGISTREMENT DE TEST POUR COMMANDES
#connection.execute(commandes.insert(), [{"idCheval":1,"datecommande":datetime.datetime(2018,12,13), "idUtilisateur":1, "montant":200}])

#----------------------------------------------------------------------------------REQUETES-------------------------------------------------------------------
#connection.execute(ch_ins.values(nomCheval= 'Nougat',age=15,race="Anglo arabe",description="Cheval d’école, facile et gentil. Convient parfaitement à un niveau débutant comme confirmé. Idéal pour se faire plaisir à cheval.",photo="static/img/pages/caramel.jpg",typ="Location"))
#connection.execute(ch_ins.values(nomCheval="Alaska",age=4,race="Mustang espagnol",description="Caractère calme et sûre.Excellente jument idéale débutants et enfants.",photo="static/img/pages/alaska.jpg",typ="Location / Vente"))
#connection.execute(ch_ins.values(nomCheval="Volcanic",age=12,race="Pur sang",description="C est un cheval calin et attachant.Cavalier confirmé.Il aime beaucoup les sauts d obstacle.",photo="static/img/pages/volcanic.jpg",typ="Location"))
#connection.execute(ch_ins.values(nomCheval="Ukon",age=7,race="Camargue",description="Excellent au concours de dressage. Il a beaucoup d énergie. Cavalier confirmé.",photo="static/img/pages/ukon.jpg",typ="Vente"))
#connection.execute(ch_ins.values(nomCheval="Lady",age=13,race="Trotteur français",description="Idéale pour la randonnée cette jument est énergique. Cavalier confirmé.",photo="static/img/pages/lady.jpg",typ="Location"))
#connection.execute(ch_ins.values(nomCheval="Rebelle",age=15,race="Pure race espagnol",description="Agréable jument. Idéale pour les loisirs. Habituée aux enfants.",photo="static/img/pages/rebelle.jpg",typ="Location"))
#connection.execute(ch_ins.values(nomCheval="Bambou",age=4,race="Welsh cob",description="Poney adapté au sport qui combine souplesse et sport. Idéal pour promenade en forêt.",photo="static/img/pages/bambou.jpg",typ="Location / Vente"))
#connection.execute(ch_ins.values(nomCheval="Castor",age=12,race="New Forest",description="Poney très gentil, passe partout. Idéal enfants et débutants.",photo="static/img/pages/castor.jpg",typ="Location"))
#connection.execute(ch_ins.values(nomCheval="Perle",age=2,race="Shetland",description="Très gentil, adapté aux familles.Bonnes conditions de vie exigées.",photo="static/img/pages/perle.jpg",typ="Vente"))
#connection.execute(ac_ins.values(date="Dimanche 09 septembre",titre="Stand Informations !",descr="Nous tenons à vous informer que le dimanche 09 septembre nous serons présents à la Foire de la Vigne de Charly Sur Marne. Pour l’occasion, nous tiendrons un stand d’informations pour ceux intéressés par notre centre équestre, nos cours et stages.",image="static/img/b1.jpg"))
#connection.execute(ac_ins.values(date="Samedi 08 Septembre",titre="Baptêmes Poney",descr="Nous tenons à vous informer que le samedi 08 septembre 2018 se tiendra les baptêmes des poneys. L’événement aura lieu de 14h00 à 18h00 au magasin Décathlon à Château Thierry. Nous espérons vous voir nombreux !",image="static/img/b2.jpg"))
#connection.execute(ut_ins.values(nom="bernet", prenom="agathe", mail="a@hotmail.com", telephone=722235643, numLocation=0, mdp="123"))
#connection.execute(pres_ins.values(activite = "randonnée", prix=250))
#connection.execute(pres_ins.values(activite = "mariage", prix=300))
#connection.execute(pres_ins.values(activite = "mariage + calèche", prix=400))
#connection.execute(pres_ins.values(activite = "anniversaire", prix=200))

#------------------------------------------------------------ FIN REQUETES ----------------------------------------------------------------------------------------
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
    logged = "logged" in session
    if logged:
        if session['logged']== True:
            return render_template('accueil.html', title='Accueil',liste=data, liste2=dataAct, mail=session["mail"], session=session)
    else:
        return render_template('accueil.html', title='Accueil', liste=data, liste2=dataAct, session=session)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'serviceclientcyclone@gmail.com', #remplacer par gmail de serviceclientcyclone
    "MAIL_PASSWORD":  'Tcinsa123'
}
app.config.update(mail_settings)
listemail=[]




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
    return render_template('contact.html', title='contact', session=session)


@app.route('/presentation')
def Presentation():
    return render_template('presentation.html', title='présentation', session=session)


@app.route('/activites')
def Activites():
    return render_template('activite.html', title='Activités', session=session)

@app.route('/achat')
def AvendreAlouer():
    connection = engine.connect()
    data = []
    for row in connection.execute(select([cheval.c.nomCheval, cheval.c.age,cheval.c.typ, cheval.c.race,cheval.c.description,cheval.c.photo])):
        data.append(row)
    logged = "logged" in session
    if logged:
        if session['logged']== True:
            return render_template('achat.html', title='A vendre / A louer',liste=data, mail=session["mail"], session=session)
    else:
        return render_template('achat.html', title='A vendre / A louer',liste=data, session=session)

#route calendrier
#PAGE CALENDRIER + FORMULAIRE -------------------------------------------------------------------------------------------------
@app.route("/calendrier/<nomChe>")
def calendrier(nomChe):

    info1=[]
    info2=[]
    if len(session['nom'].split())>1:
        nomm = session['nom'].split()
        name= nomm[0]
    else:
        name=session['nom']
    connection = engine.connect()
    for row in connection.execute(select([dates.c.dateDebut]).where(dates.c.nomCheval == nomChe)):
        info1.append(row[0])

    for row in connection.execute(select([dates.c.dateFin]).where(dates.c.nomCheval == nomChe)):

        info2.append(ajoute_jour(row[0]))

    
    return render_template("demos/background-events.html", liste = info1, liste2=info2, nom=nomChe, name=name)


#REQUETES POUR LES INFOS + ON REMPLIT TABLE DATES --------------------------------------------------------------------------

@app.route("/resa",methods=['GET', 'POST'])
def resa():
    info1 = []
    info2 = []
    tout = []
    b=0
    connection = engine.connect()
    if request.method == 'POST':

        nomUt = request.form['nomUtilisateur']
        name = request.form['nom']
        dated = request.form['dd']
        datef= request.form['df']
        pres = request.form['pre']

    for row in connection.execute(select([dates.c.dateDebut]).where(dates.c.nomCheval == name)):
        info1.append(row[0])

    for row in connection.execute(select([dates.c.dateFin]).where(dates.c.nomCheval == name)):
        info2.append(ajoute_jour(row[0]))

    for row in connection.execute(select([utilisateur.c.nom])):
        tout.append(row[0])

    for i in tout:

        if i == nomUt:

            b = 1
    a = verif_date(dated, datef,info1,info2)

    jours = calcul_jour(dated,datef)
#on ajoute les valeurs dans la table

    for row in connection.execute(select([utilisateur.c.idUtilisateur]).where(utilisateur.c.nom == nomUt)):
        nb = row[0]

    for row in connection.execute(select([prestation.c.prix]).where(prestation.c.activite == pres)):
        arg = row[0]*jours


#ici, on remplit la table dates
    if b == 0:
        return render_template("erreur2.html")
    if a ==1:
        connection.execute(da_ins.values(nomCheval=name,dateDebut=dated,dateFin=datef,prestation=pres, prix=arg, idUtilisateur=nb))
        return(redirect(url_for('calendrier', nomChe=name)))
    if a==0:
        return render_template("erreur.html")



@app.route("/resa2",methods=['GET', 'POST'])
def resa2():
    connection = engine.connect()
    if request.method == 'POST':
        name = request.form['nom']

    return(redirect(url_for('calendrier', nomChe=name)))

from datetime import *
#calcul de différence entre 2 jours
def calcul_jour(date1,date2):
    DATETIME_FORMAT = "%Y-%m-%d"
    from_dt =datetime.strptime(date1, DATETIME_FORMAT)
    to_dt = datetime.strptime(date2, DATETIME_FORMAT)
    timedelta = to_dt - from_dt
    diff_day = timedelta.days + float(timedelta.seconds) / 86400
    return(diff_day)

#on ajoute un jour à la date fin pour erreur dans calendrier
def ajoute_jour(jour):
    DATETIME_FORMAT = "%Y-%m-%d"
    dt =datetime.strptime(jour, DATETIME_FORMAT)
    dt = dt + timedelta(days = 1)
    date = dt.strftime(DATETIME_FORMAT)
    return(date)
def verif_date(date1,date2,liste1,liste2):
    for i in range(len(liste1)):
        if date1 == liste1[i] or date1 == liste2[i]:
            return(0)
        if date2 == liste1[i] or date2 == liste2[i]:
            return(0)
        if liste1[i][5:7] == date1[5:7]:
            if date1[8:10]<liste1[i][8:10]:
                if date2[8:10]>liste1[i][8:10]:
                    return(0)
            if date1[8:10]>liste1[i][8:10]:
                if date1[8:10]<liste2[i][8:10]:
                    return(0)
    return(1)

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
    connection = engine.connect()
    logged= "logged" in session
    #si utilisateur connecté:
    if logged:
        if session["logged"] == True:
            # chercher ses informations et les remplir dans la page
            s = text(
                'SELECT utilisateur.nom, utilisateur.prenom, utilisateur.mail, utilisateur.telephone, utilisateur.numLocation FROM utilisateur WHERE utilisateur.mail==:x and utilisateur.mdp==:y')
            resultats = connection.execute(s, x=session["mail"], y=session["mdp"])
            if resultats != None:
                for resultat in resultats:
                    session['nom']= resultat[0]+ " " +resultat[1]
                    session['mail']= resultat[2]
                    session['tel'] = resultat[3]
                    session['tel'] = resultat[3]
                    session['loc'] = resultat[4]
                    s2 = text(
                        'SELECT commandes.idcommande, cheval.nomCheval, commandes.datecommande, commandes.montant FROM utilisateur inner join commandes on utilisateur.idUtilisateur = commandes.idUtilisateur inner join cheval on cheval.idCheval = commandes.idCheval WHERE utilisateur.mail==:x')
                    resultats2=connection.execute(s2, x=session["mail"])
                    if (resultats2 != None):
                        if session['change'] == '0':
                            for resultat in resultats2:
                                cmd.append({'idcmd': resultat[0], 'nomcheval': resultat[1], 'datecmd': resultat[2],
                                            'montant': resultat[3]})  # liste de dictionnaires
                    return render_template('espaceclient.html',
                                           message=[session["nom"], session["mail"], session['tel'], session['loc']],
                                           commandes=cmd, logged=logged, texte=session['message'], session=session)
        if session['logged'] == False:
            return render_template('espaceclient.html', texte="Mauvais identifiants. Veuillez réessayer")
    else:
        return render_template('espaceclient.html', session=session)


#----------------------------------------------------------------------------------------

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
        nom = escape(request.form['nom'])
        loc = escape(request.form['ville'])
        tel= escape(request.form['tel'])
        mail = escape(request.form['mail'])
        mdp = escape(request.form['mdp'])
        prenomm= escape(request.form['prenom'])
        # VERIFICATION SI MAIL DEJA PRIS
        s = text('SELECT * FROM utilisateur WHERE utilisateur.mail==:x')
        resultats=connection.execute(s, x=mail)
        for result in resultats:
            if  result != None:
                msg = "adresse mail déjà prise!"
                return render_template("inscription.html", message = msg)
        else:
            session['logged'] = True
            session['nom'] = nom
            session['loc'] = loc
            session['mail'] = mail
            session['mdp'] = mdp
            session['mail'] = mail
            session['tel'] = tel
            connection.execute(utilisateur.insert(), [
                {'nom': session['nom'], 'prenom': prenomm, "mail": session["mail"], "telephone": session["tel"], "numLocation": session["loc"], "mdp": session["mdp"]}
            ])
            session['nom'] = prenomm + session['nom'] #on garde ce format
            return redirect("/espaceclient")



# FIN INSCRIPTION UTILISATEUR-----------------------------------------------------------------------------------------

#CHANGEMENT INFOS UTILISATEUR----------------------------------------------------------------------------------------
@app.route('/changerinfos')
def changeinfos():
    logged= "logged" in session
    session['change']='1'
    return render_template('espaceclient.html', message=[session["nom"],session["mail"], session['tel'],session['loc']], commandes= cmd, logged=logged, change=1)

@app.route('/changermdp')
def changemdp():
    logged= "logged" in session
    session['change']='2'
    return render_template('espaceclient.html', message=[session["nom"],session["mail"], session['tel'],session['loc']], commandes= cmd, logged=logged, change=2)



@app.route('/updateinfos',methods=['POST'])
def updateinfos():
    connection = engine.connect()
    if request.method=="POST":
        session['nom'] = escape(request.form['nom'])
        session['loc'] = escape(request.form['ville'])
        session['tel'] = escape(request.form['tel'])
        session["mail"] = escape(request.form['mail'])
        nomprenom = session['nom'].split()
        if len(nomprenom) > 1:
            nom= nomprenom[0]
            prenom=nomprenom[1]
        else:
            nom=  session['nom']
            prenom=''

        infos = utilisateur.update().\
                    where(utilisateur.c.mail == session['mail']).\
                    values(nom=nom, prenom=prenom, mail=session['mail'], telephone=session['tel'], numLocation=session['loc'])
        connection.execute(infos)
        return redirect('/espaceclient')


@app.route('/updatemdp',methods=['POST'])
def updatemdp():
    connection = engine.connect()
    if request.method=="POST":
        ancienmdp = request.form['ancienmdp']
        nouveaumdp = request.form['nouveaumdp']
        confnouveaumdp= request.form['confnouveaumdp']
        if session['mdp']!=ancienmdp:
            session['message'] = "Mot de passe erroné!"
        else:
            if confnouveaumdp==nouveaumdp:
                    mdpupdate = utilisateur.update().\
                    where(utilisateur.c.mail == session['mail']).\
                    values(mdp=nouveaumdp)
                    session['mdp'] = confnouveaumdp
                    connection.execute(mdpupdate)
                    session['message'] = "Mot de passe changé avec succès."
            else:
                session['message'] = "Veuillez retapez le nouveau mot de passe correctement."
        return redirect('/espaceclient')


#FIN CHANGEMENT INFOS UTILISATEUR----------------------------------------------------------------------------------------

@app.route('/panier')
def panier():
    message=[] #liste dont chaque élément représente une location
    global total
    total=0
    global iduser
    connection = engine.connect()
    logged = "logged" in session #la clé logged est elle dans session?
    if logged:
        if session["logged"] == True:
            for row in connection.execute(select([utilisateur.c.idUtilisateur]).where(utilisateur.c.mail == session['mail'])):
                iduser= row[0]
            for row in connection.execute(select([dates.c.nomCheval,dates.c.prestation,dates.c.dateDebut, dates.c.dateFin, dates.c.prix, dates.c.numLocation]).where(dates.c.idUtilisateur == iduser and dates.c.paye==0)):
                message.append(row)
                total += row[4]
            return render_template("panier.html", panierinfos=message, total=total, session=session)
    else:
        return redirect('/espaceclient')


@app.route('/supprpanier',methods=['POST'])
def supprpanier():
    connection = engine.connect()
    if request.method == "POST":
        numlocation = escape(request.form['numlocation'])
        connection.execute(dates.delete().where(dates.c.numLocation == numlocation))
        return redirect('/panier')


@app.route('/rapport')
def rapport():
    return render_template("rapport.html")


# LOGOUT DE l'UTILISATEUR-----------------------------------------------------------------------------------------
@app.route('/logout')
def logout():
    session['nom'] = ''
    session['mail'] = ''
    session['mdp'] = ''
    session['tel'] = ''
    session['loc'] = ''
    session['change'] = '0'
    session['message'] = ''
    session.pop('logged', None)
    return redirect('/')

# FIN LOGOUT DE l'UTILISATEUR-----------------------------------------------------------------------------------------

# ENVOI MAIL A l'UTILISATEUR-----------------------------------------------------------------------------------------


mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'serviceclientcyclone@gmail.com',
    "MAIL_PASSWORD":  'Tcinsa123'
}

app.config.update(mail_settings)

@app.route('/serviceclient', methods=['POST'])
def serviceclt():
    if request.method == "POST":
        nom = escape(request.form['name'])
        adrmail = escape(request.form['email'])
        sujet = escape(request.form['subject'])
        texte = escape(request.form['message'])
        mail = Mail(app)
        mail.init_app(app)
        with app.app_context():
            msg = Message(sender=adrmail,
                      recipients=["serviceclientcyclone@gmail.com"],body = "Message de: "+nom+"\n"+"adresse mail: " + adrmail+"\n"+texte, subject=sujet)
            mail.send(msg)
        session['message']="Message envoyé. Nous vous recontacterons très bientôt!"
        session['change']='3'
        return redirect('/espaceclient')


# FIN ENVOI MAIL A l'UTILISATEUR----------------------------------------------------------------------------------------

#ENVOI MAIL NEWSLETTER--------------------------------------------------------------------------------------------------

@app.route('/newsletter', methods=['POST'])
def envoiNewsletter():
    if request.method == "POST":
        adrmail = escape(request.form['email'])
        listemail.append(adrmail)
        mail = Mail(app)
        mail.init_app(app)
        with app.app_context():
            msg = Message(sender="serviceclientcyclone@gmail.com",recipients=[adrmail],body = "Suite à votre demande sur le site du centre équestre Cyclone, vous êtes bien abonné à la Newsletter. \n A bientôt !" , subject="Votre abonnement à la Newsletter Cyclone")
            mail.send(msg)
        session['message']="Votre adresse a été enregistrée, vous recevrez notre Newsletter !"
        session['change']='3'
        return redirect(request.url)


#PAYPAL -----------------------------------------------------------------------------------------------------------------
paypalrestsdk.configure({
  "mode": "live", # sandbox or live
  "client_id": "AbJHYLk4rqYPSbXCz8bNIR6YMwQq54F8Zi5jI0jPBcBsQ153vPHJEIEYtbKixyfe2PLOCrBH3cpSlaDy",
  "client_secret": "ECBkFJubkYA38QY6mE96znTCEjVQyt-_EAsqwSnDG4EjWYISLTwptl6XTa0REBplfq8wGdizQbQqhUT5"})


#PAYPAL: CREER UN PAIEMENT-----------------------------------------------------------------------------------------------

@app.route('/payment', methods=['POST'])
def paiement():
    #générer le payment.id
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:5000/execute",
            "cancel_url": "http://localhost:5000/annuler"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "item",
                    "sku": "item",
                    "price": "0.00",
                    "currency": "EUR",
                    "quantity": 1}]},
            "amount": {
                "total": total,
                "currency": "EUR"},
            "description": "Paiement pour la location d'un cheval"}]})
    if payment.create():
        print("Payment created successfully")
    else:
        print(payment.error)
    response= jsonify({"paymentID": payment.id})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

#Autoriser paiement
    for link in payment.links:
        if link.rel == "approval_url":
        # Convert to str to avoid Google App Engine Unicode issue
        # https://github.com/paypal/rest-api-sdk-python/pull/58
            approval_url = str(link.href)
            print("Redirect for approval: %s" % (approval_url))


#EXECUTER LE PAIEMENT---------------------------------------------------------------------------------------------------
@app.route ('/execute', methods=['POST'])
def execute():
    conn = engine.connect()
    success= False
    #Créer le payment id
    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({"payer_id": request.form['payerID']}):
        print("Payment executed successfully")
        success= True
        #enlever du panier et remplir la table commandes
        for row in conn.execute(select([dates.c.idCheval]).where(dates.c.idUtilisateur == iduser)): #selectionner toutes les lignes du panier
            connection.execute(commandes.insert(), [
                {"idCheval": row, "datecommande": datetime.datetime.now(), "idUtilisateur": iduser, "montant": total}]) #les insérer dans cmd
        dates.update(). \
            where(dates.c.idUtilisateur == iduser). \
            values(paye=1)
    else:
        print(payment.error)  # Error Hash
    response= jsonify({'success': success})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


#ANNULATION DU PAIEMENT-----------------------------------------------------------------------------------------

@app.route('/annuler')
def annulation():
    conn = engine.connect()
    conn.execute(
        dates.delete().where(dates.c.idUtilisateur == iduser))  # supprimer les lignes de panier de l'utilisateur
    session['message'] = "Le paiement n'a pas abouti. Nous avons annulé votre réservation."
    redirect('/espaceclient')
# FIN PAIEMENT-----------------------------------------------------------------------------------------

#LISTE DE PAIEMENTS-----------------------------------------------------------------------------------------------------
payment_history = paypalrestsdk.Payment.all({"count": 10})
payment_history.payments



if __name__ == '__main__':
    app.run(debug=True)
