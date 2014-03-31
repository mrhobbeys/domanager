
import httplib, json

class DOHandler(object):
    def __init__(self):
        self._url = "api.digitalocean.com"
        self._clientId = "qLBGBATXxiEYFNA3JXMvr"
        self._apiKey = "c5d09dc0e5b22763d18a3ea76be6048b"

    def _request(self, method, request):
        request = request % (self._clientId, self._apiKey)
        conn = httplib.HTTPSConnection(self._url)
        conn.putrequest(method, request)
        conn.endheaders()
        response = conn.getresponse()
        return json.loads(response.read())

    def info(self):
        url = "/droplets/?client_id=%s&api_key=%s"
        return self._request("GET", url)

    def powerCycle(self, dropletId):
        url = "/droplets/%s/power_cycle/" % dropletId
        url += "?client_id=%s&api_key=%s"
        return self._request("GET", url)

    def powerOff(self, dropletId):
        url = "/droplets/%s/power_off/" % dropletId
        url += "?client_id=%s&api_key=%s"
        return self._request("GET", url)

    def powerOn(self, dropletId):
        url = "/droplets/%s/power_on/" % dropletId
        url += "?client_id=%s&api_key=%s"
        return self._request("GET", url)

    def resetRoot(self, dropletId):
        url = "/droplets/%s/password_reset/" % dropletId
        url += "?client_id=%s&api_key=%s"
        return self._request("GET", url)

    def destroy(self, dropletId):
        url = "/droplets/%s/destroy/" % dropletId
        url += "?client_id=%s&api_key=%s"
        return self._request("GET", url)