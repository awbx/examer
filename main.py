from requests import session
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from os import path, environ
import time
import sys

BASE_URL = "https://intra.42.fr"

load_dotenv()

class SignInFailed(Exception):
    """Sign In Exception"""
    pass


class Examer:
    def __init__(self, username, password):
        self.username= username
        self.password = password
        self.sess = session()
    
    def sign_in(self):
        endpoint = "users/sign_in"
        res = self.sess.get(self.build_url(endpoint))
        soup = BeautifulSoup(res.text, "html.parser")
        token_el = soup.find("input", {"name":"authenticity_token"})
        if token_el:
            data = {
                "utf8":"✓",
                "authenticity_token":token_el.attrs.get('value'),
                "user[login]":self.username,
                "user[password]": self.password,
                "commit": "Sign in"
            }
            res = self.sess.post(self.build_url(endpoint), data=data)
            if res.status_code == 200 and self.is_logged_in():
                return 
        raise SignInFailed()
    
    def register(self):
        BASE_URL = 'https://profile.intra.42.fr'
        if not self.is_logged_in():
            self.sign_in()
            return 
        res = self.sess.get(self.build_url(""))
        soup = BeautifulSoup(res.text, "html.parser")
        exam_el = soup.find("a", {"data-class": "exam-modal"})
        token_el = soup.find("meta", {"name":"csrf-token"})
        if token_el and exam_el:
            if exam_el.parent.parent.parent.find("span", {"class":"event-registered"}):
                print("You're already registered in the exam event!")
                exit(0)
            data = {
                "_method": "post",
                "authenticity_token": token_el.attrs.get("content")
            }
            print("Registering in the exam event!")
            res = self.sess.post(self.build_url(f"{exam_el.attrs.get('data-url')[1:]}/exams_users", BASE_URL), data=data)
        elif not exam_el:
            print("No exam event yet !")
        
    def build_url(self, endpoint, base_url = None):
        if not base_url:
            base_url = BASE_URL
        return path.join(base_url, endpoint)
    
    def is_logged_in(self):
        return self.sess.cookies.get("user.id")


forty_two_user = environ.get("INTRA_USER", None)
forty_two_pass = environ.get("INTRA_PASS", None)

try:
    examer = Examer(forty_two_user, forty_two_pass)
    examer.sign_in()
    while True:
        print("Checking if the exam event exists...")
        examer.register()
        time.sleep(1)
except SignInFailed:
    print("Failed to Sign In, please check your credentials!", file=sys.stderr)
except Exception as e:
    print("Error : %s", e, file=sys.stderr);