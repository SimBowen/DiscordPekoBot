from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
load_dotenv()


S_ID = os.getenv('CLIENT_ID')
S_SECRET = os.getenv('CLIENT_SECRET')

""" Loading spotipy API """
client_credentials_manager = SpotifyClientCredentials(client_id=S_ID, client_secret=S_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

""" Parse spotify linnks and return a list of youtube searchable terms """
def spotify_parsing(url):
    URIs = parse_URI(url)
    yt_queries = []
    for song in URIs:
        yt_queries.append(getYTQuery(song))
    return yt_queries

""" Parse spotify links and get a list of spotify URIs """
def parse_URI(url):
    URIs = []
    if 'playlist' in url:
        id = url[0:url.index("?")].replace("open.spotify.com/playlist/","").replace("https://","")
        """ Maximum number of tracks """
        ids = getTrackIDs('Novalty', id, 15)
        URIs.extend(ids)
    else:
        id = url[0:url.index("?")].replace("open.spotify.com/track/","").replace("https://","")
        URIs.append(id)
    return URIs
    
""" Get the list of track URIs from playlist id """
def getTrackIDs(user, playlist_id, max_songs):
    ids = []
    playlist = sp.user_playlist(user, playlist_id)
    counter = 0
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
        counter+=1
        if counter == max_songs:
            break
    return ids

""" Convert spotify meta data into yt search terms """
def getYTQuery(id):
  meta = sp.track(id)
  features = sp.audio_features(id)
  # metadata
  name = meta['name']
  album = meta['album']['name']
  artist = meta['album']['artists'][0]['name']
  release_date = meta['album']['release_date']
  length = meta['duration_ms']
  yt_query = name + " by " + artist
  return yt_query
