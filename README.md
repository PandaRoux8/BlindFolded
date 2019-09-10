
Things to implement for the game :

  - A main menu
  - An option menu (resolution, keys, fps, fullscreen/windowed)
  - Find a way to scale the game for different resolution
  - An ESC menu -> To leave the game and go to the main menu

  - A save file for the configuration
  - A save file for the game
  - Create a connector matching tiles and their position
    ->  Wall = 0, Hole = 1, etc. 
    
  - Optimize the game check update/draw method in game
  
  Socket : 
  - Manage disconnect error.. 

 Map class :
 
    - A special tile to go from a map to another (Loads the map)
    - Replace the tile where the player spawned by a ground tile -> Check this with layer maybe (This is quickfixed)

 Map Parser class :
    - The display is wrong -> The screen is flipped in a weird way

Type of tiles :
 
    - Pit
    - Ground
    - Action Tile (Bumper, map rotation etc.)
    

Character class:

    - Action
    - Give action to the character (plant a tree)
    - Direction of the char (display)



General idea :

    - 2 player game cooperation
    - Player 1 don't see the map and has to be guided by the Player 2
    - ? Player 2 can place item on the map (like bridge)

Item on the map :

    - Bumper
    - Bridge
    - Téléporteur (différentes couleurs vu seulement par P1)
    - Projecteur de lumières pour les 2 joueurs (Zone affiché différents parfois)
    - Tourelle statique (à désactiver par P2 en mettant un objet devant) 
    - Clé
    - Inverseur de touches
    - ? Piège à désactiver par P2
 
    - Puzzle avec forme (Keep talking and nobody explode)
 
SOCKET : https://realpython.com/python-sockets/#echo-client-and-server

OTHERS :

 - Get a tileset with only black tile for P1 (except char) 
 - Standard tileset for P2

Make a script to put header on each python file.

# Name      : Schluchter Jules
# Mail      : jules.schluchter@gmail.com
# Date      : <today>
# Module    : BlindFolded Game  
