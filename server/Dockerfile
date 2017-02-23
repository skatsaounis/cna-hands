FROM  golang:latest

RUN go get golang.org/x/net/netutil 
RUN mkdir /code
ADD main.go /code/server.go

VOLUME /code
CMD go run /code/server.go
