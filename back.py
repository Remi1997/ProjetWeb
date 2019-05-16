from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *

app = Flask(__name__)
# CreationBDD
engine = create_engine('sqlite:///mabase.db', echo=True)

metadata = MetaData()


cheval = Table('cheval', metadata,
            Column('nomCheval', String,primary_key=True),
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

disponibilite = Table('disponibilite', metadata,
                      Column('numLocation', Integer, autoincrement=True, primary_key=True),
                      Column('idUtilisateur', Integer),
                      Column('idPrestation', Integer),
                      Column('nomCheval', String),
                      Column('dateDebut', Date),
                      Column('dateFin', Date)
                      )

utilisateur = Table('utilisateur', metadata,
                    Column('idUtilisateur', Integer, autoincrement=True, primary_key=True),
                    Column('nom', String),
                    Column('prenom', String),
                    Column('mail', String),
                    Column('telephone', Integer),
                    Column('numLocation', Integer),
                    Column('mdp', Integer),
                    Column('moyenpaiement', String)
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


metadata.create_all(engine)
ch_ins = cheval.insert()
te_ins=temoignage.insert()

connection = engine.connect()
    
#connection.execute(ch_ins.values(nomCheval= 'Nougat',age=15,race="Anglo arabe",description="Cheval d’école, facile et gentil. Convient parfaitement à un niveau débutant comme confirmé. Idéal pour se faire plaisir à cheval.",photo="static/img/pages/caramel.jpg",typ="Location"))
#connection.execute(ch_ins.values(nomCheval="Alaska",age=4,race="Mustang espagnol",description="Caractère calme et sûre.Excellente jument idéale débutants et enfants.",photo="static/img/pages/alaska.jpg",typ="Location / Vente"))
#connection.execute(ch_ins.values(nomCheval="Volcanic",age=12,race="Pur sang",description="C est un cheval calin et attachant.Cavalier confirmé.Il aime beaucoup les sauts d obstacle.",photo="static/img/pages/volcanic.jpg",typ="Location"))
#connection.execute(ch_ins.values(nomCheval="Ukon",age=7,race="Camargue",description="Excellent au concours de dressage. Il a beaucoup d énergie. Cavalier confirmé.",photo="static/img/pages/ukon.jpg",typ="Vente"))
#connection.execute(ch_ins.values(nomCheval="Lady",age=13,race="Trotteur français",description="Idéale pour la randonnée cette jument est énergique. Cavalier confirmé.",photo="static/img/pages/lady.jpg",typ="Location"))
#connection.execute(ch_ins.values(nomCheval="Rebelle",age=15,race="Pure race espagnol",description="Agréable jument. Idéale pour les loisirs. Habituée aux enfants.",photo="static/img/pages/rebelle.jpg",typ="Location"))
#connection.execute(ch_ins.values(nomCheval="Bambou",age=4,race="Welsh cob",description="Poney adapté au sport qui combine souplesse et sport. Idéal pour promenade en forêt.",photo="static/img/pages/bambou.jpg",typ="Location / Vente"))
#connection.execute(ch_ins.values(nomCheval="Castor",age=12,race="New Forest",description="Poney très gentil, passe partout. Idéal enfants et débutants.",photo="static/img/pages/castor.jpg",typ="Location"))
#connection.execute(ch_ins.values(nomCheval="Perle",age=2,race="Shetland",description="Très gentil, adapté aux familles.Bonnes conditions de vie exigées.",photo="static/img/pages/perle.jpg",typ="Vente"))



@app.route('/')
def accueil():
    connection = engine.connect()

    data=[]
    for i in connection.execute(select([temoignage.c.nom, temoignage.c.message])):
        data.append(i)
    print (data)
    return render_template('accueil.html', title='Accueil', liste=data)

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


@app.route('/actualites')
def Actualités():
    return render_template('actualites.html', title='actualités',message =session["name"])


@app.route('/contact')
def Contact():
    return render_template('contact.html', title='contact')


@app.route('/presentation')
def Presentation():
    return render_template('presentation.html', title='présentation')


@app.route('/activites')
def Activites():
    return render_template('Activites.html', title='Activités')

@app.route('/achat')
def AvendreAlouer():
    connection = engine.connect()
    data = []
    for row in connection.execute(select([cheval.c.nomCheval, cheval.c.age,cheval.c.typ, cheval.c.race,cheval.c.description,cheval.c.photo])):
        data.append(row)
    return render_template('achat.html', title='A vendre / A louer',liste=data) #message =session["name"]


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


    #Logging
app.secret_key = 'iswuygdedgv{&75619892__01;;>..zzqwQIHQIWS'

@app.route('/espaceclient')
def index():
    connection = engine.connect()
    logged= "logged" in session
    #si utilisateur connecté:
    if logged:
        if session["logged"] == True:
            cmd={'idcmd':'','nomcheval':'','datecmd':'','montant':''}
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
            return render_template('espaceclient.html', message=[session["name"],session["mail"], session['tel'],session['loc'], cmd['idcmd'], cmd['nomcheval'], cmd['datecmd'],cmd['montant']], logged=logged)
        if session['logged'] == False:
            txt = "Mauvais identifiants. Veuillez réessayer"
            return render_template('espaceclient.html', message=txt)
    else:
        return render_template('espaceclient.html')

    #else:
    #return render_template('accueil.html')
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
                session["name"] = result
        else: # si mauvais id:
            session['logged'] = False

        return redirect("/espaceclient")

# SESSION = ["name"=..., "logged"=...]


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
