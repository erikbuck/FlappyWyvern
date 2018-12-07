import cocos
import pyglet
from pyglet import image as Image
import Wyvern
import Map

##########################################################################################
#
class KeyboardInputLayer(cocos.layer.Layer):
   """
   """

   # You need to tell cocos that your layer is for handling input!
   # This is key (no pun intended)!
   # If you don't include this you'll be scratching your head wondering why your game isn't accepting input
   is_event_handler = True

   def __init__(self):
      """ """
      super(KeyboardInputLayer, self).__init__()
      self.keys_being_pressed = set()

   def on_key_press(self, key, modifiers):
      """ """
      self.keys_being_pressed.add(key)

   def on_key_release(self, key, modifiers):
      """ """
      if key in self.keys_being_pressed:
         self.keys_being_pressed.remove(key)

class GroundLayer(cocos.layer.Layer):
  """ """
  ground_image = pyglet.resource.image('images/dirtsand2.png')

  def __init__(self):
    super( GroundLayer, self ).__init__()
    self.batch = cocos.batch.BatchNode()
    self.add(self.batch)
    for i in range(0,100):
      gsprite = cocos.sprite.Sprite(GroundLayer.ground_image)
      gsprite.position = 128 + i * 256, i * 128
      self.batch.add(gsprite, z=0)


##########################################################################################
#
class PlayLayerAction(cocos.actions.Action):
   """
   """
   def step(self, dt):
      """ """
      self.target.update(dt)

##########################################################################################
#
class PlayLayer(KeyboardInputLayer):
   rubbleWallSpritesheet = pyglet.resource.image('images/TileObjectsRubbleWalls.png')
   rubbleWallGrid = Image.ImageGrid(rubbleWallSpritesheet, 8, 8)
   rubbleWallTextures = Image.TextureGrid(rubbleWallGrid)
   idToWyvernTable = {}
   
   #############################################################################
   def __init__(self):
      """ """
      super(PlayLayer, self).__init__()
      self.groundOffsetX = 0
      self.groundOffsetY = 0
      self.backgroundLayer = cocos.layer.ColorLayer(100, 100, 100, 255,
            width=1024, height=768)
      self.add(self.backgroundLayer, z=0)
      self.groundLayer = GroundLayer()
      self.backgroundLayer.add(self.groundLayer, z=0)

      self.obstacleLayer = cocos.layer.Layer()
      self.backgroundLayer.add(self.obstacleLayer, z=2)

      self.wyvern = Wyvern.Wyvern()
      self.do(PlayLayerAction())

      self.obstacleDict = {}
      
      for obstacleInfo in Map.obstacleInfos:
         obstacle = cocos.sprite.Sprite(PlayLayer.rubbleWallTextures[obstacleInfo['id']])
         mapPosition = (
               obstacleInfo['x'], 
               obstacleInfo['y'], 
               obstacleInfo['z']
         )
         obstacle.position = Map.Map.positionForMapPosition(
               mapPosition[0], mapPosition[1], mapPosition[2])
         self.obstacleLayer.add(obstacle, z=Map.Map.zForMapPosition(
               mapPosition[0], mapPosition[1], mapPosition[2]))
         self.obstacleDict[mapPosition] = True
       
      self.allWyvernsBatch = cocos.batch.BatchNode()
      self.obstacleLayer.add(self.allWyvernsBatch, z=66)
      
      self.allWyvernsShadowsBatch = cocos.batch.BatchNode()
      self.obstacleLayer.add(self.allWyvernsShadowsBatch)
      
      PlayLayer.addWyvern(self.getOwnID(), self.wyvern)   

   #############################################################################
   @staticmethod
   def addWyvern(id, wyvern):
      PlayLayer.idToWyvernTable[id] = wyvern
      print("Added wyvern {}\n".format(id))
   
   #############################################################################
   def getOwnID(self):
      return ""
      
   #############################################################################
   def respawn(self):
     self.wyvern.respawn()
      
   #############################################################################
   def update(self, dt):
      for id in PlayLayer.idToWyvernTable:
         currentWyvern = PlayLayer.idToWyvernTable[id]
         if currentWyvern.parent == None:
            self.obstacleLayer.add(currentWyvern.sprite)
            self.allWyvernsShadowsBatch.add(currentWyvern.sprites)
         currentWyvern.update(dt)
      self.groundOffsetX = -self.wyvern.sprite.position[0] + 200
      self.groundOffsetY = -self.wyvern.sprite.position[1] + 80 + self.wyvern.altitude
      self.groundLayer.position = self.groundOffsetX, self.groundOffsetY
      self.obstacleLayer.position = self.groundOffsetX, self.groundOffsetY
      self.obstacleLayer.remove(self.wyvern.sprite)
      self.obstacleLayer.add(self.wyvern.sprite,
            z=Map.Map.zForMapPosition(4, self.wyvern.altitude / 96, 0))
      x, y, z = self.wyvern.mapPosition
      intMapPosition = (
         int(x + 0.5),
         int(y + 0.5),
         int(z + 0.5)
      )
      #print(intMapPosition)
      if intMapPosition in self.obstacleDict:
         if not self.wyvern.isDead:
            #print('Collision!')
            self.wyvern.isDead = True
            self.wyvern.mapPosition = (self.wyvern.mapPosition[0],
               self.wyvern.mapPosition[1],
               self.wyvern.mapPosition[2] - 1.5)
            self.horizontalVelocity = -0.02
            self.do(cocos.actions.Delay(3) + cocos.actions.CallFunc(self.respawn))
            
   #############################################################################
   def on_key_press(self, key, modifiers):
      """ """
      super(PlayLayer, self).on_key_press(key, modifiers)
      if pyglet.window.key.SPACE in self.keys_being_pressed:
         self.wyvern.flap()

   #############################################################################
   def on_key_release(self, key, modifiers):
      super(PlayLayer, self).on_key_release(key, modifiers)
