import pygame, sys, time, random
from pygame.locals import *
#create player class with movement and update method
class Player():
    def __init__(self):
        self.x = [0]
        self.y = [0]
        for i in range(100):
            self.x.append(-100)
            self.y.append(-100)
        self.speed = 20
        self.length = 3
        self.direction = "right"
        self.updatemax = 2
        self.updatecount = 0
        self.sleep = 0.1
    #sets the direction of the snake attribute, up method makes it goes up etc.
    def up(self):
        self.direction = "up"

    def down(self):
        self.direction = "down"

    def left(self):
        self.direction = "left"

    def right(self):
        self.direction = "right"
    # updates the snake by looping thru each block and replacing that block with the previous block
    # it updates the coordinates of the head of the snake via a set speed variable and the direction variable.
    def update(self):
        self.updatecount += 1
        if self.updatecount > self.updatemax:
            for i in range(self.length - 1, 0, -1):
                self.x[i] = self.x[i - 1]
                self.y[i] = self.y[i - 1]
            if self.direction == "up":
                self.y[0] -= self.speed

            if self.direction == "down":
                self.y[0] += self.speed

            if self.direction == "left":
                self.x[0] -= self.speed

            if self.direction == "right":
                self.x[0] += self.speed
    # method to draw the snake
    def draw(self, image, surface):
        for i in range(0, self.length):
            surface.blit(image, (self.x[i], self.y[i]))
# class for the score
class Score():
    def __init__(self, number = 0):
        self.number = number


# checks whether the snake has collided with something
class Collision():
    # simple method to check is coordinates are the same
    def collisioncheck(self, x, y, x2, y2):
        collided = False
        if x == x2 and y == y2:
            collided = True
        return collided
# spawns the food
class Food():
    def __init__(self, x, y):
        self.player = Player()
        self.x = self.player.speed * x
        self.y = self.player.speed * y

    def draw(self, image, surface):
        surface.blit(image, (self.x, self.y))
# main game class
class Game():
    # intialise all variables need for the game to function
    def __init__(self):
        self.width = 500
        self.height = 500

        self.check = True
        self.player = Player()
        self.surf = pygame.Surface((15, 15))
        self.displayer = None
        self.collision = Collision()
        self.food = Food(random.randint(2, self.width/self.player.speed - 2), random.randint(2, self.height/self.player.speed - 2))
        self.apple = pygame.Surface((15, 15))
        self.score = Score()

    def physics(self):
        self.player.update()
        # checks if the snake has collided with any part of it's body, if true, the game ends.
        for i in range(1, self.player.length):
            if self.collision.collisioncheck(self.player.x[0], self.player.y[0], self.player.x[i], self.player.y[i]):
                print("Mission failed, we're get them next time.")
                self.endgame()
        # checks if the snake has collided with the game windows, if true than move it to opposite edge.
        for i in range(self.player.length):
            if self.player.x[i] > self.width:
                self.player.x[i] = 0

            elif self.player.x[i] < 0:
                self.player.x[i] = self.width

            if self.player.y[i] > self.height:
                self.player.y[i] = 0

            elif self.player.y[i] < 0:
                self.player.y[i] = self.height
        # checks if the snake has collided wit the food, if true despawn the food and increase length and score by 1
        if self.collision.collisioncheck(self.player.x[0], self.player.y[0], self.food.x, self.food.y):
            self.player.length += 1
            self.food.x = random.randint(2, (self.width/self.player.speed - 2)) * self.player.speed
            self.food.y = random.randint(2, (self.height/self.player.speed - 2)) * self.player.speed
            self.score.number += 1

    def reset(self):
        self.player = Player()
        self.score.number = 0
    # ends the game, shows the score and asks if you want to restart.

    def endgame(self):
        run = True
        mediumfont = pygame.font.SysFont("arial", 50)
        largefont = pygame.font.SysFont("arial", 80)
        current = largefont.render("Score: "+str(self.score.number), 1, (255, 255, 0))
        playagain = mediumfont.render("Click to play again", 1, (255, 255, 0))
        while run:
            self.displayer.blit(current, (250 - current.get_width()/2, 220 - current.get_height()/2))
            self.displayer.blit(playagain, (250 - playagain.get_width()/2, 280 - playagain.get_height()/2))
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    pygame.quit()

                elif i.type == pygame.MOUSEBUTTONDOWN:
                    self.reset()
                    run = False

            pygame.display.flip()



    # starts the game
    def switch(self):
        pygame.init()
        self.displayer = pygame.display.set_mode((self.width, self.height), pygame.HWSURFACE)
        self.check = True

    # renders the objects
    def render(self):
        self.displayer.fill((0, 0, 0))
        self.surf.fill((255, 255, 255))
        self.apple.fill((255, 0, 0))
        self.player.draw(self.surf, self.displayer)
        self.food.draw(self.apple, self.displayer)
        smallfont = pygame.font.SysFont("arial", 20)
        text = smallfont.render("Score: "+str(self.score.number), 1, (255, 255, 255))
        self.displayer.blit(text, (10, 10))

        pygame.display.flip()

    # main game loop
    def on(self):
        self.switch()
        while (self.check):
            time.sleep(self.player.sleep)
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if (keys[K_ESCAPE]):
                self.check = False

            if (keys[K_RIGHT] or keys[K_LEFT] or keys[K_UP] or keys[K_DOWN]):
                self.check = False
                print("You're not a gamer")

            if (keys[K_w] and self.player.direction != "down"):
                self.player.up()

            if (keys[K_a] and self.player.direction != "right"):
                self.player.left()

            if (keys[K_s] and self.player.direction != "up"):
                self.player.down()

            if (keys[K_d] and self.player.direction != "left"):
                self.player.right()
            self.physics()

            self.render()
        pygame.quit()


game = Game()
game.on()