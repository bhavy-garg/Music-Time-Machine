from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os

# ------------------------------ SETTING ENVIRONMENT VARIABLES ------------------------------------------------
# Set environment variables
# os.environ['SPOTIPY_CLIENT_ID'] = '010947403e2544a8bc905882553fcc75'
# os.environ['SPOTIPY_CLIENT_SECRET'] = '3a76a231bf47413f8e7cff10b0ae3d22'
#
# # Get environment variables
# ID = os.getenv('SPOTIPY_CLIENT_ID')
# SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')

# ------------------------------------- WEB SCRAPING FROM THE BILLBOARDS WEBSITE -----------------------------------
URl = 'https://www.billboard.com/charts/hot-100'

user_input = input('Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ')
response = requests.get(f'{URl}/{user_input}')
website_html = response.text

soup = BeautifulSoup(website_html, 'html.parser')
# print(soup.prettify())
songs_list = []
# all_songs = soup.find_all(name='h3', id='title-of-a-story')
all_songs = soup.select(selector="li #title-of-a-story")
for song in all_songs:
    songs_list.append(song.getText().strip())

# ---------------------------------------- API OF SPOTIFY -----------------------------------------------------

# print(songs_list)
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id='010947403e2544a8bc905882553fcc75',
        client_secret='3a76a231bf47413f8e7cff10b0ae3d22',
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
# 31l5qxnvovt5x72mdfib2itp76uy
# print(user_id)

# -------------------------------------- EXTRACTING SONG URLS FROM SPOTIFY ----------------------------------------
song_urls = []
year = user_input.split("-")[0]
for song in songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        url = result["tracks"]["items"][0]["uri"]
        song_urls.append(url)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# print(song_urls)

# --------------------------- CREATING PRIVATE PLAYLIST IN SPOTIFY ---------------------------------------------

playlist = sp.user_playlist_create(user=user_id, name=f"{user_input} Billboard 100", public=False)
# print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_urls)