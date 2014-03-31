
import httplib, json
from domanager.config import config

class DOHandler(object):
    def __init__(self):
        self._url = "api.digitalocean.com"

    def _request(self, method, request):
        clientId = config.value('clientId', "")
        apiKey = config.value('apiKey', "")
        request = request % (clientId, apiKey)
        conn = httplib.HTTPSConnection(self._url)
        conn.putrequest(method, request)
        conn.endheaders()
        response = conn.getresponse()
        try:
            return json.loads(response.read())
        except:
            return

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

    def rename(self, dropletId, name):
        url = "/droplets/%s/rename/" % dropletId
        url += "?client_id=%s&api_key=%s"
        url += "&name=%s" % name
        return self._request("GET", url)