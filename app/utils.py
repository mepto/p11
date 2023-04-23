import json
from datetime import date, datetime


def load_clubs():
    """Return list of clubs based on clubs file."""
    with open('clubs.json') as c:
        return json.load(c)['clubs']


def load_competitions():
    """Return list of competitions based on competitions file."""
    with open('competitions.json') as comps:
        competitions = json.load(comps)['competitions']
        for competition in competitions:
            if datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S").date() > date.today():
                competition['is_active'] = True
        competitions.sort(key=lambda x: x['date'], reverse=True)
        return competitions
