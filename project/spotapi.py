# What should it do?

# The goal of using the Spotify API is to allow users to easily import whatever data is in their JSON files into
# A Spotify playlist.

# This feature should be optional, meaning if the user only wants the raw JSON data without the Spotify stuff, it should
# be unnecessary to using it.

# If enabled, the program should be able to create a playlist (if one does not already exist) on the end user's Spotify
# account with the name of the JSON file (to denote what station this data is from). From there, the program should
# read from the JSON data set, and use artist and song info to populate the playlist.

# To prevent long scan times, perhaps implement a "checkpoint" system, where the program will start reading the JSON
# data from a defined point, instead of parsing the entire file each time. This checkpoint can be updated every time a
# song is added to the playlist.

# This will require authorization on the end user's part.

import spotipy
import json

# Needed for the authorization code OAuth2 flow
from spotipy.oauth2 import SpotifyOAuth

AUTH_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/'
SCOPE = 'user-read-private playlist-modify-public'


def main(meta_key, station_name, playlist_id, song_name, artist_name):

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))

    # Get the current user's id and region.
    cur_user_id = sp.current_user().get('id')
    cur_user_region = sp.current_user().get('country')

    if playlist_id == 'None':  # No matching playlist id
        # Create a playlist on the user's account and grab its id.
        playlist_id = sp.user_playlist_create(cur_user_id, station_name).get('id')
        # TODO: Write the newly created playlist ID to the json file.
        with open('stations.json', 'r+') as song_file:
            temp_data_all = json.load(song_file)  # Grab all the json data
            temp_data_scoped = temp_data_all.get(f'{meta_key}')  # Grab the part we want to update
            temp_data_scoped[0].update({'playlist_id': playlist_id})  # Write new data to the desired location
            temp_data_all.update({f'{meta_key}': temp_data_scoped})  # Reintegrate new data into json file
            song_file.truncate(0)
            song_file.seek(0)
            json.dump(temp_data_all, song_file, indent=4, separators=(', ', ': '), ensure_ascii=False)

    cur_query = f"{song_name} by {artist_name}"
    cur_song_id = f'spotify:track:{sp.search(cur_query, 5, 0, "track", cur_user_region)["tracks"]["items"][0]["id"]}'
    sp.playlist_add_items(playlist_id, [cur_song_id])


if __name__ == "__main__":
    main()
