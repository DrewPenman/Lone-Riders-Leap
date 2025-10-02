#-------------------------------------------------------------------------------
# Name:        Lone Rider's Leap

# Created:     05/01/2024
# Copyright:   Creative Common BY-NC-SA 3.0 Licence 2024
#-------------------------------------------------------------------------------
#!/usr/bin/env python

#importing modules
import pygame
import random

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
CHARACTER_START_X = 0
CHARACTER_START_Y = 210
CHARACTER_DEATH_Y = 425
MAX_X_POSITION = 950
MOVEMENT_SPEED = 5
JUMP_SPEED = 6
MAX_GRAVITY = 13
GRAVITY_INCREMENT = 0.5
FPS = 20

#Storing the intial platform positions
platformXPos = [0, 150, 250, 350, 450, 550, 650, 750, 850, 950]
platformYPos = [250, 240, 240, 260, 230, 230, 250, 250, 260, 250, 250, 235, 240, 245, 260, 260, 255, 235, 245, 250]
coinXpos = [665,165,455]
coinYpos = [235,215,240]
tumbleweedxPos = [950,260,600,400]
tumbleweedyPos = [220,240,240,150]

# Define objects (sprites) here
class platform(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([50,20])        # Create a surface on which to display grahics.
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()              # Set a colour to be transparent.


    def displayPlatform(self,x,y):
        self.rect.width = 35
        self.rect.height = 5    # These lines create the rectangular sprite,
        self.rect.x = x                             # the same size as the image surface and then
        self.rect.y = y                             # assigns it coordinates.


    def type(self,image):
        type = pygame.image.load(image)             # Load in the passed image file
        self.image.blit(type,(0,0))

class Text(pygame.sprite.Sprite):
    def __init__(self,type,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([x,y])
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()

        if type == "UI/victory.png":
            self.rect.x = 320
            self.rect.y = 200
        if type == "UI/Lone Rider's Leap.png":
            self.rect.x = 300
            self.rect.y = 35

        self.image.blit(pygame.image.load(type),(0,0))

class collectable(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([20,20])
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.rect.width = 10
        self.rect.height = 10
        self.image.blit(pygame.image.load("collectables/coin.png"),(0,0))

    def movement(self):
        self.rect.y -= 1

        if self.rect.y <= self.y - 5:
            self.rect.y += 5


class Tumbleweed(pygame.sprite.Sprite):
    def __init__(self,image):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.Surface([20,20])
       self.image.set_colorkey(black)
       self.rect = self.image.get_rect()
       self.rect.x = 950
       self.rect.y = 230
       self.image.blit(pygame.image.load(image),(0,0))
       
       # Set speed based on enemy type
       if image == "enemies/Tumbleweed.png":
           self.speed = 3
       elif image == "enemies/bat.png":
           self.speed = 2
       
       # Track direction as instance variable
       self.direction = "left"


    def movement(self):
        # Reverse direction at boundaries
        if self.rect.x <= 45:
            self.direction = "right"
        elif self.rect.x >= 945:
            self.direction = "left"

        # Move in current direction
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

    def position(self,x,y):
        self.rect.x = x
        self.rect.y = y

class Heart(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([32,32])
        self.image.set_colorkey(black)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.blit(pygame.image.load("UI/Heart.png"),(0,0))


class Character(pygame.sprite.Sprite):
     def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([36,42])
        self.image.set_colorkey(black)

        self.rect = self.image.get_rect()
        self.rect.x = CHARACTER_START_X
        self.rect.y = 207

        self.rect.width = 36
        self.rect.height = 42
        
        # Cache images to avoid repeated loading
        self.image_right = pygame.image.load("character/character-right.png")
        self.image_left = pygame.image.load("character/character-left.png")
        self.image.blit(self.image_right,(0,0))

     def imgDirection(self,direction):
        if direction == "left":
            self.image.blit(self.image_left,(0,0))
        elif direction == "right":
            self.image.blit(self.image_right,(0,0))


     def moveCharacter(self,movement,vertMovement):
        # Update position with bounds checking
        self.rect.x += movement
        self.rect.x = max(0, min(self.rect.x, MAX_X_POSITION))
        
        if vertMovement > 0:
            self.rect.y -= vertMovement

     def startingPos(self):
         self.rect.y = CHARACTER_START_Y
         self.rect.x = CHARACTER_START_X
         self.image.blit(self.image_right,(0,0))

     def gravity(self,rate,lives):
        self.rect.y += rate
        if self.rect.y >= CHARACTER_DEATH_Y:
            deathsound.play()
            self.rect.y = CHARACTER_START_Y
            self.rect.x = CHARACTER_START_X
            self.image.blit(self.image_right,(0,0))
            lives -= 1
        return lives


pygame.init()                               # Pygame is initialised (starts running)
pygame.mixer.init()
screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT]) # Set the width and height of the screen [width,height]
pygame.display.set_caption("Lone Rider's Leap")  # Name your window
background_image = pygame.image.load("backgrounds/DesertBackground.jpg").convert() # sets level 1 background to the desert.jpg
done = False
state = ""
clock = pygame.time.Clock()
black    = (   0,   0,   0)                 # Define some colors using rgb values.  These can be
white    = ( 255, 255, 255)                # used throughout the game instead of using rgb values.

#loading audio
backgroundmusic = pygame.mixer.Sound("music/background_music.wav") #loads in the music for the loading screen
item_collection = pygame.mixer.Sound("music/collectionSound.wav") #Loads item collection sound
jumpingsound = pygame.mixer.Sound("music/jump.wav")
walkingsound = pygame.mixer.Sound("music/walking.wav")
deathsound = pygame.mixer.Sound("music/deathSound.wav")

# Define additional Functions and Procedures here
platforms = pygame.sprite.Group() #creates a group for all plaforms
endPlatform = pygame.sprite.Group() #Adds the last platform to the group endPlatform

#Creates a variable character and adds it to the charactersGroup group
character = Character()
charactersGroup = pygame.sprite.Group()
charactersGroup.add(character)

#Creating coin collectable and pasing in the coordinates
coin = collectable(coinXpos[0],230)

#Creating and adding coins to group for collectables
collectables = pygame.sprite.Group()
collectables.add(coin)

#Creating enemy group
tumbleweed = Tumbleweed("enemies/Tumbleweed.png")
enemies = pygame.sprite.Group()
enemies.add(tumbleweed)

#creating heart group
hearts = pygame.sprite.Group()

#initialising variables
state = ""
collected = 0
level = "start"
if level == "start":
    #Adding in each of the level 1 desert plaforms by iterating through each elments within the group
    for index in range(0,10):
        nextObject = platform()
        nextObject.type("platforms/desert_platform.png")
        nextObject.displayPlatform(platformXPos[index],250)
        platforms.add(nextObject)
        if index == 9:
            endPlatform.add(nextObject)

    #Create and draw screen text,graphics and audio
    textType = "UI/Lone Rider's Leap.png"
    titleTxt = Text(textType,403,47)
    Title = pygame.sprite.Group()
    Title.add(titleTxt)

    #Loading in elements
    font = pygame.font.Font(None,60)
    screen.blit(background_image,[0,0])

    #Displays all elements
    font = pygame.font.Font(None,28)
    clickWindow = font.render("Click the window to start",1,black)
    screen.blit(clickWindow,(350,430))
    Title.draw(screen)

    #Starts the background music
    backgroundmusic.play(-1)

    #Update the screen
    pygame.display.flip()

    #Determine when the screen has been clicked
    while done == False:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                done = True
                state = "level 1"
                backgroundmusic.stop()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    done = False
    screen.fill(black)

#Initialising Variables
lives = 1
movement = 0
vertMovement = 0
increment = 0
gravity = 0
level = "1"
direction = "left"

# -------- Main Program Loop (Game Window - Levels) -----------
while done == False and state == "level 1":

    for event in pygame.event.get():       # Check for an event (mouse click, key press)
        if event.type == pygame.QUIT: #closes the game      # If user clicks close window game is closed
            pygame.quit()
            quit()

        #Detecting key presses for movement of the character
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                movement = -MOVEMENT_SPEED
                direction = "left"
                character.imgDirection(direction)
                walkingsound.play()
            elif event.key == pygame.K_RIGHT:
                movement = MOVEMENT_SPEED
                direction = "right"
                character.imgDirection(direction)
                walkingsound.play()
            elif event.key == pygame.K_UP:
                vertMovement = JUMP_SPEED
                jumpingsound.play()

        if event.type == pygame.KEYUP:
            movement = 0
            vertMovement = 0

    #Movement of sprites
    character.moveCharacter(movement,vertMovement)
    for coins in collectables:
        coins.movement()

    for enemy in enemies:
        enemy.movement()

    #Detecting the collision between platforms and the character
    platform_collisions = pygame.sprite.groupcollide(platforms,charactersGroup,False,False)

    #Activating gravity
    if len(platform_collisions) < 1:
        if gravity < MAX_GRAVITY:
            gravity += GRAVITY_INCREMENT
        lives = character.gravity(gravity,lives)

    #Disabling gravity on platform
    if len(platform_collisions) > 0:
        gravity = 0
        lives = character.gravity(gravity,lives)

    #Detecting the colllision of character and collectables
    collectable_collisions = pygame.sprite.groupcollide(charactersGroup,collectables,False,True)
    if len(collectable_collisions) > 0 :
        item_collection.play()
        collected += 1
        lives = lives + 1

    #Detecting the collision between the character and platform
    end_platform_collisions = pygame.sprite.groupcollide(charactersGroup,endPlatform,False,False)
    if len(end_platform_collisions) > 0:
        if level == "1" and collected == 1:
            level = 2
        elif level == "2current":
            level = 3
        elif level == "3current":
            level = "complete"

    enemy_collisions = pygame.sprite.groupcollide(enemies,charactersGroup,False,False)
    if len(enemy_collisions) > 0:
        deathsound.play()
        character.startingPos()
        lives = lives - 1

    #Creation of each level
    #Starting Level 1
    if level == "1":
        levelText = font.render("Level 1 - Deserted Desert",1,black)


    #Changing level to level 2
    if level == 2:
        #Setting up background and and character for next level
        background_image = pygame.image.load("backgrounds/mountain(changed).jpg").convert()
        character.startingPos()
        level = "2current"
        levelText = font.render("Level 2 - Deserted Dunes",1,black)
        endPlatform.empty()
        enemies.empty()
        level2Coin = collectable(coinXpos[1],220)
        collectables.add(coin)
        collectables.add(level2Coin)

        for index in range(0,2):
            nextObject = Tumbleweed("enemies/Tumbleweed.png")
            enemies.add(nextObject)
            if index == 1:
                nextObject.position(260,220)

        #Adjusting position of the platforms for new level
        index = 0
        #Changing all the platforms to level 2 plaforms
        for object in platforms:
            object.type("platforms/mountain_platform.png")
            object.displayPlatform(platformXPos[index],platformYPos[index])
            index += 1
            #Adding last plaform to the end platform group
            if index == 10:
                endPlatform.add(object)

    #Resetting index to zero
    index = 0

    #Changing to level 3
    if level == 3:
        #Setting up background and character for next level
        background_image = pygame.image.load("backgrounds/cave(changed).jpg").convert()
        #Moving character back to the starting position
        character.startingPos()
        enemies.empty()
        endPlatform.empty()
        level = "3current"
        levelText = font.render("Level 3 - Cursed Caves",1,white)
        #Changing the plaforms to level 3 platforms
        for object in platforms:
            object.type("platforms/cave_plaform.png")
            object.displayPlatform(platformXPos[index] ,platformYPos[index + 10])
            if index == 9:
                endPlatform.add(object)
            index += 1

        for index in range(0,4):
            if index <= 2:
                nextObject = Tumbleweed("enemies/Tumbleweed.png")

            if index == 3:
                nextObject = Tumbleweed("enemies/bat.png")

            enemies.add(nextObject)
            nextObject.position(tumbleweedxPos[index],tumbleweedyPos[index])

        for index in range(0,3):
            nextObject = collectable(coinXpos[index],coinYpos[index])
            collectables.add(nextObject)

    hearts.empty()
    increment = 0
    for index in range(0,lives):
        nextObject = Heart(15 + increment,5)
        hearts.add(nextObject)
        increment += 45

    if lives == 0:
        pygame.quit()
        quit()

    if level == "complete":
        textType = "UI/victory.png"
        levelText = font.render("",1,black)
        enemies.empty()
        platforms.empty()
        charactersGroup.empty()
        collectables.empty()
        hearts.empty()
        background_image = pygame.image.load("backgrounds/winner.jpg")
        victory = Text(textType,376,79)
        winner = pygame.sprite.Group()
        winner.add(victory)

    # Update sprites here
    screen.blit(background_image, [0,0])
    if level == "complete":
        winner.draw(screen)

    #Drawing elements
    screen.blit(levelText, (380,15))
    hearts.draw(screen)
    charactersGroup.draw(screen)
    platforms.draw(screen)
    collectables.draw(screen)
    enemies.draw(screen)
    pygame.display.flip()                   # updates the screen with what's been drawn
    clock.tick(FPS)                          # Limit to 20 frames per second