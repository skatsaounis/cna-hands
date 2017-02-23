from __future__ import print_function

import config
import docker
import docker_utils
import gorb
import probe
import threading
import time


def serversNeededHeuristic(
        requestRate, responseRate,
        requestCount, responseCount,
        currentServerCount):
    '''
    Use one or more of the {request,response}{Rate,Count} and
    currentServerCount metrics to calculate a heuristic for
    the number of servers that need to be created / destroyed.
    The target is to minimized the number of unprocessed requests
    using the minimum number of servers (booting 1000000 servers
    is not considered a good solution).

    YOU DON'T NEED TO USE ALL THE METRICS. They are provided
    as parameters for ease of use

    needed == 0: No servers will be created or destroyed
    needed > 0 : Create #needed servers
    needed < 0 : Destroy #needed servers
    '''
    needed = 0
    return needed


def scaleUp(n, currentServerID):
    '''
    ScaleUp boots #n servers starting from currentServerID
    The procedure to boot one server is:
        1. Increment currentServerID
        2. Start docker container with currentServerID
        3. Register server to gorb (GORB_IP, SERVICE_ID &
           SERVICE_PORT are provided in config.py)
    We recommend to boot the #n servers concurrently using
    the threading library
    '''
    pass


def scaleDown(n, nextServerID):
    '''
    ScaleDown destroys #n servers starting from currentServerID
    The procedure to boot destroy a server is:
        1. Use docker_utils.containerIDFromServerID function
           to find the container with currentServerID
        2. Remove the container you found
        3. Unregister server from gorb (GORB_IP, SERVICE_ID &
           SERVICE_PORT are provided in config.py)
        4. Decrement currentServerID
    We recommend to remove the #n servers concurrently using
    the threading library
    '''
    pass


if __name__ == '__main__':
    client = docker.from_env()  # This is your docker client
    print("Got docker client {0}".format(client))

    # Assume gorb running and one server registered
    currentServerID = 0

    while True:
        requestRate = probe.getRequestRate()
        responseRate = probe.getResponseRate()
        requestCount = probe.getRequestCount()
        responseCount = probe.getResponseCount()
        currentServerCount = (docker_utils
                              .runningServerCount(client))

        print("Request rate: %s" % requestRate)
        print("Response rate: %s" % responseRate)
        print("Request count: %s" % requestCount)
        print("Response count: %s" % responseCount)
        print("Current server count: %s" % currentServerCount)

        serversNeeded = serversNeededHeuristic(
            requestRate, responseRate,
            requestCount, responseCount,
            currentServerCount)
        print("Servers needed %s " % serversNeeded)

        if serversNeeded > 0:
            scaleUp(abs(serversNeeded), currentServerID)
        elif serversNeeded < 0:
            scaleDown(abs(serversNeeded), currentServerID)
        else:
            pass

        currentServerID += serversNeeded
        time.sleep(1)
