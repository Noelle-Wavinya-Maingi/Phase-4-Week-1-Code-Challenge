from server import app

class TestApp:
    def test_home_view(self):
     client = app.test_client(self)
     response = client.get("/")
     assert response.status_code == 200

    def test_restaurant_view(self):
     client = app.test_client(self)
     response = client.get("/restaurants")
     assert response.status_code == 200

    def test_pizza_view(self):
     client = app.test_client(self)
     response = client.get("/pizzas")
     assert response.status_code == 200

    def test_restaurant_pizza_view(self):
     client = app.test_client(self)
     response = client.get('/restaurantspizza')
     assert response.status_code == 200