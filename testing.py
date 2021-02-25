import os
import unittest
import requests
import json

class TestCase(unittest.TestCase):

    def test_registration_user(self):
        user_data = {'u_name':'Aleksandr', 'username':'alex', 'password':'1235'}
        resp = requests.post('http://127.0.0.1:5000/api/user/registration', json=user_data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {'Success':'User has been registered'})
 
    def test_authorization_user(self):
        user_data = {'username':'alex', 'password':'1235'}
        resp = requests.post('http://127.0.0.1:5000/api/user/authorization', json=user_data)
        self.assertEqual(resp.status_code, 200)          
        self.assertEqual(resp.json(), {'Success':'User login'})
    
    def test_add_article(self):
        article_data = {'title':'Title', 'body':'Body'}
        resp = requests.post('http://127.0.0.1:5000/api/article/add_article_test', json=article_data)
        self.assertEqual(resp.status_code, 200)          
        self.assertEqual(resp.json(), {'Success':'Artlicle has been added'})

    def test_incorrect_registration_user(self):
        user_data = {'u_name':'Aleksandr', 'username':'alex', 'password':'1235'}
        resp = requests.post('http://127.0.0.1:5000/api/user/registration', json=user_data)
        self.assertEqual(resp.status_code, 400)
    
    def test_incorrect_authorization_user(self):
        user_data = {'username':'alex', 'password':'qwerty'}
        resp = requests.post('http://127.0.0.1:5000/api/user/authorization', json=user_data)
        self.assertEqual(resp.status_code, 404)

if __name__ == '__main__':
    #TestCase().test_registration_user()
    #TestCase().test_authorization_user()
    #TestCase().test_add_article()
    #TestCase().test_incorrect_registration_user()
    TestCase().test_incorrect_authorization_user()