import pygame
import math
from queue import PriorityQueue

WIDTH = 400
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)                                                        # defining RGB colors
GREEN = (0, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:                                                                #spot here is node 
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):                                                                            #making rectangle  window
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):                                          #to make sure that any start and end node does not have a barrier as a neighbour
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():                            # DOWN grid spot
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():                              # UP grid spot      
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():        # RIGHT grid spot
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():                              # LEFT  grid spot
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):                            #lt means less than
		return False


def h(p1, p2):                      # defining heuristic function
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)         #p2=(1,9)  this will give x2=1 and y2 = 9 value
                       

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]                   # current is where we have came last from
		current.make_path()
		draw()


def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()              # make a open set where all the possible nodes are put
	open_set.put((0, count, start))         #to get f(n) value from f(n)= G(n) + h(n)     
	came_from = {}                                   # which node we have come from 
	g_score = {spot: float("inf") for row in grid for spot in row}                                # to make G(n) value as infinity at starting using "inf"
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())                                 # f(n) value as get to be heuristic

	open_set_hash = {start}                                           # to keep track all the items are in priorityqueue or not

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]                             # when we click right button of mouse
		open_set_hash.remove(current)                      # to remove the node we have marked as a barrier or anything

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:                    # to get the optimal path
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())               # get_pos() will give row and col value
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def make_grid(rows, width):
	grid = []
	gap = width // rows                 # to make the gap between two rows
	for i in range(rows):
		grid.append([])        #making 2d list 
		for j in range(rows):
			spot = Spot(i, j, gap, rows)      #calling class and giving values
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):          #making grid lines
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))                     #for x axis grid line
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))      #for y axis grid line


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):                                                  # to get position at which coordinate mouse has clicked
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():                                    #if someone want to close window then this loop will stop 
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]:                                # left mouse button pressed
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)     #it will give at which actual spot we have clicked
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]:                     # right mouse button pressed
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:                     #to use algo
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)                         #lambda is a function which is already in a function which called

				if event.key == pygame.K_c:                       # to clear the entie screen  when c is pressed and reset
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)
