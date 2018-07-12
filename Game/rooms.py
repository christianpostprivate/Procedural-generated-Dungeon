import pygame as pg
from random import choice

import settings as st
import functions as fn

vec = pg.math.Vector2


class Room():
    def __init__(self, game, doors, type_='default'):
        self.game = game
        self.doors = doors
        self.type = type_
        self.w = st.WIDTH // st.TILESIZE
        self.h = st.HEIGHT // st.TILESIZE
     
        self.image = self.game.room_image_dict[self.doors]
        #self.tileRoom()
        
        
    def tileRoom(self):
        # floor tile
        floor = 7
        
        # layout is for objects, tiles for the tileset index
        self.layout = []
        self.tiles = []
        for i in range(self.h):
            self.layout.append([])
            self.tiles.append([])
            if i == 0 :
                for j in range(self.w):
                    self.layout[i].append(1)
                    
                    if j == 0:
                        self.tiles[i].append(12)
                    elif j == self.w - 1:
                        self.tiles[i].append(13)
                    else:
                        self.tiles[i].append(28)
            elif i == self.h - 1:
                for j in range(self.w):
                    self.layout[i].append(1)
                    
                    if j == 0:
                        self.tiles[i].append(21)
                    elif j == self.w - 1:
                        self.tiles[i].append(22)
                    else:
                        self.tiles[i].append(10)
            else:
                for j in range(self.w):
                    if j == 0:
                        self.layout[i].append(1)
                        
                        self.tiles[i].append(20)
                        
                    elif j == self.w - 1:    
                        self.layout[i].append(1)
                        
                        self.tiles[i].append(18)
                    else:
                        self.layout[i].append(0)
                        self.tiles[i].append(floor)
        
        # doors
        door_w = self.w // 2
        door_h = self.h // 2
        
        # north
        if 'N' in self.doors:
            self.layout[0][door_w] = 0
            self.layout[0][door_w - 1] = 0
            
            self.tiles[0][door_w + 1] = 27
            self.tiles[0][door_w] = floor
            self.tiles[0][door_w - 1] = floor
            self.tiles[0][door_w - 2] = 29
        
        # south
        if 'S' in self.doors:
            self.layout[self.h - 1][door_w] = 0
            self.layout[self.h - 1][door_w - 1] = 0
            
            self.tiles[self.h - 1][door_w + 1] = 9
            self.tiles[self.h - 1][door_w] = floor
            self.tiles[self.h - 1][door_w - 1] = floor
            self.tiles[self.h - 1][door_w - 2] = 11
        
        # west
        if 'W' in self.doors:
            self.layout[door_h][0] = 0
            self.layout[door_h - 1][0] = 0
            
            self.tiles[door_h + 1][0] = 11
            self.tiles[door_h][0] = floor
            self.tiles[door_h - 1][0] = floor
            self.tiles[door_h - 2][0] = 29
        
        # east
        if 'E' in self.doors:
            self.layout[door_h][self.w - 1] = 0
            self.layout[door_h - 1][self.w - 1] = 0
            
            self.tiles[door_h + 1][self.w - 1] = 9
            self.tiles[door_h][self.w - 1] = floor
            self.tiles[door_h - 1][self.w - 1] = floor
            self.tiles[door_h - 2][self.w - 1] = 27
        


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
        # starting room
        self.rooms[h//2][w//2] = Room(self.game, 'NSWE', 'start')
        self.room_index = [h//2, w//2]
        
        self.done = False
        
        self.build()
        print('done')
        # work in progress
        #self.checkDoors()
                
        
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
  
    
    def checkDoors(self):
        for i in range(1, len(self.rooms) - 1):
            for j in range(1, len(self.rooms[i]) - 1):
                room = self.rooms[i][j]
                room_n = self.rooms[i - 1][j]
                room_s = self.rooms[i + 1][j]
                room_w = self.rooms[i][j - 1]
                room_e = self.rooms[i][j + 1]
                
                if room:
                    print(j, i, room.doors)
                    for door in room.doors:  
                        if door == 'N' and room_n:
                            if 'S' in room_n.doors:
                                room_n.doors = room_n.doors.replace('S', '')
                                room.doors = room.doors.replace('N', '')
                        if door == 'S' and room_s:
                            if 'N' in room_s.doors:
                                room_s.doors = room_s.doors.replace('N', '')
                                room.doors = room.doors.replace('S', '')
                                
                        if door == 'E' and room_e:
                            if 'W' in room_e.doors:
                                room_e.doors = room_e.doors.replace('E', '')
                                room.doors = room.doors.replace('W', '')
                                
                        if door == 'W' and room_w:
                            if 'E' in room_w.doors:
                                room_w.doors = room_w.doors.replace('E', '')
                                room.doors = room.doors.replace('W', '')
                    print(j, i, room.doors)
                    room.tileRoom()
                            
    

    def blitRooms(self):
        # blit a map image onto the screen
        scale = (4 * st.GLOBAL_SCALE, 4 * st.GLOBAL_SCALE)
        
        w = self.size[0] * scale[0]
        h = self.size[1] * scale[1]
        self.map_img = pg.Surface((w, h), flags=pg.SRCALPHA)
        self.map_img.fill((0, 0, 0, 100))
             
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
        self.game.screen.blit(self.map_img, (0, 0))
        
