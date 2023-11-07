import pandas as pd
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
client_id = '7fabac9d18954a5d9c386695f198e2dd'
client_secret = 'd04aa1f12b03457db4e6eab1937c75df'
redirect_uri = 'http://localhost:3000'

# Initialize the Spotify API client with a redirect URI
sp = Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))

# Read the CSV file and normalize column names
csv_file = 'spotify23.csv'
df = pd.read_csv(csv_file, encoding='utf-8')
df.columns = df.columns.str.strip().str.lower()

# Function to fetch album art URL for a specific track and artist
def get_album_art(track_name, artist_name):
    query = f"{track_name} artist:{artist_name}"
    results = sp.search(q=query, type='track', limit=1)

    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        if track['album']['images']:
            return track['album']['images'][0]['url']
    
    return None

# Create a new column 'Album Art' and populate it with album art URLs
df['album art'] = df.apply(lambda row: get_album_art(row['track name'], row['artist']), axis=1)

# Save the updated DataFrame to a new CSV file
updated_csv_file = 'spotify23_with_album_art.csv'
df.to_csv(updated_csv_file, index=False)

print(f'Album art URLs saved to {updated_csv_file}')
