from locust import HttpUser, task

from app.utils import load_clubs, load_competitions


class Locust(HttpUser):

    @task
    def view_home(self):
        response = self.client.get("/", name="home")

    @task
    def view_points_board(self):
        response = self.client.get("/points_board", name="points_board")

    def login(self):
        response = self.client.post("/show_summary", data={'email': load_clubs()[0]["email"]}, name="show_summary")

    @staticmethod
    def get_data():
        club = load_clubs()[0]
        competition = load_competitions()[0]
        return club, competition

    @task
    def view_competition_booking(self):
        club, competition = self.get_data()
        response = self.client.get(f"/book/{competition['name']}/{club['name']}", name="booking")

    @task
    def purchase_places(self):
        club, competition = self.get_data()
        response = self.client.post(f"/purchase_places", data={'places': 2, 'club': club['name'],
                                                               'competition': competition['name']}, name="purchase")

    def on_start(self):
        self.login()
