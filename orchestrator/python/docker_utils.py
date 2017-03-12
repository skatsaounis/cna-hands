from __future__ import print_function

import config


# serverList -> List running servers
def serverList(client, all=False):
    containers = client.containers(all=all)
    # Keep only the containers booted with SERVER_BASE_IMAGE
    servers = [c
               for c in containers
               if c['Image'] == config.SERVER_BASE_IMAGE]
    return servers


# startServerContainer -> Create and start a server container and return the IP
def startServerContainer(client, serverID):
    containerConfig = client.create_container_config(
        config.SERVER_BASE_IMAGE, '')
    containerConfig['Tty'] = True
    containerConfig['AttachStdin'] = True
    containerConfig['AttachStderr'] = False
    containerConfig['AttachStdout'] = False

    newContainer = client.create_container_from_config(
        containerConfig, name='server-{0}'.format(serverID))
    newContainerID = newContainer['Id']
    print('Created container with ID = ' + str(newContainerID))
    client.start(newContainerID)

    containers = serverList(client)
    newContainerJSON = next(c for c in containers if c['Id'] == newContainerID)
    return extractContainerIP(newContainerJSON)


# removeServerContainer -> kill container instance using the serverID
# managed by the orchestrator
def removeServerContainer(client, serverID):
    containerID = containerIDFromServerID(client, serverID)
    client.remove_container(containerID, force=True)


# ContainerIDFromServerID -> Convert server ID to container ID
def containerIDFromServerID(client, serverID):
    serverName = '/server-{0}'.format(serverID)
    for server in serverList(client, all=True):
        if server['Names'][0] == serverName:
            return server['Id']
    return None


# runningServerCount -> Get number of running servers
def runningServerCount(client):
    return len(serverList(client))


def extractContainerIP(containerJSON):
    return containerJSON['NetworkSettings']['Networks']['bridge']['IPAddress']
