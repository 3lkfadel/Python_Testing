import json
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

 #ici j'ai fais en sorte que si le mails n'est pas dans liste et que l'utisateur  
@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form['email']
    club = next((club for club in clubs if club['email'] == email), None)

    if club is None:
        flash("Adresse e-mail non trouvée. Veuillez réessayer.")
        return redirect(url_for('index'))

    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)

# Global list to store reservations
reservations = []

@app.route('/purchasePlaces', methods=['POST'])
@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)
    placesRequired = int(request.form['places'])

    # Vérification du nombre de places disponibles
    if placesRequired > int(competition['numberOfPlaces']):
        flash("Pas assez de places disponibles.")
        return redirect(url_for('book', competition=competition['name'], club=club['name']))

    # Vérification des points disponibles
    if placesRequired > club['points']:
        flash("Vous n'avez pas assez de points pour réserver ce nombre de places.")
        return redirect(url_for('book', competition=competition['name'], club=club['name']))

    # Réduire le nombre de places disponibles et les points du club
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] -= placesRequired  # Diminuer les points en fonction des places réservées

    # Ajouter la réservation à la liste des réservations
    reservations.append({
        'club': club['name'],
        'competition': competition['name'],
        'places': placesRequired
    })

    flash('Réservation effectuée avec succès !')
    return render_template('welcome.html', club=club, competitions=competitions, reservations=reservations)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))