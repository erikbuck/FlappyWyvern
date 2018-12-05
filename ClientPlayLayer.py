import PlayLayer
import ChatClient
import cocos
import pyglet
import socket
import sys
from PodSixNet.Connection import connection, ConnectionListener

##########################################################################################
#


class ClientPlayLayerClient(ConnectionListener):
    """ """

    def __init__(self, host, port):
        self.Connect((host, port))

    #######################################
    ### Network event/message callbacks ###
    #######################################

    def Network_players(self, data):
        print("*** players: " + ", ".join([p for p in data['players']]))

    def Network_message(self, data):
        print(data['who'] + ": " + data['message'])

    # built in stuff

    def Network_connected(self, data):
        print("You are now connected to the server")

    def Network_error(self, data):
        print('error:', data['error'][1])
        connection.Close()

    def Network_disconnected(self, data):
        print('Server disconnected')
        exit()

    def Network_info(self, data):
        """ """
        # print(str(data))
        # sys.stdout.flush()
        if 'who' in data:
            id = data['who']
            #print("received {} {}".format(id, str(data)))
            # sys.stdout.flush()
            if not id in PlayLayer.PlayLayer.idToWyvernTable:
                print("Adding wyvern {}\n".format(id))
                sys.stdout.flush()
                PlayLayer.PlayLayer.addWyvern(id, Wyvern.Wyvern())

            if (not id == ClientPlayLayer.ownID) and ('i' in data):
                currentWyvern = PlayLayer.PlayLayer.idToWyvernTable[id]

                info = data['i']
                if 'mapPosition' in info:
                    currentWyvern.mapPosition = info['mapPosition']
                    currentWyvern.altitude = currentWyvern.mapPosition[1] * 96
                    #print("Set map position: {} {}\n".format(id, currentWyvern.mapPosition))
                    # sys.stdout.flush()
                if 'v' in info:
                    currentWyvern.verticalVelocity = info['v']
                if 'h' in info:
                    currentWyvern.horizontalVelocity = info['h']

##########################################################################################
#


class ClientPlayLayer(PlayLayer.PlayLayer):
    """ """
    ownID = socket.gethostbyname(socket.gethostname())

    #############################################################################
    def __init__(self, host, port=8080, nickname="nobody"):
        """ """
        super(ClientPlayLayer, self).__init__()

        self.host = host
        self.port = port

        if None == self.host:
            self.host = ClientPlayLayer.ownID
        if None == self.port:
            self.port = 8080

        self.client = ClientPlayLayerClient(self.host, self.port)
        connection.Send({"action": "nickname", "nickname": nickname})

    #############################################################################
    def getOwnID(self):
        return ClientPlayLayer.ownID

    def update(self, dt):
        super(ClientPlayLayer, self).update(dt)

        mapPosition = self.wyvern.mapPosition
        info = {'mapPosition': mapPosition,
                'v': self.wyvern.verticalVelocity,
                'h': self.wyvern.horizontalVelocity}
        data = {"action": "cinfo", "i": info, "who": ClientPlayLayer.ownID}
        #print("sending {}".format(str(data)))
        connection.Send(data)

        connection.Pump()
        self.client.Pump()
