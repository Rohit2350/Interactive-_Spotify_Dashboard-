import pandas as pd
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
client_id = '7fabac9d18954a5d9c386695f198e2dd'
client_secret = 'd04aa1f12b03457db4e6eab1937c75df'
redirect_uri = 'http://localhost:3000'  # Specify a redirect URI here

# Initialize the Spotify API client with a redirect URI
sp = Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))

# Read the CSV file
csv_file = 'spotify23.csv'
try:
    df = pd.read_csv(csv_file, encoding='utf-8')
except UnicodeDecodeError:
    # If 'utf-8' doesn't work, try other encodings
    df = pd.read_csv(csv_file, encoding='ISO-8859-1')  # or 'latin1'

# Function to fetch album art URLs
def get_album_art(artist, album):
    results = sp.search(q=f'album:{album} artist:{artist}', type='album')
    if results['albums']['items']:
        album_data = results['albums']['items'][0]
        return album_data['images'][0]['url']
    return None

# Create a new column 'Album Art' and populate it with album art URLs
df['Album Art'] = df.apply(lambda row: get_album_art(row['Artist'], row['Album']), axis=1)

# Save the updated DataFrame to a new CSV file
updated_csv_file = 'spotify23_with_album_art.csv'
df.to_csv(updated_csv_file, index=False)

print(f'Album art URLs saved to {updated_csv_file}')
