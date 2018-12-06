import cocos
import pyglet
from pyglet import image as Image
import random


##########################################################################################
##
obstacleInfos = [
   {'id':30, 'x':0, 'y':0, 'z':10},
   {'id':23, 'x':1, 'y':0, 'z':10},
   {'id':23, 'x':2, 'y':0, 'z':10},
   {'id':23, 'x':3, 'y':0, 'z':10},
   {'id':23, 'x':4, 'y':0, 'z':10},
   {'id':23, 'x':5, 'y':0, 'z':10},
   {'id':23, 'x':6, 'y':0, 'z':10},
   {'id':23, 'x':7, 'y':0, 'z':10},
   {'id':31, 'x':0, 'y':1, 'z':10},
   {'id':23, 'x':1, 'y':1, 'z':10},
   {'id':23, 'x':2, 'y':1, 'z':10},
   {'id':23, 'x':3, 'y':1, 'z':10},
   {'id':23, 'x':4, 'y':1, 'z':10},
   {'id':23, 'x':5, 'y':1, 'z':10},
   {'id':23, 'x':6, 'y':1, 'z':10},
   {'id':23, 'x':7, 'y':1, 'z':10},
   {'id':29, 'x':0, 'y':2, 'z':10},
   {'id':40, 'x':1, 'y':2, 'z':10},
   {'id':23, 'x':6, 'y':2, 'z':10},
   {'id':23, 'x':7, 'y':2, 'z':10},
   
   {'id':30, 'x':0, 'y':0, 'z':20},
   {'id':23, 'x':1, 'y':0, 'z':20},
   {'id':23, 'x':2, 'y':0, 'z':20},
   {'id':23, 'x':3, 'y':0, 'z':20},
   {'id':23, 'x':4, 'y':0, 'z':20},
   {'id':23, 'x':5, 'y':0, 'z':20},
   {'id':23, 'x':6, 'y':0, 'z':20},
   {'id':23, 'x':7, 'y':0, 'z':20},
   {'id':55, 'x':0, 'y':3, 'z':20},
   {'id':23, 'x':0, 'y':4, 'z':20},
   {'id':23, 'x':1, 'y':4, 'z':20},
   {'id':23, 'x':2, 'y':4, 'z':20},
   {'id':23, 'x':3, 'y':4, 'z':20},
   {'id':23, 'x':4, 'y':4, 'z':20},
   {'id':23, 'x':5, 'y':4, 'z':20},
   {'id':23, 'x':6, 'y':4, 'z':20},
   {'id':23, 'x':7, 'y':4, 'z':20},
   {'id':54, 'x':7, 'y':3, 'z':20},  
]

##########################################################################################
##
class Map(cocos.layer.Layer):
   """
   """

   #############################################################################
   @staticmethod
   def positionForMapPosition(x, y, z):
      offsetX = x - 3
      return (offsetX * 32 + z * 32, offsetX * -16 + y * 96 + z * 16)

   #############################################################################
   @staticmethod
   def zForMapPosition(x, y, z):
      return x + y * 8

