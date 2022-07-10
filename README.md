# Any-Sync

Сервис для синхронизации и бэкапа плейлистов и треков из различных музыкальных сервисов.
С помощью библиотек ([spotipy](https://github.com/plamere/spotipy), [yandex-music-api](https://github.com/MarshalX/yandex-music-api)) получаем данные по трекам и отправляем их в БД, затем есть возможность синхронизировать его на другом музыкальном сервисе.

## Поддерживаемые музыкальные сервисы

- Spotify
- Yandex-Music
- в разработке Apple Music

## Сборка репозитория и локальный запуск
Скачайте проект с github:

```
git clone https://github.com/brintadis/any-sync.git
```

Создайте виртуальное окружение и установите зависимости:
```
pip install -r requirments.txt
```

В файле webapp/config.py укажите ключ проекта:
```
SECRET_KEY = ""
```

## Запуск проекта
Для корректной работы Spotify, нужно установить зависимости, предварительно создав приложение в [Spotify Dashboard](https://developer.spotify.com/dashboard/).

<img src= "https://imgur.com/hzTnqk6.png" width = "480" height = "360">

На этой странице вам необходимо указать Redirect URIs и точно такой же redirect указать в файле ```webapp/spotify/spotify.py``` в переменной ```REDIRECT_URI```. На этой же странице, вы получаете ```Client ID``` и ```Client Secret``` своего Spotify приложения и устанавливаете зависимости ниже.

Linux и Mac:
```
export SPOTIFY_CLIENT_ID="Your Spotify App Client ID"
export SPOTIFY_CLIENT_SECRET="Your Spotify App Client Secret"
```
Windows:
```
set SPOTIFY_CLIENT_ID="Your Spotify App Client ID"
set SPOTIFY_CLIENT_SECRET="Your Spotify App Client Secret"
```
### Инициализация Базы данных
Для инициализации базы данных запустите из корня проекта файл:
```
create_db.py
```
### Запуск сервера
Для запуска сервера в терминале нужно указать путь к flask проекту:

Linux и Mac: 
```
export FLASK_APP=webapp && export FLASK_ENV=development && flask run
```
Windows: 
```
set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run
```