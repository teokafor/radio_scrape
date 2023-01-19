# Radio Scraper
A tool used to scrape web-based radio stations for song data that can be stored to a .JSON file. With said data, the Spotify API is used to automatically build the user playlists based directly on those web stations.

# Instructions
To begin, you'll need to log in to your Spotify for Developers account (if you haven't already) and grab both tokens. Save those tokens in an environment variable and point your IDE to that file. (see spotapi.xml for an example.)

The song scraping feature itself does not require Spotify authentication.

---
Built in Python, with <a href="https://spotipy.readthedocs.io/en/2.22.0/"> SpotiPy,</a> and <a href="https://beautiful-soup-4.readthedocs.io/en/latest/">BeautifulSoup4.</a>
