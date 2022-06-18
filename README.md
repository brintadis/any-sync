# Any-Sync

Сервис для синхронизации и бэкапа плейлистов и треков из различных музыкальных сервисов.
С помощью библиотек([spotipy](https://github.com/plamere/spotipy), [yandex-music-api](https://github.com/MarshalX/yandex-music-api)) получаем данные по трекам и отправляем их в БД, затем есть возможность сохранить плейлист в файле или синхронизировать его на другом музыкальном сервисе.

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
Для инициализации базы данных запустите из корня проекта файл:
```
create_db.py
```

Для запуска сервера в терминале нужно указать путь к flask проекту:

Linux и Mac: 
```
export FLASK_APP=webapp && export FLASK_ENV=development && flask run
```
Windows: 
```
set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run
```