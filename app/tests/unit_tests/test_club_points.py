from datetime import date, timedelta

import pytest

import server
from constants import BOOKING_OK, MAX_PLACES, MORE_THAN_12_PLACES, NOT_ENOUGH_POINTS


@pytest.mark.parametrize('club_points, competition_places, places_requested, result_expected',
                         [
                             ('1', '3', 3, NOT_ENOUGH_POINTS),
                             ('15', '45', MAX_PLACES + 1, MORE_THAN_12_PLACES),
                             ('1', '3', 1, BOOKING_OK)
                         ])
def test_club_purchasing_places(client, club_points, competition_places, places_requested, result_expected):
    """Test clubs purchasing competition places."""
    original_clubs = server.clubs
    try:
        server.clubs = [
            {
                'name': 'Club1',
                'email': 'test@club.c',
                'points': club_points
            }
        ]
        server.competitions = [
            {
                'name': 'Compet1',
                'date': (date.today() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
                'nb_places': competition_places
            }
        ]
        places_requested = places_requested

        response = client.post('/purchase_places', data={'places': places_requested, 'club': server.clubs[0]['name'],
                                                         'competition': server.competitions[0]['name']})
        assert result_expected in response.data.decode()
    finally:
        server.clubs = original_clubs
