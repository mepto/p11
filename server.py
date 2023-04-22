import json
from flask import flash, Flask, redirect, render_template, request, url_for

from constants import BOOKING_OK, EMAIL_ERROR, GENERIC_ERROR, NOT_ENOUGH_POINTS


def load_clubs():
    """Return list of clubs based on clubs file."""
    with open('clubs.json') as c:
        return json.load(c)['clubs']


def load_competitions():
    """Return list of competitions based on competitions file."""
    with open('competitions.json') as comps:
        return json.load(comps)['competitions']


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    """Return home page with login form."""
    return render_template('index.html')


@app.route('/show_summary', methods=['POST'])
def show_summary():
    """Show summary list of competitions or login page on failed login."""
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions)
    except IndexError:
        flash(EMAIL_ERROR)
        return render_template('index.html'), 401


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]
    if found_club and found_competition:
        return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash(GENERIC_ERROR)
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchase_places', methods=['POST'])
def purchase_places():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    club_points = int(club['points'])
    if places_required > club_points:
        flash(NOT_ENOUGH_POINTS)
    elif places_required <= club_points:
        competition['nb_places'] = int(competition['nb_places']) - places_required
        flash(BOOKING_OK)
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
