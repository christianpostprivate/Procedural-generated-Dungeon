# Procedural Dungeon Generation - room(s) for improvement

This is my first attempt to write an algorithm for a procedural generated dungeon. Now, procedural in this context just means "random with rules", and the rules are not nearly as sophisticated in a game like Minecraft or Terraria, for example.

My goal was to put some evenly sized rooms into a fixed 2D grid, and they should all be connected to each other. I put this code together in roughly a week, and build it on top of an older game "engine" of mine, so some things are super convoluted and need to be refactored at some point, but this was only done to test if the algorithm translates to an actual game.

I made two videos to show how this code looks right now. The first is a visualisation of the actual dungeon generation, the second one is the rudimentary "game" that puts some crudely drawn tiles in each room and lets you (the blue square) traverse the dungeon. Oh, and it also has a mini map, which is pretty much the same as the first example, only scaled to be in the corner of the screen.

https://youtu.be/-qDMl8qPB0I

https://youtu.be/cOoYRCCjxXI

Also, here are the codes, one for the visualisation example and one for the game:

https://github.com/MattR0se/Procedural-generated-Dungeon/tree/master/Demo

https://github.com/MattR0se/Procedural-generated-Dungeon/tree/master/Game

Since the code is pretty huge by now, and my in-code comments are probably not that helpful, I will now go over my process of building this system. The code is found in the second link.

I started with the Room and Dungeon classes, which are in the rooms.py file. A Dungeon is pretty much a collection of rooms. It stores their position and their other attributs (doors, type). The Dungeon is what is randomized every time at the beginning of the game (this is, when you call the build() method). The Room objects themselves are containers for the layout (objects, tiles) of each room. Currently, this is just the data where the doors are, and everything else is the same, but I will add more variety in the future.

## The Room

Every Room is initialized with a string called 'doors', which is any combination of 'NSWE', the 4 cardinal directions. It also has a type, but at this point there are only 'default' and 'start', but I could see adding 'boss', 'merchant' and the likes.
```python
class Room():
    def __init__(self, game, doors, type_='default'):
        self.game = game
        self.doors = doors
        self.type = type_
        self.w = st.WIDTH // st.TILESIZE
        self.h = st.HEIGHT // st.TILESIZE
```

After that, I set the room's image. Right now, this is only used for a mini map in the corner of the screen.

```python
for key in self.game.room_image_dict:
    if fn.compare(self.doors, key):
        self.image = self.game.room_image_dict[key]
```

This looks complicated, but what the compare() method does is compare two strings regardless of the order of their letters. For example, compare('NWS', 'SWN') would return True. This way I don't have to worry about the order of the doors string. 

