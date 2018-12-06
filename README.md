# FlappyWyvern

|              |                                                          |      |
|------------- |:--------------------------------------------------------:|:-----|
|![Wyvern](https://raw.githubusercontent.com/erikbuck/FlappyWyvern/master/images/wyvernNE0.png)|A 2D Isometric side scrolling multi-player game using free online art assets.|This game uses an unmodified snapshot of [PodSixNet](https://github.com/chr15m/PodSixNet/) for easy network communications.|
|![Tree](https://raw.githubusercontent.com/erikbuck/FlappyWyvern/master/images/Tree_03.png)| Dodge evey obstacle!| Penetrate the beaurocracy! |

# Instructions

## Host a game

To start a game, cd into the FlappyWyvern directory and execute > `python Game.py`.

Select `Host` at the main menu to host a network game or play single-player.

*If you need to use a specific port for network communication*, Start a game with > `python Game.py hostname:port` where `hostname` is the name or IP address of the machine you are using to host a game, and `port` is the port you want to use like `8081`.

## Play 

Press the space bar to "flap".

## Join a game

To join an already running game hosted on the same computer, execute > `python Game.py`, and then select `Join` at the main menu.

To join an already running game hosted on a different computer, you must know the hostname or IP address for the other computer and start the game with > `python Game.py hostname:port` where `hostname` is the name or IP address of the machine hosting a game, and `port` is the port to use like `8081`. By default,  hosted games use port `8080`.
