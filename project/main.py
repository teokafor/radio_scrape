from bs4 import BeautifulSoup
import requests

resource = requests.get("https://listen.klove.com/Christmas")

if resource.status_code != 200:
    print("couldn't fetch page!")
    print('error code ' + resource.status_code)
    exit()
else:
    content = resource.content
    soup = BeautifulSoup(content, 'html.parser')
    song_title = soup.find(id='nowPlaying-title')
    song_artist = soup.find(id='nowPlaying-artist')
    print(song_title.string)
    print(song_artist.string)


#TODO: Append to .CSV File
#TODO: Spotify API stuff
#TODO: Configurable settings (freqeuncy, exclude dupes,
