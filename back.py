from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *
app = Flask(__name__)
# CreationBDD
engine = create_engine('sqlite:///mabase.db', echo=True)

metadata = MetaData()


cheval = Table('cheval', metadata,
               Column('idCheval', Integer, autoincrement=True, primary_key=True),
               Column('nomCheval', String),
               Column('age', Integer),
               Column('couleur', String),
               Column('race', String),
               Column('temperament', String),
               Column('sexe', String),
               Column('description', String)
               )

prestation = Table('prestation', metadata,
                   Column('idPrestation', Integer, autoincrement=True, primary_key=True),
                   Column('idCheval', Integer),
                   Column('activite', String),
                   Column('public', String),
                   Column('periode', String),
                   Column('prix', Integer)
                   )

disponibilite = Table('disponibilite', metadata,
                      Column('numLocation', Integer, autoincrement=True, primary_key=True),
                      Column('idUtilisateur', Integer),
                      Column('idPrestation', Integer),
                      Column('idCheval', Integer),
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



metadata.create_all(engine)
ch_ins = cheval.insert()


@app.route('/')
def accueil():
    url_for("static", filename="css/main.css")
    return render_template('accueil.html', title='Accueil')


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
    return render_template('achat.html', title='A vendre / A louer', message =session["name"])


# route pour formulaire
@app.route("/ajouterCheval", methods=['GET', 'POST'])
def ajouterCheval():
    connection = engine.connect()

    if request.method == 'POST':
        name = request.form['nom']
        nb = request.form['age']
        coul = request.form['couleur']
        ra = request.form['race']
        temp = request.form['temp']
        sex = request.form['sexe']
        des = request.form['des']

    # on ajoute les valeurs dans la table
    connection.execute(
        ch_ins.values(nomCheval=name, age=nb, couleur=coul, race=ra, temperament=temp, sexe=sex, description=des))

    # on lit la table
    for row in connection.execute("select * from cheval"):
        print(row)
        print('\n')
    return render_template('AvendreAlouer.html', title='A vendre / A louer')


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
