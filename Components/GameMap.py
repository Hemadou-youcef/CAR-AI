from time import sleep
import random

class GameMap:
    def __init__(self,pygame,surface,width,height):
        self.surface = surface
        self.pygame = pygame
        self.width = width
        self.height = height

        # IMAGE

        self.mapNumber = 2
        self.MaxLineNumber = 64
        self.MapChangingNumber = 0

        self.map = any
        self.line = any
        self.generateRandomMap()
       
        
        self.draw()
        
    def getMap(self):
        return self.map

    def getStartPoint(self):
        if self.mapNumber == 1:
            return [150,450]
        elif self.mapNumber == 2:
            return [120,520]
        else:
            return [175,490]

    def getMask(self):
        mask = []
        for i in range(self.width):
            line = []
            for j in range(self.height):
                try:
                    if self.map.get_at((i,j)).a != 0:
                        line.append(1)
                    else:
                        line.append(0)
                except:
                    pass
            mask.append(line)
        return mask

    def getLine(self,number):
        # number += 8
        number = (number % (self.MaxLineNumber - 1)) + 1
        return  self.lines[number - 1]

    def showLine(self,number):
        # number += 8
        number = (number % (self.MaxLineNumber - 1)) + 1
        self.line = self.lines[number - 1]

    def generateRandomMap(self):
        if self.MapChangingNumber >= 30:
            number_map = random.randint(1,3)
        else:
            number_map = 3
        if number_map == 1:
            self.MaxLineNumber = 26
            self.mapNumber = number_map
        elif number_map == 2:
            self.MaxLineNumber = 64
            self.mapNumber = number_map
        else:
            self.MaxLineNumber = 46
            self.mapNumber = number_map 

        self.map = self.pygame.image.load("resource/image/maps/map" + str(number_map) +".png").convert_alpha()
        self.lines = []
        for i in range(self.MaxLineNumber):
            self.lines.append(self.pygame.image.load("resource/image/maps/lines" + str(self.mapNumber) + "/" + str(i + 1) + ".png").convert_alpha())
        self.line = self.lines[0]
        self.MapChangingNumber += 1

    def draw(self):
        self.surface.blit(self.line,(0,0))
        self.surface.blit(self.map,(0,0))

        


