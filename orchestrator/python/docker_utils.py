from __future__ import print_function

import config


def serverList(client, all=False):
    '''
    serverList -> List running servers. Equivalent to
                  docker ps | grep $SERVER_BASE_IMAGE
    HINT: https://docker-py.readthedocs.io/en/stable/api.html#low-level-api
    '''
    # INSERT CODE HERE
    # HINT: User all=all kw argument in containers() function
    servers = None  # Replace this with the server list
    # TODO: Keep only the containers with c['Image'] = SERVER_BASE_IMAGE
    # INSERT CODE HERE
    return servers


def startServerContainer(client, serverID):
    '''
    startServerContainer -> Create & start a server container and return the IP
    Creates and starts a server container
    HINT: https://docker-py.readthedocs.io/en/stable/api.html#low-level-api
    '''
    # Create container configuration
    containerConfig = client.create_container_config(
        config.SERVER_BASE_IMAGE, command=None)
    containerConfig['Tty'] = True
    containerConfig['AttachStdin'] = True
    containerConfig['AttachStderr'] = False
    containerConfig['AttachStdout'] = False

    # TODO: Create container from given configuration
    # HINT use name='server-{0}'.format(serverID) in
    # create_container_from_config
    # This id is an increasing number that we set externally
    # and counts the number of booted servers
    newContainer = None  # Change this to create a new container

    newContainerID = newContainer['Id']
    print('Created container with ID = ' + str(newContainerID))
    # TODO: Start container with newContainerID

    # INSERT CODE HERE

    containers = serverList(client)

    # TODO: Search containers for container with Id == newContainerID
    newContainerJSON = None  # Replace this with the new container json
    # INSERT CODE HERE

    return extractContainerIP(newContainerJSON)


def removeServerContainer(client, containerID):
    '''
    removeServerContainer -> kill container instance using the containerID
    TODO: Remove container with containerID
    HINT: https://docker-py.readthedocs.io/en/stable/api.html#low-level-api
    HINT: Use force=True kwarg
    '''
    # INSERT CODE HERE
    pass


def containerFromServerID(client, serverID):
    '''
    ContainerFromServerID -> Get container with server ID
    '''
    serverName = '/server-{0}'.format(serverID)
    for server in serverList(client, all=True):
        if server['Names'][0] == serverName:
            return server
    return None


def runningServerCount(client):
    '''
    runningServerCount -> Get number of running servers
    '''
    return len(serverList(client))


def extractContainerIP(containerJSON):
    '''
    Get the IP of a running container from the container json
    '''
    return containerJSON['NetworkSettings']['Networks']['bridge']['IPAddress']
