from datetime import datetime, timedelta, timezone
import requests
import json
import jwt
import os

class MyUtils:
    def __init__(self):
        self.access_token_path = "./access_token.json"

    def load_previous_access_token_as_dict(self):
        if not os.path.exists(self.access_token_path):
            return {}
        with open(self.access_token_path, "r") as f:
            return json.load(f)

    def load_previous_cookie(self):
        dict_cookie = self.load_previous_access_token_as_dict()
        return requests.utils.cookiejar_from_dict(dict_cookie)

    def load_previous_access_token(self):
        dict_access_token = self.load_previous_access_token_as_dict()
        return dict_access_token.get("access_token")

    def is_expired(self):
        dict_access_token = self.load_previous_access_token_as_dict()
        if not dict_access_token.get("access_token", False):
            return False
        token = dict_access_token.get("access_token")
        decoded = jwt.decode(token, algorithms="HS256", options={"verify_signature": False})
        expire_in = decoded.get("exp")
        now = datetime.now(tz=timezone.utc).timestamp()
        if expire_in <= now:
            return False
        return True

    def login_and_save_new_cookie(self, url, username, password):
        current_session = requests.Session()
        current_session.post(f"{url}/login/",data={'username':username,'password':password})
        cookies = requests.utils.dict_from_cookiejar(current_session.cookies)
        with open(self.access_token_path, "w") as f:
            json.dump(cookies, f)
        print(">> Cookie saved ...")

    def login_and_save_new_access_token(self, url, username, password):
        current_session = requests.Session()
        response = current_session.post(f"{url}/login/",data={'username':username,'password':password})
        if response.ok:
            token = response.json().get("access_token")
            with open(self.access_token_path, "w") as f:
                json.dump({"access_token": token}, f)
            print(">> Token saved successfully.")
        else:
            print("Login failed:", response.text)