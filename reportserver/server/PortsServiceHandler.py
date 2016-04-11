from reportserver.manager.PortManager import PortManager
from reportserver.manager import utilities



class PortsServiceHandler():

    def process(self, rqst, tokens):
        uom = None
        units = None
        print("processing ports request")

        if len(tokens) > 5:
            try:
                time_period = utilities.validateTimePeriod(tokens)
                uom = time_period[0]
                units = time_period[1]
            except ValueError:
                rqst.badRequest(units)

        if len(tokens) >= 5:
            portNbr = utilities.validatePortNumber(tokens[4])
            print("requested: " + str(portNbr))
            if portNbr is not None and 0 < portNbr < 9000:
                self.getPortDataByTime(rqst, portNbr, uom, units)
            else:
                rqst.badRequest()

        if len(tokens) == 4:
            self.get_port_list(rqst)
        else:
            rqst.badRequest()


    def get_port_list(self,rqst):
        #todo:  finish this!
        jsondata = "{links : [under construction]}"
        rqst.sendJsonResponse(jsondata, 200)

    def getPortDataByTime(self, rqst, portnumber, uom, unit):
        #default if we aren't given valid uom and unit
        if uom is None or unit is None:
            uom = "days"
            unit = 1

        portmgr = PortManager()
        portjsondata = portmgr.getPort(portnumber, uom, unit)
        if portjsondata is not None:
            # send response:
            rqst.sendJsonResponse(portjsondata, 200)
        else:
            rqst.notFound()
