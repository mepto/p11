import json


def load_clubs():
    """Return list of clubs based on clubs file."""
    with open('clubs.json') as c:
        return json.load(c)['clubs']


def load_competitions():
    """Return list of competitions based on competitions file."""
    with open('competitions.json') as comps:
        return json.load(comps)['competitions']
