# Building an elastic cloud orchestrator

In the previous hands-on sections we have become familiar with docker and Gorb load balancer and we have implemented a set of docker utilities in Python.

In this section we'll see how we can make use of these technologies to implement an elastic orchestrator for our cloud application. The job of the orchestrator is to observe the ingress and egress traffic (requests) in and from our servers and estimate how many servers need to be created and destroyed to minimize lost requests.

## Code structure

| Path                                             | Description                                     |
|--------------------------------------------------|-------------------------------------------------|
| `orchestractor/python/config.py`                 | Some configuration constants for the orchestrator |
| `orchestractor/python/docker_utils.py`           | Utilities to create and destroy docker containers |
| `orchestractor/python/gorb.py`                   | Utilities to register and unregister gorb servers  |
| `orchestractor/python/main.py`                   | The main logic of the orchestrator |
| `orchestractor/python/probe.py`                  | A probe to get some metrics about the current app performance |
| `client-deterministic/main.go`                   | A client with a predefined traffic pattern |
| `client/main.go`                                 | A client with a random traffic pattern |
| `cleanup.sh`                                     | Destroy leftover containers |
| `run.sh`                                         | Run the CNA, the client and the orchestrator |

## Part 1: Test `run.sh` and `cleanup.sh`

- Inspect the code of these scripts
- Run `run.sh`  
- Run `cleanup.sh`   

## Part 2: Implement scale up and scale down logic

The first task is to provide an efficient implementation for the scale{Up,Down} functions defined in `orchestrator/python/main.py`. These functions take a number `n` and have to create / destroy `n` servers accordingly. We recommend to use a concurrent implementation for these functions (simplest done using `threading`).

## Part 3: Orchestration algorithm

Now we have all the pieces in place to implement our orchestration logic. The function we need to implement is `serversNeededHeuristic`, which takes a set of metrics (like `{request,response}Rate`) and returns a number `n`, the number of servers needed to be created or destroyed. As the name suggests `n` is estimated heuristically, so there's no single optimal solution.

This function is used in the main loop of the orchestrator, which is described below:

1. Update metrics values (`{request,response}{Count,Rate}`, `runningServerCount`)
2. Calculate `n = serversNeededHeuristic(metrics)`
3. `if n>0: scaleUp(n)`, else `if n<0: scaleDown(n)`
4. Update `currentServerID`

