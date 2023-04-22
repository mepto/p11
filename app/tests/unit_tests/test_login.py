from constants import EMAIL_ERROR
from app.tests.data import DataForTests


def test_login_unknown_email(client):
    """Check the system provide a human-readable error on unknown email."""
    response = client.post("/show_summary", data={"email": DataForTests.UNKNOWN_USER}, follow_redirects=True)
    assert str.encode(EMAIL_ERROR) in response.data
    assert response.status_code == 401


def test_login_known_email(client):
    """Check the system sends a positive response when the email is known."""
    response = client.post("/show_summary", data={"email": DataForTests.VALID_USER}, follow_redirects=True)
    assert str.encode(DataForTests.VALID_USER) in response.data
    assert response.status_code == 200
