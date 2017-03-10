from __future__ import print_function

import requests
import json


# createGorbService -> create a Gorb service
def createGorbService(gorbIP, serviceID, serviceIP, servicePort):
    """
    Example:
    curl -i \
         -X PUT \
         -H "Content-Type: application/json" \
         -d '{ "host":"10.0.2.15", \
               "port":4444, \
               "protocol":"tcp", \
               "method":"rr", \
               "persistent": true}' \
         http://10.0.2.15:4672/service/0
    """
    s = requests.Session()
    s.trust_env = False

    url = 'http://{0}:4672/service/{1}'.format(gorbIP, serviceID)
    payload = {
        'host': serviceIP,
        'port': servicePort,
        'protocol': 'tcp',
        'method': 'rr',
        'persistent': True
    }

    headers = {'Content-Type': 'application/json'}

    resp = s.put(url, data=json.dumps(payload), headers=headers)

    print('Response status: {0}'.format(resp.status_code))
    if resp.status_code > 299:
        print('Something went wrong with the request')

    print('Response body'.format(resp.content))

    return resp


# registerServerToGorb -> Register a newly created server to gorb
def registerServerToGorb(gorbIP, serviceID, serverID, serverIP, serverPort):
    """
    Example:
    curl -i \
         -X PUT \
         -H "Content-Type: application/json" \
         -d '{ "host":"172.17.0.3", \
               "port":4444, \
               "method":"nat", \
               "weight":100 }' \
         http://10.0.2.15:4672/service/0/1
    """
    s = requests.Session()
    s.trust_env = False

    url = 'http://{0}:4672/service/{1}/{2}'.format(gorbIP, serviceID, serverID)
    payload = {
        'host': serverIP,
        'port': serverPort,
        'method': 'nat',
        'weight': 100
    }

    headers = {'Content-Type': 'application/json'}

    resp = s.put(url, data=json.dumps(payload), headers=headers)

    print('Response status: {0}'.format(resp.status_code))
    if resp.status_code > 299:
        print('Something went wrong with the request')

    print('Response body'.format(resp.content))

    return resp


# unRegisterServerFromGorb -> Remove server from gorb service
def unRegisterServerFromGorb(gorbIP, serviceID, serverIP):
    """
    Example:
    curl -i \
         -X DELETE \
         http://10.0.2.15:4672/service/0/1
    """
    s = requests.Session()
    s.trust_env = False

    gorbUrl = 'http://{0}:4672/service'.format(gorbIP)

    # search for backend with ip == serverIP
    service = s.get('{0}/{1}'.format(gorbUrl, serviceID))
    backends = service.json()['backends']

    backendID = -1
    for bID in backends:
        backend = s.get('{0}/{1}/{2}'.format(gorbUrl, serviceID, bID))
        if 'options' in backend.json().keys():
            if backend.json()['options']['host'] == serverIP:
                backendID = bID
                break

    if backendID == -1:
        print("Backend with {0} not found".format(serverIP))
        return None

    url = '{0}/{1}/{2}'.format(gorbUrl, serviceID, backendID)
    resp = s.delete(url)

    print('Response status: {0}'.format(resp.status_code))
    if resp.status_code > 299:
        print('Something went wrong with the request')

    print('Response body'.format(resp.content))
    return resp


if __name__ == '__main__':
    createGorbService('10.0.2.15', 0, '10.0.2.15', 4444)
    registerServerToGorb('10.0.2.15', 0, 0, '172.17.0.2', 4444)
