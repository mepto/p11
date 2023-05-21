from datetime import date, datetime

from flask import flash, Flask, redirect, render_template, request, url_for

from constants import BOOKING_OK, EMAIL_ERROR, GENERIC_ERROR, MAX_PLACES, MORE_THAN_12_PLACES, NOT_ENOUGH_POINTS, \
    PAST_COMPETITION_DATE
from app.utils import load_clubs, load_competitions

app = Flask(__name__,
            static_url_path='',
            static_folder='app/components',
            template_folder='app/templates')
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
    competition_date = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S").date()
    if competition_date <= date.today():
        flash(PAST_COMPETITION_DATE)
    if places_required > club_points:
        flash(NOT_ENOUGH_POINTS)
    if places_required > MAX_PLACES:
        flash(MORE_THAN_12_PLACES)
    if places_required <= club_points and places_required < MAX_PLACES and competition_date > date.today():
        competition['nb_places'] = int(competition['nb_places']) - places_required
        club['points'] = int(club['points']) - places_required
        flash(BOOKING_OK)
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/points_board')
def show_points_board():
    all_clubs = sorted(clubs, key=lambda club: club['name'])
    return render_template('points_board.html', clubs=all_clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
