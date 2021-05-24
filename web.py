#!/opt/lynch/python/bin/python3
# -*- coding: UTF-8 -*-

from bottle import route, run, request, response, redirect, template, TEMPLATE_PATH, HTTPResponse
from lynch import process
import json

CONFIGS = {"mini.burmistrov.pw": "/opt/lynch/mini.json",
           "lynch.burmistrov.pw": "/opt/lynch/lynch.json"}


def get_hostname_playlist(hostname):
    config = process.load_config(CONFIGS[hostname])
    return config["destination"]["playlist_id"]


@route("/ping", method="GET")
def ping():
    return "pong"


@route("/shuffle", method="GET")
def shuffle():
    all_tracks = process.process_config(CONFIGS[request.headers["Host"]])
    html_tracks = ""
    for track in all_tracks:
        html_tracks += "<div class='title'>" + \
            track["title"] + "</div><div class='artist'>" + \
            track["artist"] + "</div>"
    return html_tracks


@route("/", method="GET")
def root():
    return template("main.tpl", playlist_id=get_hostname_playlist(request.headers["Host"]))


if __name__ == "__main__":
    run(host='::', port=7070, debug=True)
