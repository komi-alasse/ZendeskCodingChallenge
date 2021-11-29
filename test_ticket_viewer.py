import unittest, requests, json, main
from dotenv import dotenv_values

url = dotenv_values('credentials.env')['URL']
user = dotenv_values('credentials.env')['USER'] + '/token'
key = dotenv_values('credentials.env')['API_KEY']

test_endpoint = "https://zcc5764.zendesk.com/api/v2/users/1524206641041.json"

class Test(unittest.TestCase):
    
    def test_credentials(self):
        response = requests.get(url, auth=(user, pwd))
        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)
     
    def test_false_credentials(self):
        response = requests.get(url, auth=(user, "password"))
        self.assertEqual(response.status_code, 401 or 400)
        

    def test_display_all_tickets():
        all_tickets = main.display_all_tickets()
        self.assertEqual(all_tickets, 102)
        
        

    def test_get_single_ticket():
        response = main.get_single_ticket(test_endpoint, {})
        self.assertNotEqual(response, -1)

        

if __name__ == "__main__":
    unittest.main()