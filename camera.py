##################################

# This file contains the Camera class, Track class and any of their associated
# functions/methods used in the game

##################################
from car import *
from coin import *
from cmu_graphics import *
from PIL import Image
import math
import random
import os, pathlib


# general helper functions
def openImage(fileName):
    
    return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))


def getRGBPixel(x, y, image):
    
    return image.getpixel((x, y))



### ************************************************************** ###
                    
                    
                    
# class to manage camera and mini map related methods 
class Camera:
    
    def __init__(self, app, x, y, width=800, height=600):

        self.x = 0
        self.y = 0
    
    # for accessing camera top left coordinates
    def giveCamera(self):
        
        return self.x, self.y
     
     
    # to draw mini map
    def drawMiniMap(self, app, car):
        
        miniMapX = app.cameraWidth - app.miniMapWidth - 15
        miniMapY = app.cameraHeight - app.miniMapHeight - 15

        # draw mini map background
        drawRect(miniMapX - 3, miniMapY - 3, app.miniMapWidth + 6,
                 app.miniMapHeight+ 6, fill='black')

        # scale positions to fit the map
        scaleX = app.miniMapWidth / app.mapWidth
        scaleY = app.miniMapHeight / app.mapHeight
        
        drawImage(app.track1Img, miniMapX, miniMapY, width = 160, height = 120)
        # dynamically change car's position on mini map
        radarCarX = miniMapX + (app.player1.x + app.cameraX) * scaleX
        radarCarY = miniMapY + (app.player1.y + app.cameraY) * scaleY
        
        drawCircle(radarCarX, radarCarY, 3, fill = 'red')
        
        # for drawing coins on mini map
        for coin in app.coins:
            
            radarCoinX = miniMapX + (coin.x) * scaleX
            radarCoinY = miniMapY + (coin.y) * scaleY
        
            drawCircle(radarCoinX, radarCoinY, 3, fill='white')



### ************************************************************** ###
            

# class to manage all tracks in the game
class Track:
    
    def __init__(self, url, x, y):
        
        self.url = url
        self.x = x
        self.y = y
        
        
    def draw(self, app):
        
        drawImage(self.url, self.x - app.cameraX, self.y - app.cameraY)



# checks whether car's center is within the track or not       
def checkTrack(app, car, track, trackRGB):
    
    carX = car.x + app.cameraX
    carY = car.y + app.cameraY

    if (0 <= carX < track.width and 0 <= carY < track.height):
        
        r, g, b = getRGBPixel(carX , carY, trackRGB)
        
        if (r, g, b) == (0, 0, 0): 
            
            return False
        

    # the car is not on the track
    return True
