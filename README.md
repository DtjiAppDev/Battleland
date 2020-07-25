# Battleland

"Battleland" is a turn based battle arena game running on command line interface. This game is played offline and allows both single player and 
multiplayer modes (1 - 10 players can play). All battles are 5 v 5 battles which can involve at least 1 and at most 10 human players. Each
player in the battle will be placed in one of the two teams randomly and both teams have 5 players.

Ever heard of "Mobile Legends: Bang Bang" on Google Play Store? Basically, this game involves both 5 v 5 PVP and PVE battles like "Mobile Legends:
Bang Bang". You will understand about this game well if you are good in playing "Mobile Legends: Bang Bang". However, the differences between this game
and "Mobile Legends: Bang Bang" are that this game is offline, running on command line interface, and is turn based.

### Executable File

The executable file "battleland.exe" is used to run the game application. It is downloadable from 
https://github.com/CreativeCloudAppDev2020/Battleland/blob/master/executable/battleland.exe.

### Source Code

Python code used to create the game application is available in 
https://github.com/CreativeCloudAppDev2020/Battleland/blob/master/code/battleland.py.

### Getting Started

Once you run the game application, you will be asked whether you want to continue playing the game or not. The image below shows what appears.
Typing in anything besides 'Y' will save game data and then quit the game. Meanwhile, typing in 'Y' will make you asked to type in what game
mode you want to play in (either single player or multiplayer).

![Getting Started](https://github.com/CreativeCloudAppDev2020/Battleland/blob/master/images/Getting%20Started.png)

### Mode Selection

You can choose either single player or multiplayer mode when playing this game. Below shows how mode selection looks like.

![Mode Selection](https://github.com/CreativeCloudAppDev2020/Battleland/blob/master/images/Mode%20Selection.png)

### Single Player Mode

In single player mode, you will play with 9 CPU controlled players where 4 of them are your teammates. You will be randomly placed in either team one or
team two for the battle.

#### Human Player Data Creation

You will be told to create human player data when no human player data has been saved. The creation process involves entering your name and looks like below.

![Human Player Data Creation](https://github.com/CreativeCloudAppDev2020/Battleland/blob/master/images/Human%20Player%20Data%20Creation.png)

#### Rune Purchase

Runes are purchaseable from the battlefield shop during battles. They are used to temporarily strengthen the heroes players control during battles. They can be purchased
by any players who are currently having their turn during the battle. Below shows how it looks like when you are about to buy a rune.

![Rune Purchase 1](https://github.com/CreativeCloudAppDev2020/Battleland/blob/master/images/Rune%20Purchase%201.png)

The screenshot above shows that when you enter Y when asked whether you want to buy a rune or not, you will be asked to enter the index (an integer) of the rune you
want to purchase where index 0 means the first rune in the list of runes sold in the battlefield shop, index 1 means the second rune in the list, and so on.

![Rune Purchase 2](https://github.com/CreativeCloudAppDev2020/Battleland/blob/master/images/Rune%20Purchase%202.png)

#### Battle Turn

Once you have your turn, you will be asked to input the x and y coordinates of the tile you want to move to. If the move to the destination tile is valid, the hero you control
will be moved there. Else, you will be asked to input another value of x and y coordinates until you input a valid move.

![Move Hero](https://github.com/CreativeCloudAppDev2020/Battleland/blob/master/images/Move%20Hero.png)

#### Attack a Character or Building

If a character or building on a tile next to the tile where the hero you control is at is detected, you will be asked whether you want to attack that character or building 
or not.

![Attack](https://github.com/CreativeCloudAppDev2020/Battleland/blob/master/images/Attack.png)

### Multiplayer Mode

In multiplayer mode, you will play with 1 to 9 other human players where 4 of all other players in the battle are your teammates. You will be randomly placed in either team one 
or team two for the battle. Everything in this mode works similarly to single player mode except that more human players are involved than in single player mode and that you are
able to create more than one human player if there are less than two human players in the saved game data. To get an idea about how battle turns, attacking characters or 
buildings, rune purchase, and human player data creation work in multiplayer, see "Single Player Mode" section of this document.

The screenshot below shows a part which is in multiplayer mode but not in single player mode. This part involves entering how many human players are to be in the battle.

![Multiplayer](https://github.com/CreativeCloudAppDev2020/Battleland/blob/master/images/Multiplayer.png)

### Upgrade Purchase

Upgrades are purchaseable from the global shop outside battles. They are used to permanently strengthen the heroes players control during battles. Below shows how it
looks like when you are about to buy an upgrade.

![Upgrade Purchase 1](https://github.com/CreativeCloudAppDev2020/Battleland/blob/master/images/Upgrade%20Purchase%201.png)

The screenshot above shows that when you enter Y when asked whether you want to buy an upgrade or not, a list of upgrades sold in the upgrade shop is shown. Then, you
will be asked to enter the index (an integer) of the upgrade you want to purchase where index 0 means the first upgrade in the list, index 1 means the second upgrade in
the list, and so on.

![Upgrade Purchase 2](https://github.com/CreativeCloudAppDev2020/Battleland/blob/master/images/Upgrade%20Purchase%202.png)

### Version History

#### Version pre-release 1 (Saturday, 25 July 2020)

This version is the first pre-release version of the game. This implies that the game is still under development. Customer feedbacks regarding
the game are required for improvement of the game. One way to give feedbacks is by creating issues in this repository.
