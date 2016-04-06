import math
import random
import pygame

random.seed()
pygame.init()

class Segway:

    segwayImg = pygame.image.load('assets/segway.png')

    def __init__(self, xP, yP, xS, yS, dW, dH):
        self.xPos = xP
        self.yPos = yP
        self.xSize = xS
        self.ySize = yS
        self.display_width = dW
        self.dispaly_height = dH
        self.acceleration = 0.15;
        self.velocity = 0
        self.slowFactor = 0.50;

    def move(self, direction):
        self.velocity += self.acceleration*direction

    def update(self, slow):
        if slow:
            if self.xPos + self.xSize + self.velocity*self.slowFactor > display_width or self.xPos + self.velocity*self.slowFactor < 0:
                self.velocity = -self.velocity

            self.xPos += self.velocity*self.slowFactor
        else:
            if self.xPos + self.xSize + self.velocity > display_width or self.xPos + self.velocity < 0:
                self.velocity = -self.velocity

            self.xPos += self.velocity

    def draw(self, display):
        display.blit(self.segwayImg, (self.xPos, self.yPos))

class Ship:

    shipImg = pygame.image.load('assets/ship.png')

    def __init__(self, xP, yP, xS, yS, S, dW, dH):
        self.xPos = xP
        self.yPos = yP
        self.xSize = xS
        self.ySize = yS
        self.velocity = S;
        self.display_width = dW
        self.display_height = dH
        self.slowFactor = 0.45;

    def move(self, slow):
        if slow:
            self.yPos += self.velocity*self.slowFactor
        else:
            self.yPos += self.velocity

        if self.yPos > self.display_height:
            return True
        return False

    def collision(self, xPos, yPos, xSize, ySize):
        if self.xPos + self.xSize > xPos and self.xPos < xPos + xSize and self.yPos + self.ySize > yPos and self.yPos < yPos + ySize:
            return True
        return False

    def draw(self, display):
        display.blit(self.shipImg, (self.xPos, self.yPos))

color_white = (255, 255, 255)
color_black = (0, 0, 0)

display_width = 800
display_height = 600

#create game window
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('SlowMo')
clock = pygame.time.Clock()

gameOver = False
key_a = False
key_d = False
key_space = False

#game variables
player = Segway(display_width/2 - 14.5, display_height - 50, 29, 42, display_width, display_height)

enemies = []
enemySpawnTimer = 400
enemyTimePassed = enemySpawnTimer - enemySpawnTimer*0.25
enemyAverageSpeed = 1
expvar = -1;

while not gameOver:

    #user try closing the game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

        #print(event)

        #user controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                key_a = True
            if event.key == pygame.K_d:
                key_d = True
            if event.key == pygame.K_SPACE:
                key_space = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                key_a = False
            if event.key == pygame.K_d:
                key_d = False
            if event.key == pygame.K_SPACE:
                key_space = False

    #clears the display
    gameDisplay.fill(color_black)

    if enemyTimePassed > enemySpawnTimer and len(enemies) < 25:
        enemies.append(Ship(random.randint(0, display_width - 20), -15, 15, 20, random.uniform(enemyAverageSpeed - enemyAverageSpeed*0.15, enemyAverageSpeed + enemyAverageSpeed*0.15), display_width, display_height))
        enemyTimePassed = 0
        enemySpawnTimer -= math.pow(2, expvar)*enemySpawnTimer
        #enemySpawnTimer -= math.pow(2, expvar)*random.uniform(enemySpawnTimer*0.05, enemySpawnTimer*0.15)
        enemyAverageSpeed += 0.05
        expvar -= 1
    enemyTimePassed += 1

    if key_a:
        player.move(-1)
    if key_d:
        player.move(1)

    if key_space:
        player.update(True)
    else:
        player.update(False)

    for enemy in enemies:
        if key_space:
            if enemy.move(True):
                enemies.remove(enemy)
        else:
            if enemy.move(False):
                enemies.remove(enemy)
        if enemy.collision(player.xPos, player.yPos, player.xSize, player.ySize):
            gameOver = True
            #print("Collision")
        enemy.draw(gameDisplay)

    player.draw(gameDisplay)

    #draws on the display
    pygame.display.update()

    #set fps to 60
    clock.tick(60)

#exit window and program
pygame.quit()
quit()

