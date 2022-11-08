from bs4 import BeautifulSoup
import requests

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
    print(song_title.string)
    print(song_artist.string)


#TODO: Append to .CSV File
#TODO: Spotify API stuff
#TODO: Configurable settings (freqeuncy, exclude dupes,
