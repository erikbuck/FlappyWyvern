import cocos
import pyglet
from pyglet import image as Image
from pyglet.image import Animation as Anim
import Map

##########################################################################################
##
class Wyvern(cocos.layer.Layer):
   gravity = -9.8
   secondsPerFrame = 0.075

   # Create a texture atlas from the individual frames of the wyvern animations
   wyvernBin = pyglet.image.atlas.TextureBin()
   wyvernTextures = []
   for i in range(0,24):
      name = "images/wyvernNE{}.png".format(i)
      wyvernTextures.append(wyvernBin.add(pyglet.image.load(name)))

   wyvernsTextures = []
   for i in range(0,24):
      names = "images/wyvernsNE{}.png".format(i)
      wyvernsTextures.append(wyvernBin.add(pyglet.image.load(names)))

   #############################################################################
   animation = {
     'hover' : Anim.from_image_sequence(wyvernTextures[0:8], secondsPerFrame, loop=True),
     'fly' : Anim.from_image_sequence(wyvernTextures[8:16], secondsPerFrame, loop=True),
     'die' : Anim.from_image_sequence(wyvernTextures[16:24], secondsPerFrame, loop=False),
   }
   animations = {
     'hover' : Anim.from_image_sequence(wyvernsTextures[0:8], secondsPerFrame, loop=True),
     'fly' : Anim.from_image_sequence(wyvernsTextures[8:16], secondsPerFrame, loop=True),
     'die' : Anim.from_image_sequence(wyvernsTextures[16:24], secondsPerFrame, loop=False),
   }
   
   #############################################################################
   def __init__(self):
      """ Constructor """
      super(Wyvern, self).__init__()
      self.altitude = 0
      self.verticalVelocity = 0
      self.horizontalVelocity = 0
      self.lateralVelocity = 0
      self.sprite = cocos.sprite.Sprite(Wyvern.animation['hover'])
      self.sprite.position = 200, 80 + self.altitude
      self.sprites = cocos.sprite.Sprite(Wyvern.animations['hover'])
      self.sprites.position = 200,100
      self.mapPosition = (4, 0, 0)
      self.animationName = 'hover'
      self.sprite.image = Wyvern.animation[self.animationName]
      self.sprites.image = Wyvern.animations[self.animationName]
      self.isDead = False
      
   #############################################################################
   def moveLeft(self):
      if not self.isDead:
         self.lateralVelocity -= 0.1
      
   #############################################################################
   def moveRight(self):
      if not self.isDead:
         self.lateralVelocity += 0.1
      
   #############################################################################
   def flap(self):
      if not self.isDead:
         self.verticalVelocity += 3
         self.horizontalVelocity = min(0.3, self.horizontalVelocity + 0.02)

   #############################################################################
   def respawn(self):
      self.isDead = False
      
   #############################################################################
   def update(self, dt):
      self.verticalVelocity = self.verticalVelocity + Wyvern.gravity * dt
      self.altitude += self.verticalVelocity

      if self.altitude <= 0:
         self.altitude = 0
         self.verticalVelocity = 0
         self.horizontalVelocity = max(0, self.horizontalVelocity - 0.1)
      elif self.altitude > 500:
         self.altitude = 500
         self.verticalVelocity = 0

      x,y,z = self.mapPosition
      x = min(max(-1.0, x + self.lateralVelocity), 6.0)
      self.lateralVelocity *= 0.9 # make lateralVelocity decay
      y = self.altitude / 96
      z += self.horizontalVelocity
      self.mapPosition = (x, y, z)
      self.sprite.position = Map.Map.positionForMapPosition(x, y, z)
      self.sprites.position = Map.Map.positionForMapPosition(x, 0, z)
	  
      if self.isDead:
         if self.animationName != 'die':
            self.animationName = 'die'
            self.sprite.image = Wyvern.animation[self.animationName]
            self.sprites.image = Wyvern.animations[self.animationName]
             
      elif self.horizontalVelocity < 0.05:
         if self.animationName != 'hover':
            self.animationName = 'hover'
            self.sprite.image = Wyvern.animation[self.animationName]
            self.sprites.image = Wyvern.animations[self.animationName]

      elif self.animationName != 'fly':
         self.animationName = 'fly'
         self.sprite.image = Wyvern.animation[self.animationName]
         self.sprites.image = Wyvern.animations[self.animationName]

