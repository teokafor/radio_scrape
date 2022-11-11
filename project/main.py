import os
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import csv

SCRAPE_FREQUENCY = 30  # The time (in seconds) that the website should be checked.
IGNORE_WRITE_TIME = 15  # If songs found are the same as the last entry and are under this value, then ignore write.


def main():
    # The URL to gather data from
    resource = requests.get("https://listen.klove.com/Christmas")

    # TODO: Make error reporting more verbose
    if resource.status_code != 200:  # Throw an error if the page cannot be returned for any reason.
        print("couldn't fetch page!")
        print(f'error code f{resource.status_code}')
        exit()
    else:  # If no error is found, proceed to scrape.



        #while True:  # Loop until the program is closed

        # Grab and format data
        content = resource.content
        raw_data = BeautifulSoup(content, 'html.parser')

        # Collect necessary information
        song_title = raw_data.find(id='nowPlaying-title').string
        song_artist = raw_data.find(id='nowPlaying-artist').string
        scrape_date = datetime.now().strftime("%m-%d-%Y")

        time_format = "%H:%M"
        scrape_time = datetime.now().strftime(time_format)

        song_data = [song_title, song_artist, scrape_date, scrape_time]

        # Print output
        #print(f'Song Title:  {song_data[0]}')
        #print(f'Song Artist: {song_data[1]}')
        #print(f'Scrape Date: {song_data[2]}')
        #print(f'Scrape Time: {song_data[3]}')

        # Write contents to CSV file
        with open('song_output.csv', 'r+', newline='') as song_output:  # Open for reading and appending
            writer = csv.writer(song_output, delimiter=',')
            reader = csv.reader(song_output, delimiter=',')

            # Prevent the same song from being written to the file within a given timespan (e.g., 15 minutes)
            try:

                # First check if the CSV file is empty
                if os.stat('song_output.csv').st_size == 0:
                    print("DEBUG: empty CSV file detected! Writing header data...")
                    writer.writerow(['TITLE: ', 'ARTIST: ', 'TIMESTAMP:'])
                else:
                    print("CSV file has data.")

                for line in reader:  # Jump to the last line
                    last_line = line
                # If it's the same song, by the same artist, on the same day, then compare times
                if last_line[0] == song_data[0] and last_line[1] == song_data[1] and last_line[2] == song_data[2]:

                    print('Similar song found!')

                    # Format date strings into datetime objects
                    current_song_time = datetime.strptime(song_data[3], time_format)
                    last_song_time = datetime.strptime(last_line[3], time_format)

                    # Compare times to see if it's a duplicate
                    time_delta_full = current_song_time - last_song_time
                    time_delta_minutes = (int(time_delta_full.total_seconds() / 60))

                    if time_delta_minutes <= IGNORE_WRITE_TIME:
                        print(f'Song has not changed in {time_delta_minutes} minute(s). Ignoring write...')
                    else:
                        print('Song played today but not recently. Writing data...')
                        writer.writerow(song_data)

                else:  # If they aren't the same song (or it's been 15+ minutes), then write the data.
                    writer.writerow(song_data)
                    print('Song written!')
            except UnboundLocalError:  # If no data exists, then no preventative action is needed
                pass

            # TODO: Close file here so next loop it can actually read from it
            # TODO: If not, you could store the data in a list variable, then do one mass write at the end
            # TODO: If you choose that route, then you need to ensure that the data isn't accidentally lost!
            #time.sleep(SCRAPE_FREQUENCY)


if __name__ == "__main__":
    main()

# TODO: Spotify API stuff
# TODO: Configurable settings (scrape freqeuncy, exclude dupes, timestamp output)
# TODO: Run quietly in background
# TODO: Fix weird accent marks in output (e.g., feliz navidad)
