# The Docker container engine: Hands on

- First clone the `cna-code` repo from github

```
git clone http://github.com/intracom-telecom-sdn/cna-code.git
cd cna-code
```

The first component of our cloud native application is a basic HTTP server 
implemented in `server/main.go`. 

This server exposes 2 REST endpoints
- `/doWork`: The server handles an incoming request to do a unit of work
- `/stop`: The server exits.

## (Part 1/3): Deploy server instance on baremetal

1. Run server application  

   ```
   go run server/main.go
   ```
2. Perform a GET request using CURL and observe the result  

   ```
   curl -X GET http://localhost:4444/doWork
   ```
3. Try to run a second server on baremetal. You should get an `Address already in use`
   error. You can bypass this by making the user specify the port, but what 
   about other resources? (config files, log files, system side effects)
   
   CHECK: I don't get an `Address already in use` error, but rather a goroutine panic 
   from the second server. 
   
4. Now stop the server  

   ```
   curl -X GET http://localhost:4444/stop
   ```
   
## (Part 2/3): Deploy server instance with docker

1. Open `server/Dockerfile`. This file is a template for a docker image to 
   deploy and run our server application.
   
   CHECK: shouldn't we have the 4444 port exposed in the Dockerfile (`EXPOSE 4444`)? it would be 
   good to demonstrate how containers expose ports, so that you can reach them, 
   both through the "backdoor" of internal IP addresses, but also through the "frontdoor" of 
   exposed ports.
   
2. Build the server image with  

   ```
   docker build -t cna-server:latest server/
   ```
3. Verify `cna-server` image exists with  

   ```
   docker images
   ```
4. Deploy a server instance container using `cna-server:latest` image  

   ```
   docker run -ti --name server1 cna-server:latest
   ```
   
   CHECK: here, we could add -p 8000:4444, and later -p 8001:4444 for the second container, 
   so that we can hit the localhost directly
   
5. Verify container is up  

   ```
   docker ps
   ```
6. Inspect `server1` container. Search for IPAddress field to get the server IP  

   ```
   docker inspect server1
   ```
7. Make `server1` do some work with CURL (don't `/stop` the server)

   CHECK: in this step we would hit the exposed ports 
   
8. Repeat steps 4-7 to create and test a new server instance named `server2`
9. Delete `server2` instance  

   ```
   docker rm -f server2
   ```
   
## (Part 3/3): Call Docker API programmatically

Here we'll learn how to interact programmatically with Docker. This is the first 
step towards building an orchestrator that will provide some elasticity to our 
application. 

We provide the boilerplate code in Go and Python. We'll follow the Python 
implementation, but you can try Go too if you feel confident.

CHECK: better remove the Go part here? (or mention it at the end, like: 
We provide the boilerplate code in Python. (if you feel confident, we also
provide a Go boilerplate to work on)


We'll give you ~20 minutes for the coding part. Implement the functions in
`orchestrator/python/docker_utils.py`.


## Conclusions

- We deployed and tested an application on baremetal. Does the trick, but 
  somewhat inflexible.
- We deployed and tested the same application using Docker. We saw that Docker 
  streamlines the deployment and destruction of application and makes it 100% 
  reproduciple.
