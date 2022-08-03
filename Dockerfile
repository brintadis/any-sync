# Выкачиваем из dockerhub образ с python версии 3.9
FROM python:3.9
# Устанавливаем рабочую директорию для проекта в контейнере
WORKDIR /backend
ENV SPOTIFY_CLIENT_ID='Your Spotify App Client ID'
ENV SPOTIFY_CLIENT_SECRET='Your Spotify App Client Secret'

# Скачиваем/обновляем необходимые библиотеки для проекта 
COPY requirements.txt /backend
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
#     && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
# RUN apt-get update && apt-get -y install google-chrome-stable

# |ВАЖНЫЙ МОМЕНТ| копируем содержимое папки, где находится Dockerfile, 
# в рабочую директорию контейнера
COPY . /backend

CMD [ "python3", "webapp" "run"]
