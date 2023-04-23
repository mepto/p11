from datetime import date, timedelta
import pytest

import server
from constants import BOOKING_OK, MAX_PLACES, PAST_COMPETITION_DATE


@pytest.mark.parametrize('competition_date, expected_result',
                         [
                             ((date.today() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"), BOOKING_OK),
                             ((date.today() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
                              PAST_COMPETITION_DATE),
                         ])
def test_clubs_book_past_competition(client, competition_date, expected_result):
    """Test booking depending on competition dates."""
    original_clubs = server.clubs
    try:
        server.clubs = [
            {
                'name': 'Club1',
                'email': 'test@club.c',
                'points': MAX_PLACES - 1
            }
        ]
        server.competitions = [
            {
                'name': 'Compet1',
                'date': competition_date,
                'nb_places': MAX_PLACES * 2
            }
        ]

        response = client.post('/purchase_places', data={'places': MAX_PLACES - 2, 'club': server.clubs[0]['name'],
                                                         'competition': server.competitions[0]['name']})
        assert expected_result in response.data.decode()
    finally:
        server.clubs = original_clubs
