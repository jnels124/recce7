import json
from http.server import BaseHTTPRequestHandler


from reportserver.server.PortsServiceHandler import PortsServiceHandler


notFoundPayload = {}

badRequestPayload = {
    'error': 'invalid port number'}


#  Handles the service request, determines what was requested,
#  then returns back response.
#
class RestRequestHandler (BaseHTTPRequestHandler):

    def do_GET(self) :

        #self.send_header("Access-Control-Allow-Origin","http://127.0.0.1:8000")
        tokens = self.path.split('/')
        print(tokens)

        if self.path.startswith("/v1/analytics"):
            if len(tokens) >= 4:
                if str(tokens[3]) == "ports":
                    PortsServiceHandler().process(self, tokens)
                #TODO:  here is where we add more urls like /ipaddresses/
                else:
                    self.badRequest()
            else:
                self.showIndex()
        else:
            self.notFound()



    def getIndexPayload(self, path):
        #TODO:  how to get full path here??
        print("address : " + str(self.client_address))
        full_path = 'http://%s:%s' % (str(self.client_address[0]), str(8080))

        #fullpath = "http://"+self.address_string[0] + ":" + self.address_string[1] + self.path
        return  {'links': ['rel: ports, href: ' + full_path + path + '/ports']}

    def showIndex(self):
        # send response code:
        self.sendJsonResponse(self.getIndexPayload(self.path), 200)

    def notFound(self):
        # send response code:
        self.sendJsonResponse(notFoundPayload,404)

    def badRequest(self):
        # send response code:
        self.sendJsonResponse(badRequestPayload,400)

    def sendJsonResponse(self, payload, responseCode):

        # Note:  responseCode must be set before headers in python3!!
        # see this post:
        # http://stackoverflow.com/questions/23321887/python-3-http-server-sends-headers-as-output/35634827#35634827
        json_result = json.dumps(payload)
        self.send_response(responseCode)
        #todo make this configurable
        self.send_header("Access-Control-Allow-Origin","http://localhost:8000")
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(json_result))
        self.end_headers()
        self.flush_headers()

        self.wfile.write(bytes(json_result, "utf-8"))

        self.wfile.flush()

        return




