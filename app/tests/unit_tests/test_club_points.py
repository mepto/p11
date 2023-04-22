import server
from constants import BOOKING_OK, MAX_PLACES, MORE_THAN_12_PLACES, NOT_ENOUGH_POINTS


def test_less_points_than_places_purchased(client):
    """Test purchasing more places than points available."""
    original_clubs = server.clubs
    try:
        server.clubs = [
            {
                'name': 'Club1',
                'email': 'test@club.c',
                'points': '1'
            }
        ]
        server.competitions = [
            {
                'name': 'Compet1',
                'date': '2023-07-27 10:00:00',
                'nb_places': '3'
            }
        ]
        places_requested = 3

        response = client.post('/purchase_places', data={'places': places_requested, 'club': server.clubs[0]['name'],
                                                         'competition': server.competitions[0]['name']})
        assert NOT_ENOUGH_POINTS in response.data.decode()
    finally:
        server.clubs = original_clubs


def test_more_points_than_places_purchased(client):
    """Test purchasing less than points available."""
    original_clubs = server.clubs
    try:
        server.clubs = [
            {
                'name': 'Club1',
                'email': 'test@club.c',
                'points': '1'
            }
        ]
        server.competitions = [
            {
                'name': 'Compet1',
                'date': '2023-07-27 10:00:00',
                'nb_places': '3'
            }
        ]
        places_requested = 1

        response = client.post('/purchase_places', data={'places': places_requested, 'club': server.clubs[0]['name'],
                                                         'competition': server.competitions[0]['name']})
        assert BOOKING_OK in response.data.decode()
    finally:
        server.clubs = original_clubs


def test_more_than_12_places_purchased(client):
    """Test purchasing more than MAX_PLACES."""
    original_clubs = server.clubs
    try:
        server.clubs = [
            {
                'name': 'Club1',
                'email': 'test@club.c',
                'points': '15'
            }
        ]
        server.competitions = [
            {
                'name': 'Compet1',
                'date': '2023-07-27 10:00:00',
                'nb_places': '45'
            }
        ]
        places_requested = MAX_PLACES + 1

        response = client.post('/purchase_places', data={'places': places_requested, 'club': server.clubs[0]['name'],
                                                         'competition': server.competitions[0]['name']})
        assert MORE_THAN_12_PLACES in response.data.decode()
    finally:
        server.clubs = original_clubs
