##################################

# This file contains the Coin class and any of its associated
# functions/methods used in the game

##################################
from car import *
from camera import *
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


class Coin: # class for all the coins in the game
    
    def __init__(self, x, y):
        
        self.x = x
        self.y = y
        self.radius = 15  # Radius of the coin
        self.offsetY = 0  # Vertical oscillation offset

    def draw(self, app):
        
        drawCircle(self.x - app.cameraX, self.y - app.cameraY + self.offsetY,
                   self.radius, fill='gold')
        
        drawCircle(self.x - app.cameraX, self.y - app.cameraY + self.offsetY,
                   self.radius - 5, fill='darkKhaki', border = 'black')
        
    def vibrate(self, app):
        
        amplitude = 6
    
        self.offsetY = math.cos(app.coinOscillation * app.blips) * amplitude
        


# check if the randomly chosen coordinates are within the track
# this helper function for generating the coins
def coinWithinTrack(x, y, track, trackImage, app):
    
    pixelX = x
    pixelY = y

    if 0 <= pixelX < track.width and 0 <= pixelY < track.height:
        
        r, g, b = getRGBPixel(pixelX, pixelY, trackImage)
        
        if (r, g, b) == (0, 0, 0):
            
            return True
    
    return False
    
    
    
# Generate coins randomly on the track
def generateCoins(app, numCoins=10):
    
    # reset coins
    app.coins = []
    
    while len(app.coins) < numCoins:

        coinX = random.randint(0, app.mapWidth)
        coinY = random.randint(0, app.mapHeight)
        
        if coinWithinTrack(coinX, coinY, app.track11Img, app.rgbTrack, app):
            
            app.coins.append(Coin(coinX, coinY))
            
      
      
# Check if the player collides with any coin.
def checkCoinCollision(app):
    
    player = app.player1
    corners = player.corners(app)
    corner1 = corners[0]
    corner2 = corners[1]
    
    for coin in app.coins:
            
        distance1 = (math.sqrt((corner1[0] + app.cameraX - coin.x) ** 2 +
                             (corner1[1] + app.cameraY - coin.y) ** 2))
        
        distance2 = (math.sqrt((corner2[0] + app.cameraX - coin.x) ** 2 +
                             (corner2[1] + app.cameraY - coin.y) ** 2))

        if (distance1 <= coin.radius + 3 * player.height // 4 or
            distance2 <= coin.radius + 3 * player.height // 4):
            # Collision detected
            
            if coin in app.coins:
                
                app.coins.remove(coin)
                app.score += 10

            
