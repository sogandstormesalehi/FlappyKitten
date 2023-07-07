import pygame
import random

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512
display_height = 0.80 * HEIGHT

pygame.mixer.init()
wing_sound = pygame.mixer.Sound('Assets/Sounds\wing.wav')

class Grumpy:
	def __init__(self, win):
		self.win = win
		self.images = []
		num = random.choice(['1', '2', '3'])
		for i in range(1, 4):
			img = pygame.image.load(f'Assets/kitten/{num}{i}.png')
			img = pygame.transform.scale(img, (48, 40))
			self.images.append(img)
		self.reset()

	def update(self):
		self.vel += 0.3
		if self.vel >= 8:
			self.vel = 8
		if self.rect.bottom <= display_height:
			self.rect.y += int(self.vel)
		
		if self.alive:
			if pygame.mouse.get_pressed()[0] == 1 and not self.jumped:
				wing_sound.play()
				self.jumped = True
				self.vel = -6
			if pygame.mouse.get_pressed()[0] == 0:
				self.jumped = False
			
			self.animate_flap()
			
			self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
		else:
			if self.rect.bottom <= display_height:
				self.theta -= 2
			self.image = pygame.transform.rotate(self.images[self.index], self.theta)
			
		self.win.blit(self.image, self.rect)
		
	def animate_flap(self):
		self.counter = (self.counter + 1) % 6
		self.index = self.counter // 2
			
	def draw_flap(self):
		self.animate_flap()
		if self.flap_pos <= -10 or self.flap_pos > 10:
			self.flap_inc *= -1
		self.flap_pos += self.flap_inc
		self.rect.y += self.flap_inc
		self.rect.x = WIDTH // 2 - 20
		self.image = self.images[self.index]
		self.win.blit(self.image, self.rect)
		
	def reset(self):
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = 60
		self.rect.y = int(display_height) // 2
		self.counter = 0
		self.vel = 0
		self.jumped = False
		self.alive = True
		self.theta = 0
		self.mid_pos = display_height // 2
		self.flap_pos = 0
		self.flap_inc = 1

class Base:
	def __init__(self, win):
		self.win = win
		self.image1 = pygame.image.load('Assets/base.png')
		self.image2 = self.image1
		self.rect1 = self.image1.get_rect()
		self.rect1.x = 0
		self.rect1.y = int(display_height)
		self.rect2 = self.image2.get_rect()
		self.rect2.x = WIDTH
		self.rect2.y = int(display_height)
		
	def update(self, speed):
		self.rect1.x -= speed
		self.rect2.x -= speed
		
		if self.rect1.right <= 0:
			self.rect1.x = WIDTH - 5
		if self.rect2.right <= 0:
			self.rect2.x = WIDTH - 5

class Pipe(pygame.sprite.Sprite):
	def __init__(self, win, image, y, position):
		super(Pipe, self).__init__()
		self.win = win
		self.image = image
		self.rect = self.image.get_rect()
		pipe_gap = 100 // 2
		x = WIDTH

		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect.bottomleft = (x, y - 1.2 * pipe_gap)
		elif position == -1:
			self.rect.topleft = (x, y + 1.2 * pipe_gap)
		
	def update(self, speed):
		self.rect.x -= speed
		if self.rect.right < 0:
			self.kill()
		self.win.blit(self.image, self.rect)
		
class Score:
	def __init__(self, x, y, win):
		self.score_images = []
		for score in range(10):
			img = pygame.image.load(f'Assets/scores/{score}.png')
			self.score_images.append(img)
		self.x = x
		self.y = y
		self.win = win
		
	def update(self, score):
		score_str = str(score)
		for index, num in enumerate(score_str):
			image = self.score_images[int(num)]
			rect = image.get_rect()
			rect.topleft = self.x - 15 * len(score_str) + 30 * index, self.y
			self.win.blit(image, rect)
