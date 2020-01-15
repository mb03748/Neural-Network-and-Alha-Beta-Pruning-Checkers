import sys, pygame, threading
from checkers import checkers
from computerPlayer import computerPlayer
from humanPlayer import humanPlayer
import numpy as np
from io import StringIO

pygame.init()

black = 0, 0, 0

height = 600

board = pygame.image.load("board.jpg")
board_rect = board.get_rect()
act_height = board_rect[-1]
new_width = board_rect[-2] * height // act_height
board_rect[-2:] = new_width, height

screen = pygame.display.set_mode(board_rect[-2:])

board = pygame.image.load("board.jpg").convert()
board = pygame.transform.scale(board, board_rect[-2:])

black = pygame.image.load("piece_black.png").convert_alpha()
white = pygame.image.load("piece_white.png").convert_alpha()
black_rect = black.get_rect()
white_rect = white.get_rect()

black_h = black_rect[-1] * height // act_height
white_h = white_rect[-1] * height // act_height
black_w = black_rect[-2] * height // act_height
white_w = white_rect[-2] * height // act_height

black_rect[-2:] = black_w, black_h
white_rect[-2:] = white_w, white_h

black = pygame.transform.scale(black, black_rect[-2:])
white = pygame.transform.scale(white, white_rect[-2:])

start_pos = 70
start_pos = start_pos * height / act_height

dist = 85
dist = dist * height / act_height

moveX = 844
moveY = 65
moveX2 = 965
moveY2 = 105
moveX = moveX * height / act_height
moveX2 = moveX2 * height / act_height
moveY = moveY * height / act_height
moveY2 = moveY2 * height / act_height

clearX = 845
clearY = 136
clearX2 = 960
clearY2 = 176
clearX = clearX * height / act_height
clearX2 = clearX2 * height / act_height
clearY = clearY * height / act_height
clearY2 = clearY2 * height / act_height

screen.blit(board, board_rect)
pygame.display.flip()

rect = pygame.Surface((int(dist),int(dist)))
rect.set_alpha(128)
rect.fill((255, 255, 255))

clicks = []
selectState = np.zeros(shape = (int(dist),int(dist)))

class pipe:
	def __init__(self):
		self.ready = False
		self.quit = False
		self.move = ""

pipE = pipe()

done = True

def makeTheMove(checkers):
	global done
	checkers.singleMove()
	done = True

c = checkers(humanPlayer(pipE), computerPlayer(3))
# c = checkers(computerPlayer(3), computerPlayer(3))


while True and c.currentState.hasEnded() == 0:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			pipE.quit = True
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			x,y = pygame.mouse.get_pos()
			if x >= moveX and x <= moveX2 and y >= moveY and y <= moveY2 and clicks:
				usersmove = " ".join([",".join(i) for i in clicks])
				pipE.move = usersmove
				pipE.ready = True
				clicks = []
				selectState[:, :] = 0
			elif x >= clearX and x <= clearX2 and y >= clearY and y <= clearY2:
				clicks = []
				selectState[:, :] = 0
			else:
				x = x - start_pos
				y = y - start_pos
				x = int(x // dist)
				y = int(y // dist)
				if x >= 0 and x <= 7 and y >= 0 and y <= 7:
					clicks.append([str(y),str(x)])
					selectState[y, x] = 1


	screen.blit(board, board_rect)

	if done:
		state = c.getState()
		done = False
		t = threading.Thread(target = makeTheMove, args = (c,))
		t.start()
		
	for i in range(state.shape[0]):
		for j in range(state.shape[1]):
			if state[i][j] > 0:
				temp_rect = white_rect.copy()
				temp_rect.x = dist * j + start_pos
				temp_rect.y = dist * i + start_pos
				screen.blit(white, temp_rect)
				if state[i][j] == 3:
					pos = [int(temp_rect.x + temp_rect.w / 2), int(temp_rect.y + temp_rect.h / 2)]
					pygame.draw.circle(screen, (0,0,255), pos, int(dist // 3), 2)
			elif state[i][j] < 0:
				temp_rect = black_rect.copy()
				temp_rect.x = dist * j + start_pos
				temp_rect.y = dist * i + start_pos
				screen.blit(black, temp_rect)
				if state[i][j] == -3:
					pos = [int(temp_rect.x + temp_rect.w / 2), int(temp_rect.y + temp_rect.h / 2)]
					pygame.draw.circle(screen, (0,0,255), pos, int(dist // 3), 2)
			if selectState[i, j] == 1:
				screen.blit(rect, (int(dist * j + start_pos), int(dist * i + start_pos)))
				
			
	pygame.display.flip()

if c.currentState.hasEnded() == 1:
	print("Victory for Player 1")
else:
	print("Victory for Player 2")
