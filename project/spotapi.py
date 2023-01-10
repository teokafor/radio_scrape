# What should it do?

# The goal of using the Spotify API is to allow users to easily import whatever data is in their JSON files into
# A Spotify playlist.

# This feature should be optional, meaning if the user only wants the raw JSON data without the Spotify stuff, it should
# be necessary to using it.

# If enabled, the program should be able to create a playlist (if one does not already exist) on the end user's Spotify
# account with the name of the JSON file (to denote what station this data is from). From there, the program should
# read from the JSON data set, and use artist and song info to populate the playlist.

# To prevent long scan times, perhaps implement a "checkpoint" system, where the program will start reading the JSON
# data from a defined point, instead of parsing the entire file each time. This checkpoint can be updated every time a
# song is added to the playlist.

# This will require authorization on the end user's part.

# TODO: Get authorized

# TODO: Read from JSON

# TODO: Write to playlist

import requests
import spotipy

# Needed for the authorization code OAuth2 flow
from spotipy.oauth2 import SpotifyOAuth

AUTH_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/'
SCOPE = 'user-read-private playlist-modify-public'


def main():
    authorize()


def authorize():

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))

    # Get the current user's id.
    cur_user_id = sp.current_user().get('id')

    # Create a playlist on the user's account
    # TODO: Check if a playlist already exists with the same name, if so, skip step
    # TODO: Change main.py code to give unique names to stations
    results = sp.user_playlist_create(cur_user_id, 'API_GEN_PLYLST')


if __name__ == "__main__""":
    main()
