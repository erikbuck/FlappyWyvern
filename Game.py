import UILayer
import PlayLayer
import ServerPlayLayer
import ClientPlayLayer
import cocos
from cocos.scenes.transitions import FadeTRTransition
import pyglet
import sys
import random

##########################################################################################
##
class Game(object):
   """
   """

   default_title = "Flappy Wyvern"
   default_window_width = 1024
   default_window_height = 760

   #############################################################################
   def __init__(self):
      """ """
      super( Game, self ).__init__()
      
      self.player_name = "Nobody"
      try:
         allNames = [name.strip() for name in open("nicknames.txt", 'r')]
         self.player_name = random.choice(allNames).capitalize()
      except:
         pass
            
      director_width = Game.default_window_width
      director_height = Game.default_window_height

      caption = Game.default_title + ' ' + \
         ServerPlayLayer.ServerPlayLayer.ownID
      cocos.director.director.init(
         director_width, director_height,
         caption = caption, fullscreen=False)

      intro_layer = UILayer.UILayer()
      intro_layer.anchor_x = director_width * 0.5
      intro_layer.anchor_y = director_height * 0.5

      intro_menu = UILayer.IntroMenu(self)
      intro_layer.add(intro_menu)

      self.intro_scene = cocos.scene.Scene(intro_layer)

   #############################################################################
   def run(self, host=None, port=8080):
      """ """
      self.host = host
      self.port = port
      cocos.director.director.set_show_FPS(True)
      cocos.director.director.run (self.intro_scene)

   #############################################################################
   def on_join_game( self ):
      """ """
      playLayer = ClientPlayLayer.ClientPlayLayer(
            self.host, self.port, self.player_name)
      cocos.director.director.replace(FadeTRTransition(
            cocos.scene.Scene(playLayer), 2))

   #############################################################################
   def on_host_game( self ):
      """ """
      cocos.director.director.replace(FadeTRTransition(
         cocos.scene.Scene(ServerPlayLayer.ServerPlayLayer(self.port)), 2))

   #############################################################################
   def on_name( self, value ):
      """ """
      self.player_name = value

   #############################################################################
   def on_quit( self ):
      """ """
      pyglet.app.exit()

##########################################################################################
##
if __name__ == "__main__":
   game = Game()
   if len(sys.argv) == 2:
      host, port = sys.argv[1].split(":")
      print("{}:{}".format(host, port))
      game.run(host, int(port))
   else:
      game.run()
