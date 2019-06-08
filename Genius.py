import requests
from bs4 import BeautifulSoup
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, USLT
from mutagen.mp3 import MP3, EasyMP3
from mutagen.mp4 import MP4
import re
import os

dic = {'title': '\xa9nam', 'artist': '\xa9ART', 'lyrics': '\xa9lyr'}


def get_token():
    f = open("token.txt", "r")
    t = f.read()
    f.close()
    return t


def get_song_path_list(path):
    song_list = []
    for filename in os.listdir(path):
        if filename.endswith('.m4a') or filename.endswith('.mp4'):
            song_list.append(filename)
    return song_list


def request_song_info(song_title, artist_name):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + get_token()}
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(search_url, data=data, headers=headers)

    return response


def find_song_url(response, artist_name, song_title):
    json = response.json()
    remote_song_info = None
    for hit in json['response']['hits']:
        found_title = hit['result']['title'].lower()
        found_artist = hit['result']['primary_artist']['name'].lower()
        if artist_name.lower() in found_artist and song_title.lower() in found_title:
            remote_song_info = hit
            break
    if remote_song_info:
        return remote_song_info['result']['url']
    return None


def crawl_for_lyrics(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()
    lyrics = re.sub('(\[.*?\])*', '', lyrics)
    lyrics = re.sub('\n{2}', '\n', lyrics)
    return lyrics


def insert_lyrics(song, lyrics):
    song[dic['lyrics']] = lyrics
    # tags = ID3(song)
    # tags[u"USLT::'eng'"] = USLT(lyrics)
    # tags.save(song)
    song.save()


def lyrics_to_songs(folder_path):
    song_paths = get_song_path_list(folder_path)
    error_list = []
    total_in_folder = len(song_paths)
    done_well = 0
    done_bad = 0
    cnt = 0

    for path in song_paths:
        cnt += 1
        full_path = folder_path + '\\' + path
        song = MP4(full_path)
        song_title, song_artist = song[dic['title']][0], song[dic['artist']][0]

        song_resposne = request_song_info(song_title, song_artist)
        song_url = find_song_url(song_resposne, song_artist, song_title)
        if song_url:
            lyrics = crawl_for_lyrics(song_url).strip()
            insert_lyrics(song, lyrics)
            done_well += 1
            print('Y', cnt, ':', total_in_folder)
        else:
            error_list.append(song_title)
            done_bad += 1
            print('N', cnt, '/', total_in_folder)

    if done_bad > 0:
        print(folder_path, error_list)



