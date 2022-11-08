from bs4 import BeautifulSoup
import requests
from datetime import datetime

# The URL to gather data from
resource = requests.get("https://listen.klove.com/Christmas")

# TODO: Make error reporting more verbose
if resource.status_code != 200:  # This block will throw a generic error if the page cannot be returned for any reason.
    print("couldn't fetch page!")
    print('error code ' + resource.status_code)
    exit()
else:  # If no error is found, proceed to scrape.
    content = resource.content
    raw_data = BeautifulSoup(content, 'html.parser')
    song_title = raw_data.find(id='nowPlaying-title')
    song_artist = raw_data.find(id='nowPlaying-artist')
    scrape_time = datetime.now().strftime("%m-%d-%Y %I:%M %p")
    print(f'Song Title:  {song_title.string}')
    print(f'Song Artist: {song_artist.string}')
    print(f'Scrape Time: {scrape_time}')

# TODO: Append to .CSV File
# TODO: Spotify API stuff
# TODO: Configurable settings (scrape freqeuncy, exclude dupes, timestamp output)
# TODO: Run quietly in background
