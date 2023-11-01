docker build . -t np-telegram-bot-image

docker container rm -f np-telegram-bot

docker container run -d --name np-telegram-bot np-telegram-bot-image