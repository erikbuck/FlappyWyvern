import PlayLayer
import ChatServer
import cocos
import pyglet
import socket
import sys

##########################################################################################
#
class ServerPlayLayerClientChannel(ChatServer.ClientChannel):
   """ """

   def Network_cinfo(self, data):
      """ """
      if 'who' in data:
         id = data['who']
         #print("received {} {}".format(id, str(data)))
         #sys.stdout.flush()
         if not id in PlayLayer.PlayLayer.idToWyvernTable:
            print("Adding wyvern {}\n".format(id))
            sys.stdout.flush()
            PlayLayer.PlayLayer.addWyvern(id, Wyvern.Wyvern()) 

         if 'i' in data:
            currentWyvern = PlayLayer.PlayLayer.idToWyvernTable[id]

            info = data['i']
            if 'mapPosition' in info:
               currentWyvern.mapPosition = info['mapPosition']
               currentWyvern.altitude = currentWyvern.mapPosition[1] * 96
               #print("Set map position: {} {}\n".format(id, currentWyvern.mapPosition))
               #sys.stdout.flush()
            if 'v' in info:
               currentWyvern.verticalVelocity = info['v']
            if 'h' in info:
               currentWyvern.horizontalVelocity = info['h']
   
##########################################################################################
##########################################################################################
#
class ServerPlayLayer(PlayLayer.PlayLayer):
   """ """
   ownID = socket.gethostbyname(socket.gethostname())
   
   #############################################################################
   def __init__( self, port=8080 ):
      """ """
      super( ServerPlayLayer, self ).__init__()

      self.port = port
      ChatServer.ChatServer.channelClass = ServerPlayLayerClientChannel
      self.server = ChatServer.ChatServer(localaddr=(
         ServerPlayLayer.ownID, self.port))
      
   #############################################################################
   def getOwnID(self):
      return ServerPlayLayer.ownID
      
   def update(self, dt):
      super(ServerPlayLayer, self).update(dt)
      
      for id in PlayLayer.PlayLayer.idToWyvernTable:
         currentWyvern = PlayLayer.PlayLayer.idToWyvernTable[id]
         mapPosition = currentWyvern.mapPosition
         info = {'mapPosition': mapPosition, 
            'v': self.wyvern.verticalVelocity,
            'h': self.wyvern.horizontalVelocity}
         data = {"action": "info", "i": info, "who": id}
         self.server.SendToAll(data)
         
      self.server.Pump()
