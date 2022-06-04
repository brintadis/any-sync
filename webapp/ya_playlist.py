from yandex_music import Client
from settings import token


def get_playlist(url):
    user_name = url.split('/')[4] 
    id_playlist = url.split('/')[-1]
    playlist_list = Client().users_playlists(int(id_playlist), user_name)
    return playlist_list['tracks']
    

print(get_playlist('https://music.yandex.ru/users/shamantur116/playlists/1009'))    
