##################################

# This file contains all the screens used in the game and onAppStart
# this is the core module of the game

##################################

from car import *
from coin import *
from camera import *
from cmu_graphics import *
from PIL import Image
import math
import random
import os, pathlib



### ************************************************************** ###


# PIL image import path is weird so we always use absolute path
def openImage(fileName):
    
    return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))


# to get the RGB value of a pixel in an image
def getRGBPixel(x, y, image):
    
    return image.getpixel((x, y))




### ************************************************************** ###



# This is the code for start menu

def start_onScreenActivate(app):
    
    app.back = openImage('back.jpg')
    app.back = CMUImage(app.back)
    app.score = 0
    app.blips = 0
    app.wheelX = 150
    app.wheelAngle = 0
    app.wheelIncrement = 5
    app.startYes = False
    app.instructionsYes = False
    app.sound = Sound('startSound.mp3')
    app.sound.play(loop = True)
    
    
def start_redrawAll(app):
    
    drawImage(app.back, 0, 0, width = app.width, height = app.height)
    
    # Draw Title    
    drawRect(app.cameraWidth // 2, 100, 490, 80, fill='papayaWhip',
             align = 'center', border = 'maroon')
    
    drawLabel("Wacky Wheels", app.cameraWidth // 2, 100, size = 60,
              fill = 'maroon', font = 'caveat', bold = True)
    
    # Draw Moving Wheel
    drawImage(app.imageWheel, app.wheelX , 500,
              width = app.wheelWidth // 2, height = app.wheelHeight // 2,
              align = 'center', rotateAngle = app.wheelAngle)
    
    # Draw Sub-Title
    drawRect(app.cameraWidth // 2, 200, 250, 50, fill='maroon',
             align = 'center', border = 'maroon')
    
    drawLabel('A Driving Experience', app.cameraWidth // 2, 200, size = 20,
              fill = 'cornSilk', bold = True)
    
    # Draw Start Button
    drawRect(app.cameraWidth // 2 - 100, 270, 200, 50,
             fill=gradient('midnightBlue', 'cyan', start = "right-top"), 
             border="white", borderWidth=2)
    
    drawLabel("Start Game", app.cameraWidth // 2, 295, size = 24,
              fill='aliceBlue', bold = True)
    
    if app.startYes:
        
        drawRect(app.cameraWidth // 2 - 100, 270, 200, 50,
                 fill=None, border="Yellow", borderWidth=4)   
        
    # Draw Instructions Button
    drawRect(app.cameraWidth // 2 - 100, 350, 200, 50,
             fill=gradient('maroon','bisque', start = 'left-top'),
             border="white", borderWidth=2)
    
    drawLabel("Instructions", app.cameraWidth // 2, 375, size=24,
              fill='aliceBlue', bold = True)
    
    if app.instructionsYes:
        
        drawRect(app.cameraWidth // 2 - 100, 350, 200, 50,
             fill=None, border="Yellow", borderWidth=4)
    


def start_onMousePress(app, mouseX, mouseY):
    
    # Check if "Start Game" button is clicked
    if (app.cameraWidth // 2 - 100 <= mouseX <= app.cameraWidth // 2 + 100 and
        270 <= mouseY <= 320):
        
        app.sound.pause()
        resetApp(app)
        setActiveScreen('loading')

    # Check if "Instructions" button is clicked
    elif (app.cameraWidth // 2 - 100 <= mouseX <= app.cameraWidth // 2 + 100 and
          350 <= mouseY <= 400):
        
        app.sound.pause()
        setActiveScreen('instructions')
        
      
      
def start_onMouseMove(app, mouseX, mouseY):
    
    # Check if cursor is hovering over "Start Game" button
    if (app.cameraWidth // 2 - 100 <= mouseX <= app.cameraWidth // 2 + 100 and
        270 <= mouseY <= 320):
        
        app.startYes = True
        
    else:
        
        app.startYes = False

    # Check if cursor is hovering over "Instructions" button is clicked
    if (app.cameraWidth // 2 - 100 <= mouseX <= app.cameraWidth // 2 + 100 and
          350 <= mouseY <= 400):
        
        app.instructionsYes = True
        
    else:
        
        app.instructionsYes = False
    


