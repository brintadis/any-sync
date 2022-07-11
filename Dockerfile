# Выкачиваем из dockerhub образ с python версии 3.9
FROM python:3.9
# Устанавливаем рабочую директорию для проекта в контейнере
WORKDIR /backend
ENV SPOTIFY_CLIENT_ID=05aecee3d14b494d89ee2fcf8faede62
ENV SPOTIFY_CLIENT_SECRET=b28942419390419881759ed6ccc7e2cc

# Скачиваем/обновляем необходимые библиотеки для проекта 
COPY requirements.txt /backend
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# |ВАЖНЫЙ МОМЕНТ| копируем содержимое папки, где находится Dockerfile, 
# в рабочую директорию контейнера
COPY . /backend
# RUN python3 create_db.py

CMD [ "python3", "webapp" "run"]
