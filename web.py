# -*- coding: UTF-8 -*-

import json

from bottle import route, run, request, response, redirect, template, TEMPLATE_PATH, HTTPResponse
from yamix import process


CONFIG_FILE = "/etc/yamix/config.json"
MAIN_TEMPLATE = "main.tpl"

with open(CONFIG_FILE) as f:
    CONFIG = json.load(f)


def get_hostname_playlist(hostname):
    config = process.load_config(CONFIG[hostname])
    return config["destination"]["playlist_id"]


@route("/ping", method="GET")
def ping():
    return "pong"


@route("/shuffle", method="GET")
def shuffle():
    all_tracks = process.process_config(CONFIG[request.headers["Host"]])
    html_tracks = ""
    for track in all_tracks:
        html_tracks += "<div class='title'>" + \
            track["title"] + "</div><div class='artist'>" + \
            track["artist"] + "</div>"
    return html_tracks


@route("/", method="GET")
def root():
    return template(MAIN_TEMPLATE, playlist_id=get_hostname_playlist(request.headers["Host"]))


if __name__ == "__main__":
    run(host='::', port=7070, debug=True)
