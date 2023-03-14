import json
import os
from urllib.parse import quote_plus

import requests

class Config:
    GERRIT_USER = "droidfreak32"
    GERRIT_PASS = "AyRyYkhV2DAGf6Q0m615P8C2jZhHZiVUkr8Z8y27Ig"

    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

class Gerrit:
    def __init__(self):
        self.auth = requests.auth.HTTPBasicAuth(Config.GERRIT_USER, Config.GERRIT_PASS)

    def get_projects(self):
        url = "https://localhost:8443/a/projects/?t"
        resp = requests.get(url, auth=self.auth, verify=False)

        if resp.status_code != 200:
            raise Exception(f"Error communicating with gerrit: {resp.text}")

        projects = json.loads(resp.text[5:])
        return projects

    def update_parent(self, child, parent, auth=None):
        child = quote_plus(child)
        url = f"https://review.lineageos.org/a/projects/{child}/parent"
        print(f"Updating {child}'s parent to {parent}")
        resp = requests.put(url, json=({"parent": parent, "commit_message": "Auto update from gerrit_config"}), auth=self.auth)
        if resp.status_code != 200:
            raise Exception(f"Error communicating with gerrit: {resp.text}")

    def create_project(self, name):
        url = f"https://review.lineageos.org/a/projects/{name.replace('/', '%2f')}"
        resp = requests.put(url, auth=self.auth)
        if resp.status_code != 201:
            raise Exception(f"Error communicating with gerrit: {resp.text}")
