import cocos
from cocos.scenes.transitions import FadeTRTransition
import pyglet

##########################################################################################
##


class UILayer(cocos.layer.ColorLayer):
    """
    """

    def __init__(self):
        super(UILayer, self).__init__(0, 0, 0, 255, width=1024, height=760)

##########################################################################################
##


class IntroMenu(cocos.menu.Menu):
    """
    """

    #############################################################################
    def __init__(self, game):
        """ """
        super(IntroMenu, self).__init__()
        self.game = game
        self.font_item = {
            'font_name': 'Arial',
            'font_size': 32,
            'bold': True,
            'color': (220, 200, 220, 100),
        }
        self.font_item_selected = {
            'font_name': 'Arial',
            'font_size': 42,
            'bold': True,
            'color': (255, 255, 255, 255),
        }

        l = []
        l.append(cocos.menu.MenuItem('Join Game',
                                     self.game.on_join_game))
        l.append(cocos.menu.MenuItem('Host Game',
                                     self.game.on_host_game))
        l.append(cocos.menu.EntryMenuItem('Name:',
                                          self.game.on_name,
                                          self.game.player_name))
        l.append(cocos.menu.MenuItem('Quit', self.game.on_quit))

        self.create_menu(l)
