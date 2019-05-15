from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *


#CreationBDD
engine = create_engine('sqlite:///mabase.db', echo=True)

metadata = MetaData()

cheval = Table('cheval', metadata,
            Column('idCheval', Integer, autoincrement=True, primary_key=True),
            Column('nomCheval', String),
            Column('age',Integer),
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
            Column('idUtilisateur',Integer),
            Column('idPrestation',Integer),
            Column('idCheval',Integer),
            Column('dateDebut',Date),
            Column('dateFin',Date)
            )

utilisateur = Table('utilisateur', metadata,
            Column('idUtilisateur', Integer, autoincrement=True, primary_key=True),
            Column('nom', String),
            Column('prenom', String),
            Column('mail', String),
            Column('telephone', Integer),
            Column('numLocation', Integer)
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

app=Flask(__name__)


@app.route('/')
def Accueil():
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

@app.route('/Actualites')
def Actualites():
  return render_template('Actualites.html', title='Actualites')

@app.route('/Contact')
def Contact():
  return render_template('Contact.html', title='Contact')

@app.route('/Presentation')
def Presentation():
    return render_template('Presentation.html', title='Presentation')

@app.route('/Activites')
def Activites():
    return render_template('Activites.html', title='Activites')

@app.route('/Achat')
def AvendreAlouer():
    return render_template('AvendreAlouer.html',title='A vendre / A louer')

#route pour formulaire
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

#on ajoute les valeurs dans la table
    connection.execute(ch_ins.values(nomCheval=name,age=nb, couleur=coul,race=ra, temperament=temp,sexe=sex, description=des))

    #on lit la table
    for row in connection.execute("select * from cheval"):
        print(row)
        print('\n')
    return render_template('AvendreAlouer.html',title='A vendre / A louer')




if __name__=='__main__':
    app.run(debug=True)