def start_onStep(app):
    
    # To move the wheel on the menu
    app.wheelAngle += 8
    
    if app.wheelX <= 100 or app.wheelX >= 700:
        
        app.wheelIncrement = -app.wheelIncrement
    
    app.wheelX += app.wheelIncrement

    
    



### ************************************************************** ###




# This is the code for loading animation when you switch between menu and game


def loading_onScreenActivate(app):
    
    app.back = openImage('loading.jpg')
    app.back = CMUImage(app.back)
    
    app.loadingTime = 0
    app.loadingAngle = 0  # Tracks the rotation angle
    app.loadingDone = False  # Tracks if loading is complete
    
    app.cx = app.cameraWidth // 2
    app.cy = app.cameraHeight // 2
    app.sideLength = 100
    app.velX = 5
    app.velY = 3

    
    
def loading_redrawAll(app):
    
    # draw background
    drawImage(app.back, 0, 0, width = app.width, height = app.height)
    
    # draw Loading Title
    drawRect(app.cameraWidth // 2, app.cameraHeight // 2 - 170, 200, 50,
             fill='tan', align = 'center')
    
    drawLabel("LOADING", app.cameraWidth // 2,
              app.cameraHeight // 2 - 170, size=35, fill='white',
              align = 'center', bold=True)
    
    # draw Loading Animation
    drawImage(app.imageWheel, app.cx, app.cy,
              width = app.wheelWidth // 2,
              height = app.wheelHeight // 2, align = 'center',
              rotateAngle = app.loadingAngle)
   
    # draw bottom Tagline
    drawLabel("Get. Set. Drive. Collect Coins!", app.cameraWidth // 2,
              app.cameraHeight - 100,
              size = 30, fill = 'honeydew', align = 'center', bold = True)
    
    
    
