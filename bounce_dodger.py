import pygame
from pygame.locals import *
import sys
import time
import random

WIDTH = 800
HEIGHT = 600
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
DIRTY_GREEN = (0,137,59)
FPS = 60
score = 0
pspeed = 10

class Cherry:
	def __init__(self,bad):
		if (not bad):
			self.image = pygame.image.load("cherry.png")
		else:
			self.image = pygame.image.load("bad_cherry.png")

		self.rect = self.image.get_rect()
		self.rect.x = random.randint(0+50,WIDTH-50)
		self.rect.y = random.randint(0+50,HEIGHT-50)
		self.xdir = 10
		self.ydir = 10



	def move(self):
		global score 

		if score == 100:
			self.xdir *= (1+.3)
			self.ydir *= (1+.3)

		if (self.rect.y <= 0 or self.rect.y +20 >= HEIGHT):
			self.ydir *= -1
		if (self.rect.x <= 0 or self.rect.x +20 >= WIDTH ):
			self.xdir *= -1

		self.rect.move_ip(self.xdir,self.ydir)


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, BLACK)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont("Comic Sans MS",30)



screen = pygame.display.set_mode((WIDTH,HEIGHT),DOUBLEBUF)
pygame.display.set_caption("THE GAME")

square = pygame.Rect(0, 0, 50, 50)
my_cherry = Cherry(False)
evil_cherry = Cherry(True)


moving_right = moving_left = moving_up = moving_down = False
draw_collide = False

increasing = decreasing = False

while (True):
  # check for user input
	for event in pygame.event.get():
		if (event.type == pygame.QUIT):
		    sys.exit()
		if (event.type == KEYDOWN):
		  if (event.key == K_ESCAPE):
		    pygame.quit()
		    sys.exit()
		  elif (event.key == K_RIGHT):
		    moving_right = True
		  elif (event.key == K_LEFT):
		    moving_left = True
		  if (event.key == K_UP):
		    moving_up = True
		  elif (event.key == K_DOWN):
		    moving_down = True
		  if event.key == K_s:
		  	increasing = True
		  if event.key == K_a:
		  	decreasing = True

		if (event.type == KEYUP):
		  if (event.key == K_RIGHT):
		    moving_right = False
		  elif (event.key == K_LEFT):
		    moving_left = False
		  if (event.key == K_UP):
		    moving_up = False
		  elif (event.key == K_DOWN):
		    moving_down = False
		  if (event.key == K_s):
		   	increasing = False
		  elif (event.key == K_a):
		   	decreasing = False


    # update things based on input
	if (moving_right == True and square.x + 50 < WIDTH):
		square.move_ip(pspeed,0)
	elif (moving_left == True and square.x > 0):
		square.move_ip(-1*pspeed,0)
	if (moving_up == True and square.y > 0):
		square.move_ip(0,-1*pspeed)
	elif (moving_down == True and square.y + 50 < HEIGHT):
		square.move_ip(0,pspeed)

	if increasing:
		pspeed += 0.1
	if decreasing:
		pspeed -= 0.1

	my_cherry.move()
	evil_cherry.move()

# fill in up/down yourself
	if square.colliderect(my_cherry.rect):
		draw_collide = True
		score += 5

	if square.colliderect(evil_cherry.rect):
		score -= 5
	
	if (score <= -100):
		drawText("HAHAHAHA!!! YOU LOSEEEEEE!!!",font,screen,WIDTH/4, HEIGHT/2)
		pygame.display.update()
		time.sleep(5)
		pygame.quit()
		sys.exit()

	if (score >= 300):
		drawText("GG", font, screen, WIDTH/4,HEIGHT/2)
		pygame.display.update()
		time.sleep(5)
		sys.exit()
  # draw
	screen.fill(WHITE)
	pygame.draw.rect(screen, DIRTY_GREEN, square)
	screen.blit(my_cherry.image,my_cherry.rect)
	screen.blit(evil_cherry.image, evil_cherry.rect)
	if (draw_collide == True):
		drawText("Bam",font,screen,my_cherry.rect.x, my_cherry.rect.y)
		draw_collide = False
	score_str = "Score: " + str(score)
	drawText(score_str,font,screen,5,5)


	pygame.display.update()

	clock.tick(FPS)

pygame.quit()
sys.exit()