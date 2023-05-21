import server
from constants import BOOKING_OK


def test_default_success_path(client):
    """Test user checking board, login in, purchasing places."""

    # Check clubs are loaded
    clubs = server.clubs
    assert clubs and clubs[0]['email']
    # Check competitions are loaded
    competitions = server.competitions
    assert competitions and competitions[0]['name']

    # Check point board displays
    board = client.get('/points_board')
    assert board.status_code == 200
    for club in clubs:
        assert f'<h3 class="item-name">{club["name"]} <span class="small">Secretary: {club["email"]}</span></h3>' in \
               board.data.decode()

    # Check homepage display
    home = client.get('/')
    assert home.status_code == 200

    # Check login
    login = client.post("/show_summary", data={"email": clubs[0]['email']}, follow_redirects=True)
    assert login.status_code == 200
    assert clubs[0]['email'] in login.data.decode()

    # Check booking page display
    booking = client.get(f"/book/{competitions[0]['name']}/{clubs[0]['name']}")
    assert booking.status_code == 200
    assert clubs[0]['name'] in booking.data.decode()

    # Check successful purchase
    initial_points = int(clubs[0]['points'])
    places_requested = 10
    purchase = client.post('/purchase_places', data={'places': places_requested, 'club': clubs[0]['name'],
                                                     'competition': competitions[0]['name']})
    assert purchase.status_code == 200
    assert int(clubs[0]['points']) == initial_points - places_requested
    assert BOOKING_OK in purchase.data.decode()

    # Check logout
    logout = client.get('/logout', follow_redirects=True)
    assert logout.status_code == 200
    assert 'Welcome' in logout.data.decode()