def loading_onStep(app):
    
    app.loadingAngle += 7
    
    # once the loading squares rotate by 700 deg, game screen appears
    if app.loadingAngle == 700:
        
        setActiveScreen('trackSelection')

    app.cx += app.velX
    app.cy += app.velY

    boxX = 100 
    boxY = 80 

    # Check for collisions with the boundaries of the box
    if (app.cameraWidth // 2 - boxX // 2 >= app.cx or
        app.cx >= app.cameraWidth // 2 + boxX // 2):
        
        app.velX = -app.velX
        
    if (app.cameraHeight // 2 - boxY // 2 >= app.cy or
        app.cy >= app.cameraHeight // 2 + boxY // 2):
        
        app.velY = -app.velY
        




### ************************************************************** ###


# this is the code for Track Selection Screen

def trackSelection_onScreenActivate(app):
    
    app.back = openImage('back.jpg')
    app.back = CMUImage(app.back)
    
    app.trackNames = ["1. Pittsburgh Track", "2. Doha Track",
                      "3. Srinagar Track", "4. Lahore Track"]
    
    app.sound = Sound('startSound.mp3')
    app.sound.play(loop = True)
    

def trackSelection_redrawAll(app):

    drawImage(app.back, 0, 0)
    
    drawRect(app.width // 2, 50, 500, 50, fill = 'maroon', align = 'center')
    drawLabel("Select Your Track", app.width // 2, 50, size=40, fill='white',
              bold=True)
    
    drawImage(app.tracks[0][1], 80, 100, width = 280, height = 180)
    drawImage(app.tracks[1][1], 460, 100, width = 280, height = 180)
    drawImage(app.tracks[2][1], 80, 330, width = 280, height = 180)
    drawImage(app.tracks[3][1], 460, 330, width = 280, height = 180)
    
    drawRect(220, 300, 200, 24, align = 'center')
    drawLabel(app.trackNames[0], 220, 300, fill = 'white', bold = True,
              size = 18)
    
    drawRect(600, 300, 160, 24, align = 'center')
    drawLabel(app.trackNames[1], 600, 300, fill = 'white', bold = True,
              size = 18)
    
    drawRect(220, 530, 160, 24, align = 'center')
    drawLabel(app.trackNames[2], 220, 530, fill = 'white', bold = True,
              size = 18)
    
    drawRect(600, 530, 160, 24, align = 'center')
    drawLabel(app.trackNames[3], 600, 530, fill = 'white', bold = True,
              size = 18)
    
    drawRect(app.width // 2, app.height - 25, 400, 30, fill = 'beige',
             align = 'center', border = 'black')
    drawLabel("Press 1, 2, 3, or 4 to Select a Track", app.width // 2,
              app.height - 25, size=20, fill='maroon', bold = True)
    

def trackSelection_onKeyPress(app, key):
    
    # Change selected track based on key press
    if key == '1':
        
        app.trackSelected = app.tracks[0]
        app.sound.pause()
        setActiveScreen('game')
    
    if key == '2':
        
        app.trackSelected = app.tracks[1]
        app.sound.pause()
        setActiveScreen('game')
        
    if key == '3':
        
        app.trackSelected = app.tracks[2]
        app.sound.pause()
        setActiveScreen('game')
        
    if key == '4':
        
        app.trackSelected = app.tracks[3]
        app.sound.pause()
        setActiveScreen('game')

    



### ************************************************************** ###


# this is the code for pause menu


def pause_onScreenActivate(app):
    
    app.back = openImage('pause.jpg')
    app.back = CMUImage(app.back)
    
    app.resumeYes = False
    app.instructionsYes = False
    app.resetYes = False
  
  
  
def pause_redrawAll(app):
    
    # Draw Background 
    drawImage(app.back, 0, 0, width = app.cameraWidth,
              height = 2 * app.cameraHeight)
    
    # Draw Pause Menu Title
    drawLabel("PAUSED", app.cameraWidth // 2, app.cameraHeight // 2 - 150,
          size=40, align = 'center', fill = 'black', bold = True)
    
    # Draw Resume Button
    drawRect(app.cameraWidth // 2, app.cameraHeight // 2 - 20, 200, 50,
             fill = gradient('midnightBlue', 'cyan', start = "right-top"),
             align = 'center', border = "sienna", borderWidth = 2)
    
    drawLabel("RESUME", app.cameraWidth // 2, app.cameraHeight // 2 - 20,
              size=22, fill='aliceBlue', bold = True)
    
    if app.resumeYes:
        
        drawRect(app.cameraWidth // 2, app.cameraHeight // 2 - 20, 200, 50,
                 fill = None, align = 'center', border = "Yellow",
                 borderWidth = 4)
    
    # Draw Reset Button
    drawRect(app.cameraWidth // 2, app.cameraHeight // 2 + 80, 200, 50, 
             fill = gradient('midnightBlue', 'cyan', start = "right-top"),
             align = 'center', border = 'sienna', borderWidth=2)
    
    drawLabel("RESET", app.cameraWidth // 2, app.cameraHeight // 2 + 80,
              size = 22, align = 'center', fill = 'aliceBlue', bold = True)
    
    if app.resetYes:
        
        drawRect(app.cameraWidth // 2, app.cameraHeight // 2 + 80, 200, 50, 
                 fill = None, align = 'center', border = 'Yellow',
                 borderWidth = 4)
    
    
    # draw Instructions Button
    drawRect(app.cameraWidth // 2, app.cameraHeight // 2 + 180, 200, 50,
             fill = gradient('midnightBlue', 'cyan', start = "right-top"),
             align = 'center', border = 'sienna', borderWidth = 3)
    
    drawLabel("INSTRUCTIONS", app.cameraWidth // 2, app.cameraHeight // 2 + 180,
              size=22, align = 'center', fill='aliceBlue', bold = True)
    
    
    if app.instructionsYes:
        
        drawRect(app.cameraWidth // 2, app.cameraHeight // 2 + 180, 200, 50,
                 fill = None, align = 'center', border = 'Yellow',
                 borderWidth = 4)



def pause_onMousePress(app, mouseX, mouseY):
    
        # Check if "Resume" button is clicked
    if (app.cameraWidth // 2 - 100 <= mouseX <= app.cameraWidth // 2 + 100 and
        app.cameraHeight // 2 - 45 <= mouseY <= app.cameraHeight // 2 + 5):
        
        setActiveScreen('game')


    # Check if "Reset" button is clicked
    elif (app.cameraWidth // 2 - 100 <= mouseX <= app.cameraWidth // 2 + 100 and
          app.cameraHeight // 2 + 55 <= mouseY <= app.cameraHeight // 2 + 105):
        
        resetApp(app)
        setActiveScreen('start')
    
    # Check if "Instructions" button is clicked
    elif (app.cameraWidth // 2 - 100 <= mouseX <= app.cameraWidth // 2 + 100 and
          app.cameraHeight // 2 - 155 <= mouseY <= app.cameraHeight // 2 + 205):
        
        setActiveScreen('instructionsPause')

        
        

def pause_onMouseMove(app, mouseX, mouseY):
    
        # Check if cursor hovers "Resume" button
    if (app.cameraWidth // 2 - 100 <= mouseX <= app.cameraWidth // 2 + 100 and
        app.cameraHeight // 2 - 45 <= mouseY <= app.cameraHeight // 2 + 5):
        
        app.resumeYes = True
        
    else:
        
        app.resumeYes = False


        # Check if cursor hovers over "Reset" button
    if (app.cameraWidth // 2 - 100 <= mouseX <= app.cameraWidth // 2 + 100 and
        app.cameraHeight // 2 + 55 <= mouseY <= app.cameraHeight // 2 + 105):
        
        app.resetYes = True
    
    else:
        
        app.resetYes = False
        
        # Check if cursor hovers over "Instructions" button
    if (app.cameraWidth // 2 - 100 <= mouseX <= app.cameraWidth // 2 + 100 and
        app.cameraHeight // 2 + 155 <= mouseY <= app.cameraHeight // 2 + 205):
        
        app.instructionsYes = True
    
    else:
        
        app.instructionsYes = False
        
        
    
def pause_onKeyPress(app, key):
    
    if key == 'p':
        
        setActiveScreen('game')
    
    if key == 'r':
        
        resetApp(app)
        setActiveScreen('start')






### ************************************************************** ###



# this is the code for the instructions page on Pause Menu


def instructionsPause_onScreenActivate(app):
    
    app.back = openImage('instruction.jpg')
    app.back = CMUImage(app.back)
    app.g1 = 'guidelines1.jpg'
    app.g2 = 'guidelines2.jpg'
    app.displaying = app.g1
    app.front = openImage(app.displaying)
    app.front = CMUImage(app.front)
    
    
def instructionsPause_redrawAll(app):
    
    drawImage(app.back, -20, 0, width = app.width + 20, height = app.height)
    
    drawLabel("INSTRUCTIONS", app.cameraWidth // 2, 50,
              fill = 'black', size = 30, bold = True)
    
    drawImage(app.front, app.cameraWidth // 2, app.cameraHeight // 2,
              width = app.cameraWidth - 130, height = app.cameraHeight - 220,
              align = 'center')
    
        
    drawLabel("Press 'Right' for Next, 'Left' for Previous and 'Enter' " +
              "to Return to Pause Menu", app.cameraWidth // 2,
              550, fill = 'black', size = 16, bold = True)
    
    
    
def instructionsPause_onKeyPress(app, key):
    
    if key == 'enter':
        
        setActiveScreen('pause')
        
    if key == 'right':
        
        app.displaying = app.g2
        app.front = openImage(app.displaying)
        app.front = CMUImage(app.front)
        
    if key == 'left':
        
        app.displaying = app.g1
        app.front = openImage(app.displaying)
        app.front = CMUImage(app.front)
    




### ************************************************************** ###



# this is the code for the instructions page on Main Menu

def instructions_onScreenActivate(app):
    
    app.back = openImage('instruction.jpg')
    app.back = CMUImage(app.back)
    app.g1 = 'guidelines1.jpg'
    app.g2 = 'guidelines2.jpg'
    app.displaying = app.g1
    app.front = openImage(app.displaying)
    app.front = CMUImage(app.front)
    
    
def instructions_redrawAll(app):
    
    drawImage(app.back, -20, 0, width = app.width + 20, height = app.height)
    
    drawLabel("INSTRUCTIONS", app.cameraWidth // 2, 50,
              fill = 'black', size = 30, bold = True)
    
    drawImage(app.front, app.cameraWidth // 2, app.cameraHeight // 2,
              width = app.cameraWidth - 130, height = app.cameraHeight - 220,
              align = 'center')
    
        
    drawLabel("Press 'Right' for Next, 'Left' for Previous and 'Enter' " +
              "to Return to Main Menu", app.cameraWidth // 2,
              550, fill = 'black', size = 16, bold = True)
    
    
    
def instructions_onKeyPress(app, key):
    
    if key == 'enter':
        
        setActiveScreen('start')
    
    if key == 'right':
        
        app.displaying = app.g2
        app.front = openImage(app.displaying)
        app.front = CMUImage(app.front)
        
    if key == 'left':
        
        app.displaying = app.g1
        app.front = openImage(app.displaying)
        app.front = CMUImage(app.front)



### ************************************************************** ###


# this is the code for the transition screen between levels



def transition_onScreenActivate(app):
    
    app.backLevel = openImage('transition.jpg')
    app.backLevel = CMUImage(app.backLevel)
    app.transitionMessage = f"Level {app.level} Complete!"
    
    app.nextLevelMessage = f"Get Ready for Level {app.level + 1}!"
    
    app.transitionTime = 1
    
    app.wheelX = 150
    app.wheelAngle = 0
    app.wheelIncrement = 5
    
    app.star1 = openImage('star1.png')
    app.star1 = CMUImage(app.star1)
    
    app.totalScore += app.targetScore
    
    if app.player1.health > 80:
        
        app.threeStars += 1
        
    app.sound = Sound('transitionSound.mp3')
    app.sound.play()



def transition_redrawAll(app):
    
    drawImage(app.backLevel, -1500, 0)
    
    drawRect(app.cameraWidth // 2, app.cameraHeight // 2 - 50, 400,
             60, align = 'center')
    
    drawLabel(app.transitionMessage, app.width // 2, app.height // 2 - 50,
              size=40, fill='white', bold=True)
    
    drawRect(app.cameraWidth // 2, app.cameraHeight // 2 + 50, 350,
             50, align = 'center', fill = 'white')
    drawLabel(app.nextLevelMessage, app.width // 2, app.height // 2 + 50,
              size=30, fill='gray', bold=True)
    
    # Draw Moving Wheel
    drawImage(app.imageWheel, app.wheelX , 500,
              width = app.wheelWidth // 2, height = app.wheelHeight // 2,
              align = 'center', rotateAngle = app.wheelAngle)
    
    
    # give star rating based on car's health in the previous level
    if 50 < app.player1.health <= 80:
        
        for i in range(2): 
            
            drawImage(app.star1, 80 + app.cameraWidth // 2 - 160 * i,
                      app.cameraHeight // 2 - 180,
                      width = 100, height = 100, align = 'center')
            
    elif 80 < app.player1.health:
        
        for i in range(3): 
            
            drawImage(app.star1, 150 + app.cameraWidth // 2 - 160 * i,
                      app.cameraHeight // 2 - 180,
                      width = 100, height = 100, align = 'center')
        
    elif 50 < app.player1.health <= 75:
    
        drawImage(app.star2, app.cameraWidth // 2 - 5,
                  app.cameraHeight // 2 - 180,
                  width = 200, height = 100, align = 'center')
        


def transition_onStep(app):
    
    app.transitionTime += 1
        
    if app.transitionTime > 150:
        
        app.score = 0
        app.blips = 0
        app.level += 1
        app.targetScore += 20
        app.penalty += 7
        app.player1.health = 100
        app.player1.velocity = 0
        app.turningSpeed += 0.5
        app.timeLimit += 4
        
        app.player1.maxSpeed += 5
        app.acceleration += 0.1
        
        generateCoins(app, numCoins = 10 + app.level * 2)
        
        app.sound.pause()
        setActiveScreen('game')

    
    # To move the wheel on the screen
    app.wheelAngle += 8
    
    if app.wheelX <= 100 or app.wheelX >= 700:
        
        app.wheelIncrement = -app.wheelIncrement
    
    app.wheelX += app.wheelIncrement

        
        

### ************************************************************** ###
    
    
    
# This is the code for displaying the completion of all levels

def gameWin_onScreenActivate(app):
    
    app.background = gradient('maroon', 'midnightBlue', start = 'left-top')
    app.gameWinner = openImage('gameWin.png')
    app.gameWinner = CMUImage(app.gameWinner)
    app.totalScore += app.score
    
    app.sound = Sound('gameWin.mp3')
    app.sound.play()



def gameWin_redrawAll(app):
    
    drawImage(app.gameWinner, app.cameraWidth // 4, 10,
              width = app.cameraWidth // 2, height = app.cameraHeight // 2)
    
    drawLabel("Congratulations!", app.width // 2, app.height // 2 + 10,
              size=40, fill='gold', bold=True)
    
    drawLabel("You have completed all levels!", app.width // 2,
              app.height // 2 + 100,
              size=20, fill='white', bold=True)
    
    drawLabel("Press 'r' to Return to Menu", app.width // 2, app.height - 50,
              size=15, fill='white', bold=True)
    
    drawLabel(f'Total Score: {app.totalScore}', app.width // 2,
            app.height // 2 + 160,
            size=  15, fill='wheat', bold=True)
    
    drawLabel(f'You completed {app.threeStars} level/s with Three Stars!',
              app.width // 2, app.height // 2 + 190, size=  15, fill='wheat',
              bold=True)



def gameWin_onKeyPress(app, key):
    
    if key == 'r':  # Restart the game
        
        app.level = 1
        app.player1.health = 100
        app.sound.pause()
        resetApp(app)
        setActiveScreen('start')
        
        
        
### ************************************************************** ###
    
    
    
# This is the code for displaying the 'Game Over' Screen

def gameOver_onScreenActivate(app):
    
    app.background = gradient('gray', 'black', start = 'center')
    app.gameLoser = openImage('gameOver.png')
    app.gameLoser = CMUImage(app.gameLoser)
    app.targetScore += app.score
    app.sound = Sound('gameOverSound.mp3')
    app.sound.play()


def gameOver_redrawAll(app):
    
    drawImage(app.gameLoser, app.cameraWidth // 4, 10,
              width = app.cameraWidth // 2, height = app.cameraHeight // 2)
    
    drawLabel("Tough Luck ...", app.width // 2, app.height // 2 + 10,
              size=40, fill='gold', bold=True)
    
    if app.player1.health <= 2:
        
        drawLabel("You lost all your health!", app.width // 2,
                app.height // 2 + 80,
                size=20, fill='white', bold=True)
            
    else:
        
        drawLabel("You ran out of time!", app.width // 2,
                app.height // 2 + 80,
                size=20, fill='white', bold=True)
        
    drawLabel(f'Total Score: {app.totalScore}', app.width // 2,
            app.height // 2 + 140,
            size=  15, fill='wheat', bold=True)
    drawLabel(f'You completed {app.threeStars} level/s with Three Stars.',
              app.width // 2, app.height // 2 + 170, size=  15, fill='wheat',
              bold=True)
    
    drawLabel("Press 'r' to Return to Menu", app.width // 2, app.height - 50,
              size=15, fill='white', bold=True)


def gameOver_onKeyPress(app, key):
    
    if key == 'r':  # Restart the game
        
        app.level = 1
        app.player1.health = 100
        app.sound.pause()
        resetApp(app)
        setActiveScreen('start')
        
        
        
### ************************************************************** ###


# this is the code for the main game            


def resetApp(app):
    
    # for drawing the track
    app.tracks = [('PittsburghSkeleton.png', 'Pittsburgh.png'),
                  ('DohaSkeleton.png', 'Doha.png'),
                  ('SrinagarSkeleton.png', 'Srinagar.png'),
                  ('LahoreSkeleton.png', 'Lahore.png')
                  ]
    
    app.trackSelected = app.tracks[0]
    app.track1Img = openImage(app.trackSelected[1])
    app.track1Img = CMUImage(app.track1Img)
    app.track1 = Track(app.track1Img, 0, 0)
    
    # for track's pixel related operations
    app.track11Img = openImage(app.trackSelected[0])
    app.rgbTrack = app.track11Img.convert("RGB")
    
    
    app.stepsPerSecond = 30
    # player's car
    app.player1 = Car(520, 530)
    
    # camera
    app.camera = Camera(app, 0, 0)
    app.cameraX, app.cameraY = app.camera.giveCamera()
    
    app.level = 1
    
    # timer
    app.blips = 0
    app.minutes = 0
    app.remainingSeconds = 0
    
    app.score = 0
    app.totalScore = 0
    app.threeStars = 0
    
    app.timeLimit = 30 # Time limit for each level
    app.targetScore = 30  # Coins required to pass the level
    
    # coin variables
    app.coins = []
    app.coinOscillation = 0.3
    
    # car variables
    app.friction = 0.07
    app.acceleration = 1.0
    app.turningSpeed = 9
    
    app.penalty = 20 # Health penalty for going off-track
    
    # variables for camera movement
    app.cameraWidth = 800
    app.cameraHeight = 600
    app.margin = 100
    
    # variables for map and mini map
    app.mapWidth = 2800
    app.mapHeight = 1600
    app.miniMapWidth = 160
    app.miniMapHeight = 120

    # for wheel animations
    app.imageWheel = openImage('Wheel.png')
    app.wheelWidth, app.wheelHeight = app.imageWheel.size
    app.imageWheel = CMUImage(app.imageWheel)


    # bonus features can be once only once in a game
    app.increaseHealth = True
    app.addCoins = True
    app.displayCoinMessage = False


def game_onStep(app):
    
    # for calculating time
    app.blips += 1
    app.seconds = int(2.2 * app.blips // app.stepsPerSecond)
    app.minutes = app.seconds // 60
    app.remainingSeconds = app.seconds % 60
    
    # for animating the coins
    for coin in app.coins:
        
        coin.vibrate(app)
        
    # Check off-track to deduct health and points
    if checkTrack(app, app.player1, app.track11Img, app.rgbTrack):
        
        app.player1.health -= 0.01 * app.penalty
        
        if app.player1.health <= 0:
            
            app.sound.pause()
            setActiveScreen('gameOver')

    # Check coin collisions
    checkCoinCollision(app)
    
    # Check level completion
    if app.score >= app.targetScore:
        
        if app.level >= 15:  # Last level
            
            app.sound.pause()
            setActiveScreen('gameWin')
            
        else:
            app.sound.pause()
            setActiveScreen('transition')

    # Check time or health expiration
    if app.seconds > app.timeLimit or app.player1.health <= 2:
        
        app.sound.pause()
        setActiveScreen('gameOver')


def onAppStart(app):
    
    resetApp(app)


def game_onScreenActivate(app):

    app.sound = Sound('gameSound.mp3')
    app.sound.play(restart = True, loop = True)
    app.track1Img = openImage(app.trackSelected[1])
    app.track1Img = CMUImage(app.track1Img)
    app.track1 = Track(app.track1Img, 0, 0)
    
    # for track's pixel related operations
    app.track11Img = openImage(app.trackSelected[0])
    app.rgbTrack = app.track11Img.convert("RGB")
    
    if app.totalScore == 0:
        
        generateCoins(app, numCoins = 10)
        
    
def game_onKeyPress(app, key):
    

    if key == "p":
        
        app.sound.pause()
        setActiveScreen('pause')
    
    if 'r' == key:
        
        app.sound.pause()
        resetApp(app)
        setActiveScreen('start')
    
    # increase health by 15 points
    if app.increaseHealth and 'space' == key:
        
        app.player1.health += 15
        app.increaseHealth = False
        
    if app.addCoins and 'c' == key:
        
        num = 0
        
        while num < 1:
            coin1X = random.randint(0, app.mapWidth)
            coin1Y = random.randint(0, app.mapHeight)
            
            coin2X = random.randint(0, app.mapWidth)
            coin2Y = random.randint(0, app.mapHeight)
            
            if (coinWithinTrack(coin1X, coin1Y,
                                app.track11Img, app.rgbTrack, app) and
                coinWithinTrack(coin2X, coin2Y,
                                app.track11Img, app.rgbTrack, app)):
                
                app.coins.extend([Coin(coin1X, coin1Y), Coin(coin2X, coin2Y)])
                num += 1
                
        app.addCoins = False
        app.displayCoinMessage = True
        

   
def game_onKeyHold(app, keys):
        
    app.player1.update(app, keys)
    

    

def game_onKeyRelease(app, keys):
    pass

# Draw timer on the screen
def drawTimer(app):
    
    if app.minutes < 10 and app.remainingSeconds < 10:
        
        drawLabel(f'0{app.minutes} : 0{app.remainingSeconds}',
                  app.width - 90, 50, fill = 'black', size = 28, bold = True)
        
    elif app.minutes >= 10 and app.remainingSeconds < 10:
        
        drawLabel(f'{app.minutes} : 0{app.remainingSeconds}',
                  app.width - 90, 50, fill = 'black', size = 28, bold = True)
        
    elif app.minutes >= 10 and app.remainingSeconds >= 10:
        
        drawLabel(f'0{app.minutes} : 0{app.remainingSeconds}',
                  app.width - 90, 50, fill = 'black', size = 28, bold = True)
        
    elif app.minutes < 10 and app.remainingSeconds >= 10:
        
        drawLabel(f'0{app.minutes} : {app.remainingSeconds}',
                  app.width - 90, 50, fill = 'black', size = 28, bold = True)
        
        
def game_redrawAll(app):
    
    # Draw the track
    app.track1.draw(app)

    # Draw the car
    app.player1.draw(app)
    
    # Draw all coins
    for coin in app.coins:
        
        coin.draw(app)
    
    # Display message if car is off-track
    if checkTrack(app, app.player1, app.track11Img, app.rgbTrack):
        
        drawRect(0, 0, app.cameraWidth, app.cameraHeight, fill = 'red',
                 opacity = 40)
        drawRect(app.cameraWidth // 2, app.cameraHeight // 2, 220, 40,
                 align = 'center', border = 'maroon')
        drawLabel('Ouch! Losing Health', app.cameraWidth // 2,
                  app.cameraHeight // 2, size = 20, fill = 'gold', bold = True)
    
    
    # Display timer and other important information
    drawRect(app.cameraWidth - 160, 20, 140, 120, fill='oldLace', border = None)
    drawTimer(app)
    drawLabel(f'Score: {app.score}', app.width - 90, 90, fill='maroon',
              size=18, bold=True)
    drawRect(20, 50, 200, 100, fill='oldLace', border = None)
    drawLabel(f"Target Score: {app.targetScore}", 85, 70, size = 15,
              fill = 'black', bold = True)
    drawLabel(f"Finish Within {app.timeLimit} seconds", 117, 100,
              size=15, fill='maroon', bold = True)
    
    if app.increaseHealth:
        
        drawLabel('Press Space to Boost Health', 109, 127,
                  size=12, fill='Green', bold = True)
        
    else:
        
        drawLabel('No Boost Health Bonus Left.', 111, 127,
                  size=12, fill='black', bold = True)
    
    # Display health bar
    drawRect(20, 20, 200, 20, fill='gray') 
    drawRect(20, 20, 2 * app.player1.health, 20, fill='red') 
    
    # Diplay Level
    drawRect(app.width // 2, 40, 140, 50, align = 'center', fill = 'oldLace',
             border = None)
    drawLabel(f"LEVEL {app.level}", app.width // 2, 40, size=30,
              fill='black', bold=True)
    
    if app.displayCoinMessage:
        
        drawLabel('Coin Boost Feature Exhausted', app.width // 2, 80, size=15,
                  fill='red', bold=True)
        

    # Mini map
    app.camera.drawMiniMap(app, app.player1)


    
        

runAppWithScreens(initialScreen = 'start', width = 800, height = 600)
