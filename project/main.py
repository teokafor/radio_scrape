import time
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json
import os

SCRAPE_FREQUENCY = 120  # The time (in seconds) that the website should be checked.
IGNORE_WRITE_TIME = 25  # If songs found are the same as the last entry and are under this value, then ignore write.
TIME_FORMAT = "%H:%M"  # Used to format (and un-format) time data.


def main():
    while True:  # Loop until the program is closed

        # Ask the user for the name of the radio station (used for Spotify playlist labeling)
        # TODO: Check local file for names of preexisting stations and show that list first
        # TODO: Wrap in try/except for special characters, as the OS won't like those.
        station_name = input("Enter the radio station's name: ")
        print(station_name)

        # The URL to gather data from
        resource = requests.get("https://listen.klove.com/Christmas")

        if resource.status_code != 200:  # Throw an error if the page cannot be returned for any reason.
            print("couldn't fetch page!")
            print(f'error code f{resource.status_code}')
            exit()

        # Grab and format data
        content = resource.content
        raw_data = BeautifulSoup(content.decode('utf-8'), 'html.parser')

        # Collect necessary information
        song_title = raw_data.find(id='nowPlaying-title').string
        song_artist = raw_data.find(id='nowPlaying-artist').string
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
        if not (os.path.isfile(f'{station_name}.json')) or os.stat(f'{station_name}.json').st_size == 0:
            with open(f'{station_name}.json', 'w') as song_file:
                song_file.write('[]')

        # Read contents from JSON file
        with open(f'{station_name}.json') as song_file:
            # Load the JSON data into a list
            temp_list = json.load(song_file)

            # Grab the latest dict entry in the list
            try:
                last_dict_item = next(reversed(temp_list))
            except StopIteration:
                print("the file is empty, so dont worry about comparing songs")

                # Write first song to file
                write_song(temp_list, song_data, station_name)
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
                        write_song(temp_list, song_data, station_name)

                else:  # If they aren't the same song (or it's been 15+ minutes), then write the data.
                    write_song(temp_list, song_data, station_name)

        time.sleep(SCRAPE_FREQUENCY)


def write_song(cur_list, new_song_data, station_name):
    cur_list.append(new_song_data)
    with open(f'{station_name}.json', 'w') as song_file:
        json.dump(cur_list, song_file, indent=4, separators=(', ', ': '), ensure_ascii=False)
    print('Song written!')


if __name__ == "__main__":
    main()

# TODO: Spotify API stuff
# TODO: Run quietly in background
# TODO: Add command line functionality (help, config settings)
# TODO: Migrate code into functions
# TODO: Multithread for multiple stations at once?
