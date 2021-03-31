from app import app, get_weather
import unittest


class FlaskTest(unittest.TestCase):

    def test_index(self):
        """ comprobar si el estado es 200 """
        tester = app.test_client(self)
        response = tester.get("/")
        status = response.status_code
        self.assertEqual(status, 200)

    def test_index_data(self):
        # comprobar que devuelve datos
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertTrue(b'Postal' in response.data)

    def test_get_weather(self):
        # comprobar llamada a la api
        response = get_weather(23330, "XwTaXqXzXaXr4e5")
        self.assertTrue('locality' in response.keys())


if __name__ == "__main__":
    unittest.main()


