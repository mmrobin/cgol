# object oriented implementation of Conway's Game of Life
# (with periodic boundary conditions)
# this implementation is an animated terminal toy;
# however, all but the printGrid method in the grid class
# are entirely portable for use in another form factor
# such as an SDL2 window or exporting gifs

# NOTE: to add
# saving and loading grid states
# (maybe) a logging mode
# a check that terminates the program on still-lifes
# text below the simulation with information about the generation, etc
# pause, back, forward, save buttons
#       worth noting that back button will be HEAVY on memory
#       because cgol is not backwards-deterministic
#       maybe use async library
import random
import time
import os

# for later: ignore dim defaults if loading a file
xDimDefault = 24
yDimDefault = 24
waitDefault = 0.1
printGen = True

# the grid object has two purposes
# give the cells coordinates
# tell them to update
class grid:
    # the grid object will hold a dictionary called cells
    # which associates each cell to an x and y coordinate
    # relative to the grid
    # NOTE: init should check that xDim * yDim == len(cells)
    def __init__(self, xDim, yDim, cells):
        self.generation = 0
        self.xDim = xDim
        self.yDim = yDim
        
        # cells is a list of 0s and 1s which correspond
        # to the states of the cells in the grid
        self.cells = cells

        self.cellxy = {}
        cellPos = 0
        for i in range(len(self.cells)):

            cellx = cellPos % self.xDim
            celly = int(cellPos / self.xDim)
            cellTuple = (cellx, celly)
            # print(f'{cellTuple}, {cellPos}')
            # the cell object associated to the (x, y) coordinate pair
            # is initialized with the x value, the y value, and the state
            # in the list used to init the grid object
            self.cellxy[cellTuple] = cell(cellTuple[0], cellTuple[1], cells[i], 0)
            cellPos += 1

    def gridUpdate(self):
        # update the grid, meaning to move one generation forward
        # print(self.cellxy)
        for coord in self.cellxy:
            # cell refers to the cell object at the coordinate
            # NOTE: flip the key:value pairs in grid.cellxy to make this
            # readable for human beings (and name things better)
            cell = self.cellxy[coord]
            
            # printing the cell object simply calls the __str__
            # method inside the cell object, which returns its state
            # print(cell)
            
            # count neighbors
            nbrCount = 0
            # construct cell coordinate tuples by asking each cell where it is
            # this isn't strictly necessary but it scales well
            
            # to avoid index errors we introduce periodic boundary conditions
            # we do this by modding coords by dimensions
            # cell.x and cell.y are more or less sugar -- we can just as easily
            # grab the coordinates from self.cellxy, but it looks gross
            left    = (cell.x - 1) % self.xDim
            xcenter = cell.x       % self.xDim
            right   = (cell.x + 1) % self.xDim

            up      = (cell.y - 1) % self.yDim
            ycenter = cell.y       % self.yDim
            down    = (cell.y + 1) % self.yDim

            # it seems fastest to just do the arithmetic per-cell with coords
            # as opposed to 
            nbrs = [self.cellxy[ ( left,     up      ) ],
                    self.cellxy[ ( xcenter,  up      ) ],
                    self.cellxy[ ( right,    up      ) ],
                    self.cellxy[ ( left,     ycenter ) ],
                    self.cellxy[ ( right,    ycenter ) ],
                    self.cellxy[ ( left,     down    ) ],
                    self.cellxy[ ( xcenter,  down    ) ],
                    self.cellxy[ ( right,    down    ) ]]
            
            for nbr in nbrs:
                if nbr.state == 1:
                    nbrCount += 1
                else:
                    pass
            # tell each cell how many neighbors it has so that they
            # can all update at the same time
            cell.nbrCount = nbrCount
        
        # we tell each cell to update outside of the loop above
        # because otherwise each cell would update with the knowledge
        # of all cells before it updating
        # when in reality the cells should all update based on the same information
        # (meaning the previous grid state)
        for coord in self.cellxy:
            cell = self.cellxy[coord]
            cell.update()
        
        self.generation += 1


    def gridPrint(self):
        for coord in self.cellxy:
            cell = self.cellxy[coord]
            if cell.x != self.xDim - 1:
                if cell.state == 1:
                    print('\u2588\u2588', end='')
                else:
                    print('\u2592\u2592', end='')
            else:
                if cell.state == 1:
                    print('\u2588\u2588', end='\n')
                else:
                    print('\u2592\u2592', end='\n')
        if printGen:
            print(f'Generation {self.generation}')
# the cell really only needs to store its state and its neighbors
# but the x and y coordinates clarify the methods inside the grid class
class cell:
    def __init__(self, x, y, state, nbrCount):
        self.x = x
        self.y = y
        self.state = int(state)
        self.nbrCount = nbrCount
    
    def __str__(self):
        return str(self.state)

    def update(self):
        # update rules based on the number of living neighbors
        # there are three rules
        # 1) a dead cell with exactly 3 neighbors comes to life
        # 2) a living cell with exactly 2 or 3 neighbors survives
        # 3) all other cells die or remain dead
        
        # print(self.nbrCount)
        if self.state == 0:
            if self.nbrCount == 3:
                self.state = 1
            else:
                pass
        else:
            if self.nbrCount == 2 or self.nbrCount == 3:
                self.state = 1
            else:
                self.state = 0

# generate a random list of cells to seed the main grid object with
def randomizeGrid(xDim = xDimDefault, yDim = yDimDefault):
    randomCells = []
    for y in range(0, yDim):
        for x in range(0, xDim):
            value = random.randint(0, 1)
            randomCells.append(value)
    
    return randomCells

def main(xDim = xDimDefault, yDim = yDimDefault):
    
    mainCells = randomizeGrid(xDim, yDim)
    mainGrid = grid(xDim, yDim, mainCells)
    os.system('clear')
    
    # control+C to stop the simulation
    while True:
        mainGrid.gridUpdate()       # update the grid object
        mainGrid.gridPrint()        # show the grid
        time.sleep(waitDefault)     # for (default 0.4) seconds
        os.system('clear')          # clear the screen (and start over)

# let er rip
main()
