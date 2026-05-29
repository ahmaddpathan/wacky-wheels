Wacky Wheels - README


1) Project Description: Wacky Wheels is an exciting driving simulation game where players control a car to collect coins on a track while avoiding penalties for going off-track. 
The goal is to achieve the target score by collecting coins within the time limit for each level. Progress through increasingly challenging levels, each with higher targets and penalties. 
Maintain your car's health to avoid a game over!

2) How to Run the Project:

#### Prerequisites:
- Python Version: Ensure you have Python 3.7 or higher installed on your system.
- Required External Libraries:
  - `cmu_graphics` (for the game's graphics and animations)
  - `Pillow` (for image processing)

To install the required libraries, run the following commands in your terminal: pip install cmu-graphics pillow

#### Project Structure:
The project is divided into the following files:
- screens.py: Entry point of the game. Handles the main menu, screen transitions, and game orchestration.
- car.py: Contains the car class, including movement logic, collision detection, and drawing.
- coin.py: Manages the coins' generation, animations, and interactions.
- camera.py: Handles the camera view, mini-map functionalities and track-related functions.

Ensure all files are in the same directory.

#### Required Assets:

Place the following image and audio files in the same directory as the source code:

- Image Files:
  - `back.jpg` (Main menu background)
  - `loading.jpg` (Loading screen background)
  - `pause.jpg` (Pause menu background)
  - `instruction.jpg` (Instructions screen background)
  - `Wheel.png` (Wheel image for animations)
  - `gameOver.png` (Game over screen image)
  - `gameWin.png` (Winning screen image)
  - `star1.png` (Star icon for level ratings)
  - 'guidelines1.jpg' (game instructions)
  - 'guidelines2.jpg' (game instructions)
  - 'transition.jpg' (level completion screen background)
  - 'Pittsburgh.png' (track map)
  - 'PittsburghSkeleton.png' (track skeletion)
  - 'Doha.png' (track map)
  - 'DohaSkeleton.png' (track skeletion)
  - 'Srinagar.png' (track map)
  - 'SrinagarSkeleton.png' (track skeletion)
  - 'Lahore.png' (track map)
  - 'LahoreSkeleton.png' (track skeletion)

- Audio Files:
  - `startSound.mp3` (Main menu background music)
  - `transitionSound.mp3` (Sound effect for level transitions)
  - `gameSound.mp3` (Background music for gameplay)
  - `gameWin.mp3` (Sound effect for winning the game)
  - `gameOverSound.mp3` (Sound effect for game over)


#### Running the Game:
1. Open the `screens.py` file in your preferred Python IDE (e.g., VSCode, PyCharm, Thonny).
2. Run the script. The game will start with the main menu.


3) Installing Libraries: The project uses the following libraries: `cmu_graphics`, `PIL (Python Imaging Library)`, `math`, `random`, `os`, and `pathlib`. 
For installing the first two libraries (which are not built-in), refer to previous section.

4) Shortcut Commands: You can manually switch between screens by using the runAppWithScreens function in the source code and specifying the desired screen as initialScreen.
Available screens include: start, loading, game, pause, transition, trackSelection, gameOver, gameWin.



Notes:
The game is designed for full-screen mode (800x600 resolution).
Ensure all required image and audio files are in the same directory to avoid errors.