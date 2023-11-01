docker build . -t np-api-image

docker container rm -f np-api

docker container run -d --name np-api --publish 5000:5000 np-api-image