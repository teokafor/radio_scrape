from bs4 import BeautifulSoup
import requests
from datetime import datetime
import csv

def main():
    # The URL to gather data from
    resource = requests.get("https://listen.klove.com/Christmas")

    # TODO: Make error reporting more verbose
    if resource.status_code != 200:  # This block will throw a generic error if the page cannot be returned for any reason.
        print("couldn't fetch page!")
        print('error code ' + resource.status_code)
        exit()
    else:  # If no error is found, proceed to scrape.

        # Grab and format data
        content = resource.content
        raw_data = BeautifulSoup(content, 'html.parser')

        # Collect necessary information
        song_title = raw_data.find(id='nowPlaying-title').string
        song_artist = raw_data.find(id='nowPlaying-artist').string
        scrape_time = datetime.now().strftime("%m-%d-%Y %I:%M %p")

        song_data = [song_title, song_artist, scrape_time]

        # Print output
        print(f'Song Title:  {song_data[0]}')
        print(f'Song Artist: {song_data[1]}')
        print(f'Scrape Time: {song_data[2]}')

        # Write contents to CSV file
        song_output = open('song_output.csv', 'a')
        writer = csv.writer(song_output, delimiter=',')
        writer.writerow(song_data)

    # Close the file when we are done with it
    song_output.close()

if __name__ == "__main__":
    main()

# TODO: Append to .CSV File
# TODO: Spotify API stuff
# TODO: Configurable settings (scrape freqeuncy, exclude dupes, timestamp output)
# TODO: Run quietly in background