The Room has one method called 'tileRoom()'. Here, the layout (which stores information where the sprites are beinig placed) is created as a two-dimensional array (because this is python, 'list of lists' would be more precise, but I hope you get the idea. Right now, the first and last column are all 1s, which stand for wall tiles, and the floor are 0s. Notice that the outer loop is for the columns and the inner loop is for the rows, which is something I always confuse and it is a point where errors happen frequently, especially if you combine this with (x, y) coordinates and vectors, where it is the other way round...
```python
self.layout = []
for i in range(self.h):
    self.layout.append([])
    if i == 0 :
        for j in range(self.w):
            self.layout[i].append(1)
        elif i == self.h - 1:
            for j in range(self.w):
                self.layout[i].append(1)           
        else:
            for j in range(self.w):
                if j == 0:
                    self.layout[i].append(1)
                elif j == self.w - 1:    
                    self.layout[i].append(1)
                else:
                    # in the room
                        self.layout[i].append(0) 
```

In the final code, there is also a grid for the tile data, but since this depends on the final game and how your rooms should look like, I left this out for clarity reasons.

After the walls, the doors are put into the room's grid. I look for the 4 letters that represent the directions and if they are in the room's doors variable, a door is put in that particular spot, which here are just two 0s that determine that np wall should be placed there. 
```python
# north
if 'N' in self.doors:
    self.layout[0][door_w] = 0
    self.layout[0][door_w - 1] = 0
    
# south
if 'S' in self.doors:
    self.layout[self.h - 1][door_w] = 0
    self.layout[self.h - 1][door_w - 1] = 0

# west
if 'W' in self.doors:
    self.layout[door_h][0] = 0
    self.layout[door_h - 1][0] = 0

# east
if 'E' in self.doors:
    self.layout[door_h][self.w - 1] = 0
    self.layout[door_h - 1][self.w - 1] = 0
```
And that's it for now with the Room object.

## The Dungeon

As for the Dungeon object, it it initialized with a size (that restrains how big your Dungeon can possibly be and what shape it has), a room pool (every possible room object), a 'rooms' that is again a 2D grid for the rooms, initially with only 'None' in it, and a 'room_map' that stores an unique ID for every room. Now, this is probably not needed after I refactored the code, but for now it is necessary to check if there is a room transition and what the next room is after that.
```python
class Dungeon():
    def __init__(self, game, size):
        self.size = vec(size)
        self.game = game
           
        self.room_pool = [
                Room(self.game, 'NS'),  
                Room(self.game, 'WE'),  
                Room(self.game, 'N'),
                Room(self.game, 'S'),
                Room(self.game, 'W'),
                Room(self.game, 'E'),
                Room(self.game, 'SW'),
                Room(self.game, 'SE'),
                Room(self.game, 'NE'),
                Room(self.game, 'NW'),
                Room(self.game, 'NSWE'),
                Room(self.game, 'NWE'),
                Room(self.game, 'SWE'),
                Room(self.game, 'NSW'),
                Room(self.game, 'NSE')
                ]
        
        w = int(self.size.x)
        h = int(self.size.y)
        # empty dungeon
        self.rooms = [[None for i in range(w)] for j in range(h)]
        self.room_map = [[(j * w + i) for i in range(w)] for j in range(h)]
```
Then, the starting room is created. In this example, it is a room with 4 exits and located in the middle of the grid, but it could also have any given position and number of exists. I believe this is how it's done in The Binding of Isaac, whereas in Zelda, the entrance would be at the bottom of the dungeon's grid.
```python
# starting room
self.rooms[h//2][w//2] = Room(self.game, 'NSWE', 'start')
self.room_index = [h//2, w//2]
```
There is also the 'room_index', which is probably redundant since it stores the same information as the room_map's contents.

Finally, 'build()' is called. Now, you could call this function from the Game() object instead if you wanted to instantiate the Dungeon only once but build a different maze multiple times. For example if you wanted to keep certain attributes the same, but randomize every time the player enters the dungeon. That's pretty much up to you.
self.done is just a boolean that checks if no room was placed during a loop, and if so, stays True. That's how I know the dungeon is finished.
```python
self.done = False
        
self.build()
```
Now, the build method is where the magic happens, so to speak. There is a while loop that goes through the rooms grid and checks for every room's doors and if there is empty space and if so, places a random room.
```python
def build(self):  
    while self.done == False:
        self.done = True
        for i in range(1, len(self.rooms) - 1):
            for j in range(1, len(self.rooms[i]) - 1):
                room = self.rooms[i][j]
                if room:
                    if 'N' in room.doors and self.rooms[i - 1][j] == None:
                        if i == 1:
                            self.rooms[i - 1][j] = Room(self.game, 'S')
                        else:
                            rng = choice(st.ROOMS['N'])
                            for rm in self.room_pool:
                                if fn.compare(rng, rm.doors):
                                    self.rooms[i - 1][j] = rm
                        self.done = False

                    if 'W' in room.doors and self.rooms[i][j - 1] == None:
                        if j == 1:
                            self.rooms[i][j - 1] = Room(self.game, 'E')
                        else:
                            rng = choice(st.ROOMS['W'])
                            for rm in self.room_pool:
                                if fn.compare(rng, rm.doors):
                                    self.rooms[i][j - 1] = rm
                        self.done = False

                    if 'E' in room.doors and self.rooms[i][j + 1] == None:
                        if j == len(self.rooms) - 2:
                             self.rooms[i][j + 1] = Room(self.game, 'W')
                        else:
                            rng = choice(st.ROOMS['E'])
                            for rm in self.room_pool:
                                if fn.compare(rng, rm.doors):
                                    self.rooms[i][j + 1] = rm
                        self.done = False                              

                    if 'S' in room.doors and self.rooms[i + 1][j] == None:
                        if i == len(self.rooms) - 2:
                            pass
                            self.rooms[i + 1][j] = Room(self.game, 'N')
                        else:
                            rng = choice(st.ROOMS['S'])
                            for rm in self.room_pool:
                                if fn.compare(rng, rm.doors):
                                    self.rooms[i + 1][j] = rm
                        self.done = False
```
A little bit more in-depth: The code loops through each item in the rooms grid, except for the first and last rows and columns. Remember that there are only 'None's in the beginning, except for the starting room. So if the loop reaches this room, the 'if room:' is True because 'None' defaults to False.
```python
while self.done == False:
    self.done = True
    for i in range(1, len(self.rooms) - 1):
        for j in range(1, len(self.rooms[i]) - 1):
            room = self.rooms[i][j]
            if room: # if room is not None
```
Now, there are a bunch of if-clauses that check if that room.doors has a certain direction in it and also if there is a room next to it in that direction. For example, if room.doors has 'N' in it, it has to check north of that room. That would be rooms[i-1][j] because remember, the vertical component comes first in the grid (Imagine this as rooms[y][x]). If there is no room, there are two options: If i == 1, it means that the next room would be placed at the border, so no room with an 'N' door should be placed there. For this example, I chose only to place the 'S' room, but other possible rooms would be 'SE', 'SW' and 'SWE'.
```python
if 'N' in room.doors and self.rooms[i - 1][j] == None:
    if i == 1:
        self.rooms[i - 1][j] = Room(self.game, 'S')
    else:
        rng = choice(st.ROOMS['N'])
        for rm in self.room_pool:
            if fn.compare(rng, rm.doors):
                self.rooms[i - 1][j] = rm
    self.done = False
```
Otherwise, it the Dungeon picks a room constellation randomly from a list. Now, this is the important part that defines the overall structure of your final dungeon. See that currently, for the 'N' direction there are four items 'NS' in it, three 'S' and one of each of the other possible choices. So, it is four times as likely to pick the 'NS' and three times as likely to pick 'S' than the other constellations. Here you can play with the list and see what happens. For example, if you put even more 'NS' room in there, the branches become more streched. If you have only one 'NS' in there, the rooms will somewhat clump together. If you add more 'S', the dungeon gets smaller. This is determined in the settings.py:
```python
ROOMS = {
        'N': ['NS', 'NS', 'NS', 'NS', 'S', 'S', 'S', 'WS', 'ES', 'SWE', 'NSW', 'NSE'],
        'W': ['WE', 'WE', 'WE', 'WE', 'E', 'E', 'E', 'ES', 'EN', 'SWE', 'NSE', 'NWE'],
        'E': ['WE', 'WE', 'WE', 'WE', 'W', 'W', 'W', 'WS', 'WN', 'SWE', 'NSW', 'NWE'],
        'S': ['NS', 'NS', 'NS', 'NS', 'N', 'N', 'N', 'WN', 'EN', 'NSE', 'NSW', 'NWE']
        }
```
This is done for all 4 directions. You could also make totally different room_pools for each direction, if you want the dungeon to branch out more to one direction, for example. This is really up to you.

The second method blitRooms() is just a visual representation of the generated dungeon and serves as a mini map. If you want to know more about that, leave a comment.
```python
def blitRooms(self):
    # blit a map image onto the screen
    scale = (3 * st.GLOBAL_SCALE, 3 * st.GLOBAL_SCALE)

    w = self.size[0] * scale[0]
    h = self.size[1] * scale[1]

    self.map_img = pg.Surface((w, h))

    for i in range(len(self.rooms)):
        for j in range(len(self.rooms[i])):
            room = self.rooms[i][j]
            pos = (j * (w / self.size[0]), i * (h / self.size[1]))
            if room:
                self.map_img.blit(pg.transform.scale(room.image,
                                  scale), pos)
                if room.type == 'start':
                    # blue square representing the starting room
                    self.map_img.blit(pg.transform.scale(
                            self.game.room_images[12], scale), pos)
            else:
                self.map_img.blit(pg.transform.scale(
                        self.game.room_images[17], scale), pos)

    pos2 = (self.room_index[1] * (w / self.size[0]), 
                           self.room_index[0] * (h / self.size[1]))
    # red square representing the player
    self.map_img.blit(pg.transform.scale(self.game.room_images[11], scale), 
                                         pos2)
    self.map_img.set_alpha(150)
    self.game.screen.blit(self.map_img, (0, 0))
```
I also won't go much into detail about the sprites.py, functions.py and settings.py. In sprites, there are just the player and the wall sprite and all the player does is move and check for collisions with the wall sprite. Aside from the collision, functions also contains the room transition (which is a mess tbh) and some methods for loading images and make a background out of a tileset. Again, feel free to ask about them in the comments.

The settings contain some variables regarding the screen and tile size. I made it so that you can change the GLOBAL_SCALE variable and everything in the game keeps its proportions.

Alright, so it all comes together in the main.py (as you would probably expect). First, I load all the images for the rooms (which are used for the mini map) and different tilesets that have a similar layout, but different color, from which the game picks a random one. 
```python
def load_data(self):
    game_folder = path.dirname(__file__)
    img_folder = path.join(game_folder, 'images')

    self.room_images = fn.img_list_from_strip(path.join(img_folder, 
                                                        'rooms_strip_2.png'), 
                                              16, 16, 0, 18)
    self.room_image_dict = {
            'NSWE': self.room_images[0],
            'NS': self.room_images[1],
            'WE': self.room_images[2],
            'N': self.room_images[3],
            'S': self.room_images[4],
            'W': self.room_images[5],
            'E': self.room_images[6],
            'SW': self.room_images[7],
            'SE': self.room_images[8],
            'NE': self.room_images[9],
            'NW': self.room_images[10],
            'NWE': self.room_images[13],
            'SWE': self.room_images[14],
            'NSE': self.room_images[15],
            'NSW': self.room_images[16]
            }

    self.tileset_names = ['tileset.png', 'tileset_sand.png', 
                          'tileset_green.png','tileset_red.png']

    self.tileset_list = [fn.tileImageScale(path.join(img_folder, 
                         tileset), 16, 16, 
                         scale=1) for tileset in self.tileset_names]
```
In new(), the Dungeon, the background and the sprites are put into the game. 
```python
def new(self):
    # start a new game
    # initialise sprite groups
    self.all_sprites = pg.sprite.LayeredUpdates()
    self.walls = pg.sprite.Group()

    # instantiate objects
    self.dungeon = rooms.Dungeon(self, st.DUNGEON_SIZE)
    self.room_number = self.dungeon.room_map[self.dungeon.room_index[0]][
                                             self.dungeon.room_index[1]]

    # pick a random tileset from all available tilesets
    self.tileset = choice(self.tileset_list)
    # create a background image from the tileset for the current room
    self.background = fn.tileRoom(self, self.tileset, self.dungeon.room_index)

    # spawn the player in the middle of the screen/room
    self.player = spr.Player(self, (st.WIDTH // 2 - st.TILESIZE /2, 
                                    st.HEIGHT // 2 - st.TILESIZE / 2))
    # spawn the wall objects (invisible)
    self.walls = fn.transitRoom(self, self.walls, self.dungeon, 
                                self.room_number)

    self.run()
```
The transitioning between rooms happens in the update() method (and it should probably be its own method for clarity reasons). Again, the system with room numbers and room index is too convoluted and I have to clean it up, but it works for now.
```python
def update(self):
    index = self.dungeon.room_index

    # game loop update
    # update the player (move and check for collisions with walls)
    self.player.update(self.walls)
    
    # check for room transitions on screen exit (every frame)
    new_room, new_pos = fn.screenWrap(self.player, self.dungeon)
    if new_room != self.room_number: 
        self.room_number = new_room
        # build the new room
        fn.tileRoom(self, self.tileset, self.dungeon.room_index)
        self.background = fn.tileRoom(self, self.tileset, self.dungeon.room_index)
        self.walls = fn.transitRoom(self, self.walls, 
                                    self.dungeon, self.room_number)
        self.player.rect.topleft = new_pos
```
So, feel free to play the game if you want. You can restart the game with the R key to get a fresh dungeon.

You can also change some variables in the settings.py (and try to crash the game, if you want ;) )

Things I need to improve:

- The way the loop in the dungeon generation works right now is that it leaves out the first and last iteration. That was just a lazy way to prevent index errors, but prevents putting the starting room along a border.

- Close doors that lead to nowhere: Right now, there is the chance of generating one-way doors, where one room has a door in a direction but the adjacent room doesn't. I would appreciate some ideas on that.

- A pathfinding algorithm. Now, that's a whole 'nother topic, but at least I want to know what the longest branch in a dungeon is to place the boss room there, for example.

Also, the game currently has a bug where it occationally puts the wrong room. This is not happening in the demo, so maybe this is a copy/paste bug...

Feel free to test the code and commentate!
