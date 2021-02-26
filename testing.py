import os
import unittest
import requests
import json

class TestCase(unittest.TestCase):

    def success_test(self, message):
        print(f'Test {message} passed')

    def test_registration_user(self):
        user_data = {'u_name':'Aleksandr', 'username':'us', 'password':'1235'}
        resp = requests.post('http://127.0.0.1:5000/api/user/registration', json=user_data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {'Success':'User has been registered'})
        self.success_test('registration')
 
    def test_authorization_user(self):
        user_data = {'username':'alex', 'password':'1235'}
        resp = requests.post('http://127.0.0.1:5000/api/user/authorization', json=user_data)
        self.assertEqual(resp.status_code, 200)          
        self.assertEqual(resp.json(), {'Success':'User login'})
        self.success_test('authorization')
    
    def test_add_article(self):
        s = requests.Session()
        user_data = {'username':'usx1', 'password':'1235'}
        s.post('http://127.0.0.1:5000/api/user/authorization', json=user_data)
        article_data = {'title':'Title', 'body':'Body'}
        resp = s.post('http://127.0.0.1:5000/api/article/add_article', json=article_data)
        self.assertEqual(resp.status_code, 200)          
        self.assertEqual(resp.json(), {'Success':'Artlicle has been added'})
        self.success_test('add article')

    def test_incorrect_registration_user(self):
        user_data = {'u_name':'Aleksandr', 'username':'alex', 'password':'1235'}
        resp = requests.post('http://127.0.0.1:5000/api/user/registration', json=user_data)
        self.assertEqual(resp.status_code, 400)
        self.success_test('with incorrect user data for registration')

    def test_change_password_user(self):
        s = requests.Session()
        user_data = {'username':'usx1', 'password':'1235'}
        s.post('http://127.0.0.1:5000/api/user/authorization', json=user_data)
        new_user_data = {'password':'12345'}
        resp = s.post('http://127.0.0.1:5000/api/user/change_password', json=new_user_data)
        self.assertEqual(resp.status_code, 200)          
        self.assertEqual(resp.json(), {'Success':'Password has been changed'})
        self.success_test('change password')

    def test_update_article(self):
        s = requests.Session()
        user_data = {'username':'alex', 'password':'12345'}
        s.post('http://127.0.0.1:5000/api/user/authorization', json=user_data)
        resp = s.put('http://127.0.0.1:5000/api/article/1')
        self.assertEqual(resp.status_code, 200)          
        self.assertEqual(resp.json(), {'Success':'Article has been updated'})
        self.success_test('update article')

    def test_delete_article(self):
        s = requests.Session()
        user_data = {'username':'alex', 'password':'1235'}
        s.post('http://127.0.0.1:5000/api/user/authorization', json=user_data)
        resp = s.delete('http://127.0.0.1:5000/api/article/2')
        self.assertEqual(resp.status_code, 200)          
        self.assertEqual(resp.json(), {'Success':'Article deleted'})
        self.success_test('delete article')

if __name__ == '__main__':
    TestCase().test_registration_user()
    TestCase().test_authorization_user()
    TestCase().test_add_article()
    TestCase().test_incorrect_registration_user()
    TestCase().test_change_password_user()
    TestCase().test_update_article()
    TestCase().test_delete_article()
