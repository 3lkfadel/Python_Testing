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

@app.route('/showSummary',methods=['POST'])
def showSummary():
    email = request.form['email']
    club = next((club for club in clubs if club['email'] == email), None)

    if club is None:
        flash("Adresse e-mail non trouvée. Veuillez réessayer.")
        return redirect(url_for('index'))

    return render_template('welcome.html', club=club, competitions=competitions)



@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return redirect(url_for('showSummary'))
@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)
    placesRequired = int(request.form['places'])

    # Log pour le débogage
    print(f"Requested competition: {request.form['competition']}, Requested club: {request.form['club']}, Places required: {placesRequired}")
    print(f"Found competition: {competition}, Found club: {club}")

    if competition and club:
        available_places = int(competition['numberOfPlaces'])
        club_points = int(club['points'])  # Convertir les points en entier

        # Validation : Vérifier si les places demandées ne dépassent pas les places disponibles
        if placesRequired <= available_places:
            # Validation : Vérifier si le club a suffisamment de points
            if club_points >= placesRequired:
                competition['numberOfPlaces'] = available_places - placesRequired
                club['points'] = club_points - placesRequired  # Déduire les points
                flash('Great - booking complete!')
            else:
                flash('Not enough points available for this booking.')
        else:
            flash('Not enough places available.')
    else:
        flash('Something went wrong - please try again.')

    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))