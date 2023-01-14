import time
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json
import os

import spotapi

SCRAPE_FREQUENCY = 120  # The time (in seconds) that the website should be checked.
IGNORE_WRITE_TIME = 25  # If songs found are the same as the last entry and are under this value, then ignore write.
TIME_FORMAT = "%H:%M"  # Used to format (and un-format) time data.


def user_controls():
    song_file = json.load(open('stations.json'))

    # Stations.
    increment_value = 0
    for entry in song_file:
        increment_value += 1
        station_name = song_file.get(f'{increment_value}')[0].get('name')
        print(f'{increment_value}.\t{station_name}')

    # Other options.
    print(f'----------------------------------\n0. Program Options\n{increment_value+1}. New Station')

    # Check that the input is valid
    valid_input_range = range(0, increment_value + 2)  # TODO: What does this look like with an empty json file?
    while True:
        try:
            user_choice = int(input(f'Please select an option from the list: '))
        except ValueError:
            user_choice = -1
        if user_choice not in valid_input_range:
            print('Please select a valid option from the list.\n')
        else:
            break

    if user_choice == 0:
        print('Program options (coming soon)')
        exit()
    elif user_choice != (increment_value + 1):
        return user_choice
    else:
        new_station_name = input("Enter the radio station's name: ")  # Used to label the Spotify playlist
        new_station_url = input("The URL: ")  # Used by bs4 to fetch the data
        new_title_id = input("Now paste the song title id (html element): ")  # The name of the element with song title.
        new_artist_id = input("Next, the artist id (html element): ")  # The name of the element with artist name

        new_station_data = {  # Format the data into a dictionary
            "name": new_station_name,
            "url": new_station_url,
            "title_id": new_title_id,
            "artist_id": new_artist_id,
            "playlist_id": "None"
        }
        nsd = {f'{user_choice}': [new_station_data]}  # More formatting

        # Do a special write for the new metadata
        with open('stations.json', 'r+') as song_file:
            temp_dict = json.load(song_file)
            temp_dict.update(nsd)

            # Clear the file before writing
            song_file.truncate(0)
            song_file.seek(0)
            json.dump(temp_dict, song_file, indent=4, separators=(', ', ': '), ensure_ascii=False)

        user_controls()  # Show options again after a new station has been made
        # TODO: Fix bug where picking a newly created station causes a 1st time crash (won't crash 2nd time)


def main():
    # TODO: Does this not close??
    song_file = json.load(open('stations.json'))

    user_choice = user_controls()

    station_url = song_file.get(f'{user_choice}')[0].get('url')
    song_title_id = song_file.get(f'{user_choice}')[0].get('title_id')
    song_artist_id = song_file.get(f'{user_choice}')[0].get('artist_id')
    #spotify_playlist_id = song_file.get(f'{user_choice}')[0].get('playlist_id')

    while True:  # Loop until the program is closed

        # The URL to gather data from
        resource = requests.get(station_url)

        if resource.status_code != 200:  # Throw an error if the page cannot be returned for any reason.
            print("couldn't fetch page!")
            print(f'error code f{resource.status_code}')
            exit()

        # Grab and format data
        content = resource.content
        raw_data = BeautifulSoup(content.decode('utf-8'), 'html.parser')

        # Collect necessary information
        song_title = raw_data.find(id=song_title_id).string
        song_artist = raw_data.find(id=song_artist_id).string
        scrape_date = datetime.now().strftime("%m-%d-%Y")
        scrape_time = datetime.now().strftime(TIME_FORMAT)

        # Compile data into a writable dict object
        song_data = {
            "Title": song_title,
            "Artist": song_artist,
            "Date": scrape_date,
            "Time": scrape_time
        }

        # Used for comparison later (& convenient printing now ;) )
        new_song = list(song_data.values())

        # Print output
        print(f'\nSong Title:  {new_song[0]}\nSong Artist: {new_song[1]}'
              f'\nScrape Date: {new_song[2]}\nScrape Time: {new_song[3]}\n')

        # If the file does not exist (or it does but is empty), create it and/or write preliminary data
        if not (os.path.isfile('stations.json')) or os.stat('stations.json').st_size == 0:
            with open('stations.json', 'w') as song_file:
                song_file.write('[]')

        # Read contents from JSON file
        with open('stations.json') as song_file:
            # Load the JSON data into a list
            temp_list = json.load(song_file)
            temp_list = temp_list.get(f'{user_choice}')

            # Grab the latest dict entry in the list
            try:
                last_dict_item = next(reversed(temp_list))
            except StopIteration:
                print("the file is empty, so dont worry about comparing songs")

                # Write first song to file
                write_song(song_data, user_choice)
            else:
                # Convert both songs to lists
                old_song = list(last_dict_item.values())

                # If it's the same song, by the same artist, on the same day, then compare times
                if old_song[0] == new_song[0] and old_song[1] == new_song[1] and old_song[2] == new_song[2]:

                    print('Similar song found!')

                    # Format date strings into datetime objects
                    last_song_time = datetime.strptime(old_song[3], TIME_FORMAT)
                    current_song_time = datetime.strptime(new_song[3], TIME_FORMAT)

                    # Compare times to see if it's a duplicate
                    time_delta_full = current_song_time - last_song_time
                    time_delta_minutes = (int(time_delta_full.total_seconds() / 60))

                    if time_delta_minutes <= IGNORE_WRITE_TIME:
                        print(f'Song has not changed in {time_delta_minutes} minute(s). Ignoring write...')
                    else:
                        print('Song played today but not recently. Writing data...')
                        write_song(song_data, user_choice)

                else:  # If they aren't the same song (or it's been 15+ minutes), then write the data.
                    write_song(song_data, user_choice)

        # Repeat the while loop.
        time.sleep(SCRAPE_FREQUENCY)


def write_song(new_song_data, cur_station):
    with open('stations.json', 'r+') as song_file:
        temp_data_all = json.load(song_file)  # Grab all the json data
        temp_data_scoped = temp_data_all.get(f'{cur_station}')  # Grab the part we want to update
        temp_data_scoped.append(new_song_data)  # Write new data to the desired location
        temp_data_all.update({f'{cur_station}': temp_data_scoped})  # Reintegrate new data into json file

        # Grab the station metadata while the file is open
        metadata = temp_data_all.get(f'{cur_station}')[0]

        # Empty the file and write new data
        song_file.truncate(0)
        song_file.seek(0)
        json.dump(temp_data_all, song_file, indent=4, separators=(', ', ': '), ensure_ascii=False)
    print('Song written!')

    spotify_update(cur_station, metadata, new_song_data)


# TODO: Is this function redundant?
def spotify_update(dict_key, meta_dict, song_dict):
    spotapi.main(dict_key, meta_dict, song_dict)


if __name__ == "__main__":
    main()

# TODO: Spotify API stuff
# TODO: Run quietly in background
# TODO: Migrate code into functions
# TODO: Multithread for multiple stations at once?
