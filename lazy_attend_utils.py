from datetime import datetime, timedelta, timezone
import requests
import json
import jwt
import os

class MyUtils:
    def __init__(self):
        self.cookie_path = "./cookie.json"

    def load_previous_cookie_as_dict(self):
        if not os.path.exists(self.cookie_path):
            return {}
        with open(self.cookie_path, "r") as f:
            return json.load(f)

    def load_previous_cookie(self):
        dict_cookie = self.load_previous_cookie_as_dict()
        return requests.utils.cookiejar_from_dict(dict_cookie)

    def is_expired(self):
        dict_cookie = self.load_previous_cookie_as_dict()
        if not dict_cookie.get("access_token_cookie", False):
            return False
        token = dict_cookie.get("access_token_cookie")
        decoded = jwt.decode(token, algorithms="HS256", options={"verify_signature": False})
        expire_in = decoded.get("exp")
        now = datetime.now(tz=timezone.utc).timestamp()
        if expire_in <= now:
            return False
        return True

    def login_and_save_new_cookie(self, url, email, password):
        current_session = requests.Session()
        current_session.post(f"{url}/login",json={'email':email,'password':password})
        cookies = requests.utils.dict_from_cookiejar(current_session.cookies)
        with open("./cookie.json", "w") as f:
            json.dump(cookies, f)
        print(">> Cookie saved ...")
