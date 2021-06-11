# -*- coding: UTF-8 -*-


import argparse
import re
import json
import requests
from random import shuffle

DEFAULT_CONFIG_PATH = "/opt/lynch/lynch.json"
PLAYLIST_URL = "https://api.music.yandex.net/users/uid/playlists/playlist_id"


def get_playlist_tracks(uid, playlist_id):
    url = re.sub("uid", str(uid), PLAYLIST_URL)
    url = re.sub("playlist_id", str(playlist_id), url)
    data = json.loads(requests.get(url).text)
    tracks = []
    for track in data["result"]["tracks"]:
        tracks.append(track)
    return tracks


def get_playlist_revision(uid, playlist_id):
    url = re.sub("uid", str(uid), PLAYLIST_URL)
    url = re.sub("playlist_id", str(playlist_id), url)
    data = json.loads(requests.get(url).text)
    return data["result"]["revision"]


def change_playlist(uid, playlist_id, diff, music_oauth_headers):
    playlist_revision = get_playlist_revision(uid, playlist_id)
    diff = re.sub("'", '"', str(diff))
    api_data = {'kind': playlist_id,
                'revision': playlist_revision, 'diff': diff}

    url = re.sub("uid", str(uid), PLAYLIST_URL)
    url = re.sub("playlist_id", str(playlist_id), url)
    url += "/change"
    result = requests.post(
        url, headers=music_oauth_headers, data=api_data).text
    return result


def clean_playlist(uid, playlist_id, music_oauth_headers):
    playlist_size = len(get_playlist_tracks(
        uid, playlist_id))
    diff = [
        {
            "op": "delete",
            "at": 0,
            "from": 0,
            "to": playlist_size
        }
    ]
    change_playlist(uid, playlist_id, diff, music_oauth_headers)


def add_tracks_to_playlist(uid, playlist_id, tracks, music_oauth_headers):
    diff = [
        {
            "op": "insert",
            "at": 0,
            "tracks": tracks
        }
    ]
    change_playlist(uid, playlist_id, diff, music_oauth_headers)


def load_config(path):
    with open(path) as f:
        return json.loads(f.read())


def get_track_by_id(tracks, id):
    for track in tracks:
        if track["id"] == id:
            title = track["track"]["title"]
            artist = track["track"]["artists"][0]["name"]
            return {"title": title, "artist": artist}


def process_config(config_path):

    config = load_config(config_path)
    music_oauth_headers = {"Authorization": "OAuth " +
                           config["destination"]["music_oauth_token"]}
    destination_uid = config["destination"]["uid"]
    destination_playlist_id = config["destination"]["playlist_id"]

    playlists = config["source_playlists"]

    all_tracks = []
    for user in playlists:
        tracks = get_playlist_tracks(user["uid"], user["playlist_id"])
        all_tracks += tracks
        tracks_ids = [track["id"] for track in tracks]
        shuffle(tracks_ids)
        playlists[playlists.index(user)]["tracks"] = tracks_ids
        print("Got tracks for " + user["login"])

    longest_playlist_size = 0
    for user in playlists:
        if len(user["tracks"]) > longest_playlist_size:
            longest_playlist_size = len(user["tracks"])

    mixed_playlist = []
    for i in range(0, longest_playlist_size):
        for user in playlists:
            user_tracks = user["tracks"]
            if i < len(user_tracks):
                mixed_playlist.append(user_tracks[i])

    api_tracks = []
    for track in mixed_playlist:
        api_tracks.append({"id": track})

    clean_playlist(destination_uid, destination_playlist_id,
                   music_oauth_headers)
    add_tracks_to_playlist(destination_uid, destination_playlist_id,
                           api_tracks, music_oauth_headers)
    named_tracks = [get_track_by_id(all_tracks, track["id"])
                    for track in api_tracks]
    return named_tracks


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str,
                        default=DEFAULT_CONFIG_PATH, required=False, help="Config path")
    args = parser.parse_args()
    print(process_config(args.config))
