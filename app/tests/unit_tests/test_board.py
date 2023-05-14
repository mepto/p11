import pytest

import server


def test_points_board(client):
    """Test that board displays clubs and points."""
    original_clubs = server.clubs
    try:
        server.clubs = [
            {
                'name': 'Club1',
                'email': 'test@club.c',
                'points': 1
            },
            {
                'name': 'Club2',
                'email': 'test2@club.c',
                'points': 42
            }
        ]

        response = client.get('/points_board')

        assert response.status_code == 200
        for club in server.clubs:
            assert f"<h3>{ club['name'] } (secretary: { club['email'] }</h3>" in response.data.decode()
            assert f"<p>Points balance: { club['points'] }</p>" in response.data.decode()
    finally:
        server.clubs = original_clubs
