from time import sleep
import threading
import math


class Car:
    def __init__(self,name, pygame, surface,position_x = 120,position_y = 520):
        self.name = name
        self.surface = surface
        self.pygame = pygame
    
        
        self.car1 = self.pygame.image.load("resource/image/cars/car1.png").convert_alpha()
        self.Origincar1 = self.pygame.transform.scale(self.car1, (28, 13))
        self.car1 = self.pygame.transform.scale(self.car1, (28, 13))
        
        self.currentRotation = 0
        self.rotation = 0

        self.isDead = False
        self.score = 0

        self.position_x = position_x
        self.offset_xpos = position_x

        self.position_y = position_y
        self.offset_ypos = position_y

        self.rotateCar()
        self.draw()

    def getXY(self):
        return [int(self.offset_xpos), int(self.offset_ypos)]

    def setXY(self,x,y):
        self.position_x = x
        self.position_y = y

    def getCar(self):
        return self.car1

    def getMonitorPoint(self):
        return self.calculateDisplacement(self.position_x,self.position_y,-self.currentRotation,20)

    def getAngle(self):
        return self.currentRotation

    def draw(self):
        if not self.isDead:
            # self.goForward(False)
            rotate_angle = -self.currentRotation
            monitor_position_source = self.calculateDisplacement(self.position_x,self.position_y,rotate_angle,20)
            monitor_position_right = self.calculateDisplacement(monitor_position_source[0],monitor_position_source[1],rotate_angle + 45,150)
            monitor_position_left = self.calculateDisplacement(monitor_position_source[0],monitor_position_source[1],rotate_angle - 45,150)
            monitor_position_front = self.calculateDisplacement(monitor_position_source[0],monitor_position_source[1],rotate_angle,150)

            self.pygame.draw.line(self.surface, (0,255,0), monitor_position_source, monitor_position_front)
            self.pygame.draw.line(self.surface, (0,0,255), monitor_position_source, monitor_position_left)
            self.pygame.draw.line(self.surface, (255,0,0), monitor_position_source, monitor_position_right)
            self.surface.blit(self.car1,(self.offset_xpos,self.offset_ypos))
        

    def killCar(self):
        self.isDead = True

    def goLeft(self,slope):
        NewAngle = self.currentRotation + (slope * 5) 
        if NewAngle > 180:
            self.currentRotation = NewAngle - 360
        else:
            self.currentRotation = NewAngle
        self.rotateCar()
    
    def goRight(self,slope):
        NewAngle = self.currentRotation - (slope * 5) 
        if NewAngle <= -180:
            self.currentRotation = NewAngle + 360
        else:
            self.currentRotation = NewAngle
        self.rotateCar()

    def goForward(self,ADD_SPEED,speed):
        # if ADD_SPEED:offset_x, offset_y = self.calculateDisplacement(0,0,self.currentRotation,20)
        # else:offset_x, offset_y = self.calculateDisplacement(0,0,self.currentRotation,15)
        offset_x, offset_y = self.calculateDisplacement(0,0,self.currentRotation,30 * speed)
        self.position_x += offset_x / 5
        self.position_y -= offset_y / 5
        self.rotateCar()

    def calculateDisplacement(self,x,y,angle,length):
        y += math.sin(math.radians(angle)) * length
        x += math.cos(math.radians(angle)) * length
        return x,y
    
    
    def rotateCar(self):
        x,y = [0,0]
        if 0 <= self.currentRotation <= 90:
            x,y = self.calculateDisplacement(0,0,90 - self.currentRotation,6)
            y += math.cos(math.radians(90 - self.currentRotation)) * 26
        elif -90 <= self.currentRotation < 0 :
            x,y = self.calculateDisplacement(0,0,-1 * self.currentRotation   + 90,6)
            x += math.cos(math.radians(90 + self.currentRotation)) * 13
        elif 90 < self.currentRotation < 180:
            x,y = self.calculateDisplacement(0,0,self.currentRotation % 90,6)
            x += math.sin(math.radians(self.currentRotation % 90)) * 26
            y = math.cos(math.radians(self.currentRotation % 90)) * 26 + math.sin(math.radians(self.currentRotation % 90)) * 13 - y
        elif -180 < self.currentRotation < -90:
            x,y = self.calculateDisplacement(0,0,-1 * self.currentRotation % 90,6)
            x += math.cos(math.radians(self.currentRotation % 90)) * 26
        elif self.currentRotation == 180:
            x = 26
            y = 6
        elif self.currentRotation == -180:
            x = 26
            y = 6

        self.offset_xpos = self.position_x - x
        self.offset_ypos = self.position_y - y
        self.car1 = self.pygame.transform.rotate(self.Origincar1, self.currentRotation)


    def restart(self,x,y):
        self.currentRotation = 0
        self.rotation = 0

        self.position_x = x
        self.offset_xpos = x

        self.position_y = y
        self.offset_ypos = y

        self.isDead = False

        self.rotateCar()
        self.draw()
