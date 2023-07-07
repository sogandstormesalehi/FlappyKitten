import pygame
import random
from prefabs import Grumpy, Pipe, Base, Score

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512
display_height = 0.80 * HEIGHT
info = pygame.display.Info()
pygame.mixer.music.load('Assets\Sounds\mixkit-game-level-music-689.wav') 
pygame.mixer.music.play(-1)

win_mode = pygame.NOFRAME if info.current_w >= info.current_h else pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN
win = pygame.display.set_mode(SCREEN, win_mode)

clock = pygame.time.Clock()
FPS = 60

bg = pygame.image.load('Assets/background1.png')

pipe_img = pygame.image.load('Assets/icicle.png')

gameover_img = pygame.image.load('Assets/tryagain.png')
flappybird_img = pygame.transform.scale(pygame.image.load('Assets/flappykitten.png'), (200, 80))

die_fx = pygame.mixer.Sound('Assets/Sounds/die.wav')
hit_fx = pygame.mixer.Sound('Assets/Sounds/hit.wav')
point_fx = pygame.mixer.Sound('Assets/Sounds/point.wav')
swoosh_fx = pygame.mixer.Sound('Assets/Sounds/swoosh.wav')
wing_fx = pygame.mixer.Sound('Assets/Sounds/wing.wav')

pipe_group = pygame.sprite.Group()
base = Base(win)
score_display = Score(WIDTH // 2, 50, win)
grumpy = Grumpy(win)

speed = 0
game_started = False
game_over = False
score = 0
start_screen = True
pipe_pass = False
pipe_frequency = 1600

running = True
while running:
	win.blit(bg, (0, 0))
	
	if start_screen:
		speed = 0
		grumpy.draw_flap()
		base.update(speed)
		
		win.blit(flappybird_img, (40, 50))
	else:
		if game_started and not game_over:
			next_pipe = pygame.time.get_ticks()
			if next_pipe - last_pipe >= pipe_frequency:
				y = display_height // 2
				pipe_pos = random.choice(range(-100, 101, 4))
				height = y + pipe_pos
				
				top = Pipe(win, pipe_img, height, 1)
				bottom = Pipe(win, pipe_img, height, -1)
				pipe_group.add(top)
				pipe_group.add(bottom)
				last_pipe = next_pipe
		
		pipe_group.update(speed)
		base.update(speed)
		grumpy.update()
		score_display.update(score)
		
		if pygame.sprite.spritecollide(grumpy, pipe_group, False) or grumpy.rect.top <= 0:
			game_started = False
			if grumpy.alive:
				hit_fx.play()
				die_fx.play()
			grumpy.alive = False
			grumpy.theta = grumpy.vel * -2
	
		if grumpy.rect.bottom >= display_height:
			speed = 0
			game_over = True
	
		if len(pipe_group) > 0:
			p = pipe_group.sprites()[0]
			if grumpy.rect.left > p.rect.left and grumpy.rect.right < p.rect.right and not pipe_pass and grumpy.alive:
				pipe_pass = True
	
			if pipe_pass:
				if grumpy.rect.left > p.rect.right:
					pipe_pass = False
					score += 1
					point_fx.play()
					
	if not grumpy.alive:
		win.blit(gameover_img, (50, 200))
		
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if start_screen:
				game_started = True
				speed = 2
				start_screen = False

				game_over = False
				last_pipe = pygame.time.get_ticks() - pipe_frequency
				next_pipe = 0
				pipe_group.empty()
				score = 0
				
			if game_over:
				start_screen = True
				grumpy = Grumpy(win)
				
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()
