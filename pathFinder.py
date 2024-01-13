import pygame
import sys
from tkinter import messagebox, Tk

#created the window for the game
width = 1000
height = 1000
window = pygame.display.set_mode((width,height))

#number of colums and rows
columns = 50
rows = 50

#size of each box
boxWidth = width // columns
boxHeight = height // rows

grid = []
queue = []
path = []

class Box:
    def __init__(self,i,j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * boxWidth, self.y * boxHeight, boxWidth - 2, boxHeight - 2))
    
    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])
        
#create grid
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)

#sets the Neighbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()

    
start_box = grid[0][0]
start_box.start = True
start_box.visited = True
queue.append(start_box)

def main():
    begin_search = False
    target_box_set = False
    searching = True
    target_box = None

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT: #close the window
                pygame.quit()
                sys.exit()
            #Mouse controls
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                #draw wall
                if event.buttons[0]:
                    i = x // boxWidth
                    j = y // boxHeight
                    grid[i][j].wall = True
                #set target
                if event.buttons[2] and not target_box_set:
                    i = x // boxWidth
                    j = y // boxHeight
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True
                #start the algorithm
            if event.type == pygame.KEYDOWN and target_box_set:
                    begin_search = True

        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour)
            else:
                if searching:
                    print("There is no solution!")
                    searching = False


        #color white for the window
        window.fill((255,255,255))

        for i in range(columns):
             for j in range(rows):
                box = grid[i][j]
                #grid color
                box.draw(window, (230,230,230))
                
                if box.queued:
                    box.draw(window, (200,0,0))
                if box.visited:
                    box.draw(window, (0,200,0))
                if box in path: 
                    box.draw(window,(255,165,0))

                if box.start:
                    box.draw(window,(0,200,200))
                if box.wall:
                    box.draw(window, (90,90,90))
                if box.target:
                    box.draw(window, (200,200,0))

        pygame.display.flip()

main()