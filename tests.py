import unittest
import server

class MyAppIntegrationTestCase(unittest.TestCase):
    def test_index(self):
        client = server.app.test_client()
        result = client.get('/')
        self.assertIn('<title>Poolavan | Ridesharing for Adventurers. </title>', result.data)

    def test_userlogin(self):
        client = server.app.test_client()
        server.app.config['TESTING'] = True
        result = client.get('/userlogin', data ={'username': 'password'})
        self.assertIn('<div id="homepage-block"></div>', result.data)

    def test_register(self):
        client = server.app.test_client()
        server.app.config['TESTING'] = True
        result = client.get('/register')
        self.assertIn('<h1>Register</h1>', result.data)

    def test_mytrips(self):
        client = server.app.test_client()
        server.app.config['TESTING'] = True
        result = client.get('/mytrips')
        self.assertIn('<h2>My Trips:</h2>', result.data)


if __name__ == "__main__":
    unittest.main()