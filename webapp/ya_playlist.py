from yandex_music import Client


def get_playlist(url):
    user_name = url.split('/')[4]
    id_playlist = url.split('/')[-1]
    playlist_list = Client().users_playlists(int(id_playlist), user_name)
    # playlist_json = playlist_list.to_json()
    return playlist_list['tracks']


f = get_playlist('https://music.yandex.ru/users/shamantur116/playlists/1001')


name_tracks = []
for i in f:
    name_tracks.append(getattr(i.fetch_track(), 'title'))

artists_tracks = []
for i in f:
    list_artist = getattr(i.fetch_track(), 'artists')
    artists_tracks.append(getattr(list_artist[0], 'name'))

duration_tracks = []
for i in f:
    duration_ms = getattr(i.fetch_track(), 'duration_ms')
    duration_min = duration_ms * 0.000017
    duration_tracks.append(f'{duration_min:.0f}:{str(duration_min)[2:4]}')
