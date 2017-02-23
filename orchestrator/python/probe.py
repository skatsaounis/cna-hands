from __future__ import print_function

import requests


# RequestRateProbeURL -> /GET  #requests / sec
RequestRateProbeURL = 'http://127.0.0.1:5555/requestRate'


# ResponseRateProbeURL -> /GET #responses / sec
ResponseRateProbeURL = 'http://127.0.0.1:5555/responseRate'

# RequestCountProbeURL -> /GET #requests
RequestCountProbeURL = 'http://127.0.0.1:5555/numRequests'

# ResponseCountProbeURL -> /GET #responses
ResponseCountProbeURL = 'http://127.0.0.1:5555/numResponses'


# probeGet -> perform get request to probe server. Return rate or count value.
def probeGet(url):
    # TODO: Perform http get request in url, to get the current rate
    # HINT: http://docs.python-requests.org/en/master/

    s = requests.Session()
    s.trust_env = False

    # return rate as integer
    return int(float(s.get(url).text.strip()))


def getRequestRate():
    return probeGet(RequestRateProbeURL)


def getResponseRate():
    return probeGet(ResponseRateProbeURL)


def getRequestCount():
    return probeGet(RequestCountProbeURL)


def getResponseCount():
    return probeGet(ResponseCountProbeURL)
