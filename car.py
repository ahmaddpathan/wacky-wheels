##################################

# This file contains the Car class and any of its associated
# functions/methods used in the game

##################################
from coin import *
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



# this function checks if car is within invisible margin area
# if a car crosses margin area, it facilitates camera movemenet
def isCarWithinMargin(app, x, y):
    
    if app.cameraWidth - x <= app.margin:
        
        return False
    
    if app.cameraHeight - y <= app.margin:
        
        return False
    
    if x <= app.margin:
        
        return False
    
    if y <= app.margin:
        
        return False
    
    return True



class Car: # class for player's car
    
    def __init__(self, x, y, width = 35, height = 25):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = 0
        self.velocity = 0
        self.maxSpeed = 20
        self.health = 100

    # gives us coordinates of car's corners
    def corners(self, app):

        carCenterX = self.x
        carCenterY = self.y
        
        halfWidth, halfHeight = self.width // 2, self.height // 2
        
        angleRad = math.radians(self.angle)
    

        # we use 2D rotation formula to calculate coordinates after rotation
        # if (a, b) is the origin, (x, y) after rotation is:
        # x coordinate = a + x * cos(angleRad) - y * sin(angleRad)
        # y coordinate = b + x * sin(angleRad) + y + cos(angleRad)
        
        # Top-right corner: (1, 1) from carCentre
        topRightX = (carCenterX + halfWidth * math.cos(angleRad)
                     - halfHeight * math.sin(angleRad))
        topRightY = (carCenterY + halfWidth * math.sin(angleRad)
                     + halfHeight * math.cos(angleRad))

        # Top-left corner: (-1, 1) from carCentre
        topLeftX = (carCenterX - halfWidth * math.cos(angleRad)
                    - halfHeight * math.sin(angleRad))
        topLeftY = (carCenterY - halfWidth * math.sin(angleRad)
                    + halfHeight * math.cos(angleRad))

        # Bottom-left corner: (-1, -1) from carCentre
        bottomLeftX = (carCenterX - halfWidth * math.cos(angleRad)
                       + halfHeight * math.sin(angleRad))
        bottomLeftY = (carCenterY - halfWidth * math.sin(angleRad)
                        - halfHeight * math.cos(angleRad))

        # Bottom-right corner: (1, -1) from carCentre
        bottomRightX = (carCenterX + halfWidth * math.cos(angleRad)
                        + halfHeight * math.sin(angleRad))
        bottomRightY = (carCenterY + halfWidth * math.sin(angleRad)
                        - halfHeight * math.cos(angleRad))
        
        # Calculate coordinates of the 4 corners of the car upon its rotation
        corners = [
                    (topRightX, topRightY),
                    (topLeftX, topLeftY),
                    (bottomLeftX, bottomLeftY),
                    (bottomRightX, bottomRightY)
                    ]
        
        return corners

    
    # draws the car using its corners
    def draw(self, app):
        
        corners = self.corners(app)
        
        # Draw the car on the screen according to updated parameters
        drawPolygon(corners[0][0], corners[0][1], corners[1][0], corners[1][1],
                    corners[2][0], corners[2][1], corners[3][0], corners[3][1],
                    fill='red', border = None)
        
        drawArc((corners[0][0] + 1 + corners[3][0])/2,
                (corners[0][1] + corners[3][1])/2, 60, self.width - 10,
                -90, 180,
                rotateAngle = self.angle, fill='lightBlue', border = None)
        
        drawArc((corners[1][0] + 1 + corners[2][0])/2,
                (corners[1][1] + corners[2][1])/2, 30, self.width - 10,
                90, 180,
                rotateAngle = self.angle, fill='red')
        
        for _ in range(4):
            
            for corner in corners:
                
                drawCircle(corner[0], corner[1], 6, fill = 'gray',
                           border = 'black')
        
        
    # implementing car movement
    def update(self, app, keys):
        
        # turning speed based on turning dynamics
        turningSpeed = app.turningSpeed * (abs(self.velocity)/self.maxSpeed)
        
        # left and right arrow keys rotates the car
        if 'left' in keys:
            
            self.angle -= turningSpeed
            
            
        if 'right' in keys:
            

            self.angle += turningSpeed
        
        
        # for forward and backward movement
        if 'up' in keys:
            
            

            self.velocity += app.acceleration

        # clamp down velocity to max speed
            if self.velocity > self.maxSpeed:
                
                self.velocity = self.maxSpeed
                
            if self.velocity < -self.maxSpeed:
                
                self.velocity = -self.maxSpeed
                
            angleRad = math.radians(self.angle)
            
            nextX = self.velocity * math.cos(angleRad)
            nextY = self.velocity * math.sin(angleRad)
            
            self.predictMove(app, nextX, nextY)
            
            
        if 'down' in keys:
            
            self.velocity -= app.acceleration

        # clamp down velocity to max speed
            if self.velocity > self.maxSpeed:
                
                self.velocity = self.maxSpeed
                
            if self.velocity < -self.maxSpeed:
                
                self.velocity = -self.maxSpeed
                
            angleRad = math.radians(self.angle)
            
            nextX = self.velocity * math.cos(angleRad)
            nextY = self.velocity * math.sin(angleRad)
            
            self.predictMove(app, nextX, nextY)

        # Update car's center position based on angle and velocity
        self.velocity -= app.friction * self.velocity
        
    def predictMove(self, app, nextX, nextY):
        
        # check if car is within margins (not visible on screen)
        # after predicted move

        # updates car's coordinates if car is within the margins
        if isCarWithinMargin(app, self.x + nextX, self.y + nextY):
            
            self.x += nextX
            self.y += nextY
         
        else:
             
            if nextX > 0:
                
                if self.x < app.margin:
                    
                    self.x += nextX
                
                elif app.cameraX + nextX < app.mapWidth - app.cameraWidth:
                    
                    app.cameraX += nextX
                    
                elif self.x + nextX + self.width / 2 < app.cameraWidth:
                    
                        self.x += nextX
                     
            if nextX < 0:
                
                if self.x > app.cameraWidth - app.margin:
                    
                    self.x += nextX
                    
                elif app.cameraX + nextX > 0:
                    
                    app.cameraX += nextX
                    
                elif self.x + nextX - self.width / 2 > 0:
                    
                    self.x += nextX
            
            if nextY > 0:
                
                if self.y < app.margin:
                    
                    self.y += nextY
                    
                elif app.cameraY + nextY < app.mapHeight - app.cameraHeight:
                    
                    app.cameraY += nextY
                    
                elif self.y + nextY + self.height / 2 < app.cameraHeight:
                    
                        self.y += nextY
                      
            if nextY < 0:
                
                if self.y > app.cameraHeight - app.margin:
                    
                    self.y += nextY
                    
                elif app.cameraY + nextY > 0:
                    
                    app.cameraY += nextY
                    
                elif self.y + nextY - self.height/2 > 0:
                    
                    self.y += nextY
                    
                    


