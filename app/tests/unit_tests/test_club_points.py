from datetime import date, timedelta

import pytest

import server
from constants import BOOKING_OK, MAX_PLACES, MORE_THAN_12_PLACES, NOT_ENOUGH_POINTS


@pytest.mark.parametrize('club_points, competition_places, places_requested, points_changed, result_expected',
                         [
                             ('1', '3', 3, False, NOT_ENOUGH_POINTS),
                             ('15', '45', MAX_PLACES + 1, False, MORE_THAN_12_PLACES),
                             ('1', '3', 1, True, BOOKING_OK),
                             ('13', '45', 12, True, BOOKING_OK)
                         ])
def test_club_purchasing_places(client, club_points, competition_places, places_requested,
                                points_changed, result_expected):
    """Test clubs purchasing competition places."""
    original_clubs = server.clubs
    original_competitions = server.competitions
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
        assert (int(server.clubs[0]['points']) != int(club_points)) is points_changed
        assert result_expected in response.data.decode()
    finally:
        server.clubs = original_clubs
        server.competitions = original_competitions
