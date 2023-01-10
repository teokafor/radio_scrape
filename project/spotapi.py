# What should it do?

# The goal of using the Spotify API is to allow users to easily import whatever data is in their JSON files into
# A Spotify playlist.

# This feature should be optional, meaning if the user only wants the raw JSON data without the Spotify stuff, it should
# be necessary to using it.

# If enabled, the program should be able to create a playlist (if one does not already exist) on the end user's Spotify
# account with a generic name. From there, the program should read from the JSON data set, and use artist and song info
# to populate the playlist.

# To prevent long scan times, perhaps implement a "checkpoint" system, where the program will start reading the JSON
# data from a defined point, instead of parsing the entire file each time. This checkpoint can be updated every time a
# song is added to the playlist.

# This will require authorization on the end user's part.

# TODO: Get authorized

# TODO: Read from JSON

# TODO: Write to playlist

import requests

AUTH_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/'


def main():
    authorize()


def authorize():

    with open('SpotCredentials.txt', 'r') as credentials:
        client_id = credentials.readline().split()
        client_secret = credentials.readline().split()

    auth_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }

    auth_response = requests.post(AUTH_URL, data=auth_data)
    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']

    print(access_token)
    # Set up authentication for easy access
    headers = {
        'Authorization': 'Bearer {token}'.format(token='access_token')
    }

    # Get the user's Spotify ID
    #cur_user_id = requests.get(BASE_URL + 'me', headers=headers).json()
    #print(cur_user_id)
    #update_playlist(headers, client_id)









def update_playlist(headers, client_id):
    # Create the playlist
    #req = requests.post(BASE_URL + 'users/{user_id}/playlists'.format(user_id='teokafor'), headers=headers).json()
    #print(req)
    pass


if __name__ == "__main__""":
    main()
