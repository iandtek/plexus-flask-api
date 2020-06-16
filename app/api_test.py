from googleapiclient.discovery import build
from pprint import pprint
import json

API_KEY = 'AIzaSyBcaYzKl8KLwEA0pp-e6X4oQvoz0cXkhSQ'
youtube = build('youtube', 'v3', developerKey=API_KEY)


def get_playlists():
    request = youtube.playlists().list(
        part="snippet",
        channelId="UCp0Kd665CtievA0ss105ujA"
    )
    return request.execute()


def get_playlist_videos(id, pageToken=''):
    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=50,
        playlistId=id,
        pageToken=pageToken
    )
    response = request.execute()
    videos = response['items']
    if('nextPageToken' in response):
        videos = videos + get_playlist_videos(id, response['nextPageToken'])
    return videos


def data():
    playlists = get_playlists()
    for playlist in playlists['items']:
        playlist['videos'] = get_playlist_videos(playlist['id'])
    return playlists


def save_data():
    json.dump(data(), open('plexus.json', 'wb'))


save_data()
