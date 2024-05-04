# Introduction

This is a performance test using locust and docker to analise how this application perform with diferent configurations

the applications is from https://training.play-with-docker.com/microservice-orchestration/
## Try it out

```
$ docker-compose up --build

$ docker build -t my-locust-test . 
$ docker run -p 8089:8089 --network=link-extractor-teste-desempenho_default my-locust-test

```

Open http://localhost/?url=http%3A%2F%2Fodu.edu%2F in a web browser.

Press `Ctrl + C` to terminate the service.
