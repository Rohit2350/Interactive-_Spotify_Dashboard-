import requests
import pandas as pd

# Function to get a Spotify access token
def get_spotify_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    auth_data = auth_response.json()
    return auth_data['access_token']

# Function to search for a track and get its ID
def search_track(track_name, artist_name, token):
    query = f"{track_name} artist:{artist_name}"
    url = f"https://api.spotify.com/v1/search?q={query}&type=track"
    response = requests.get(url, headers={'Authorization': f'Bearer {token}'})
    json_data = response.json()
    try:
        first_result = json_data['tracks']['items'][0]
        track_id = first_result['id']
        return track_id
    except (KeyError, IndexError):
        return None

# Function to get track details
def get_track_details(track_id, token):
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    response = requests.get(url, headers={'Authorization': f'Bearer {token}'})
    json_data = response.json()
    image_url = json_data['album']['images'][0]['url']
    return image_url

# Your Spotify API Credentials
client_id = '7fabac9d18954a5d9c386695f198e2dd'
client_secret = 'd04aa1f12b03457db4e6eab1937c75df'

# Get an Access Token
access_token = get_spotify_token(client_id, client_secret)

# Read your DataFrame from a CSV file
df_spotify = pd.read_csv('spotify233.csv', encoding='ISO-8859-1')

# Loop through each row to get track details and add to DataFrame
for index, row in df_spotify.iterrows():
    track_id = search_track(row['track_name'], row['artist_name'], access_token)
    if track_id:
        image_url = get_track_details(track_id, access_token)
        df_spotify.at[index, 'image_url'] = image_url

# Save the updated DataFrame to a new CSV file
df_spotify.to_csv('updated_file.csv', index=False)

