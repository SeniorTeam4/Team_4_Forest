# import libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors
import random
import copy

# colors for visualization
EMPTY, TREE, FIRE, WATER = 0, 1, 2, 3
colors_list = [(0.2,0,0), (0,0.5,0), (1,0,0), 'orange', 'black']
cmap = colors.ListedColormap(colors_list)
bounds = [0,1,2,3,4]
norm = colors.BoundaryNorm(bounds, cmap.N)


def windDirection(windOp, nx, ny):
  #N - 1
  if windOp == 1:
     return [1, 1, 1, 0, 0, 0, 0, 0]
  #S - 2
  elif windOp == 2:
    return [0, 0, 0, 0, 0, 1, 1, 1]
  #W - 3 
  elif windOp == 3:
    return [1, 0, 0, 1, 0, 1, 0, 0]
  #E - 4
  elif windOp == 4:
    return [0, 0, 1, 0, 1, 0, 0, 1]
  #NW - 5
  elif windOp == 5:
    return [1, 1, 0, 1, 0, 0, 0, 0]
  #NE - 6
  elif windOp == 6:
    return [0, 1, 1, 0, 1, 0, 0, 0]
  #SW - 7 
  elif windOp == 7:
    return [0, 0, 0, 1, 0, 1, 1, 0]
  #SE - 8
  elif windOp == 8:
    return [0, 0, 0, 0, 1, 0, 1, 1]
  else:
    return [1]*8

def isValid(i, j, x, y):
  if 0<=i<=x-1 and 0<=j<=y-1:
    return True
  else:
    return False

'''
Parameters
'''
# inits 
# density
d = 0.6

# forest size
nX, nY = 100,100

# neihborhood
# Moore neighborhood =((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1)) 
x =  ([-1,-1,-1,0,0,1,1,1])
y =  ([-1,0,1,-1,1,-1,0,1])


# wind
windOp = 2
neighbor = windDirection(windOp, x, y) #return proper

# humidity
humidity = 0

# temperature
temp = 0
'''
Parameters
'''

def init(nX, nY, d):
    '''
    nX, nY: 
    '''
    grid = np.zeros((nX,nY))
    empty = []
    tree = []

    global fire
    fire = []

    nEmpty = 0
    nTree = 0

    for i in range(nX):
        for j in range(nY):
            empty.append((i,j))
            nEmpty+=1

    #randomly distribute tree
    for i in range(int(d*nY*nX)):
      j = random.randrange(nEmpty)
      tree.append(empty.pop(j))
      nEmpty -= 1
      nTree += 1

    #initilize trees in grid
    for t in tree:
        grid[t[0], t[1]] = TREE


    #lightning hits a tree
    if nTree > 0:
        i = random.randrange(nTree)
        t = tree.pop(i)
        grid[t[0], t[1]] = FIRE
        nTree -= 1
        fire.append((t[0], t[1]))

    return grid

def spread(grid, fire, x, y, neighbor):
    newGrid = grid.copy()
    if len(fire) != 0: 
        t = fire.pop(0)
        for i in range(len(neighbor)):
            if neighbor[i] != 0 and isValid(t[0]+x[i], t[1]+y[i], len(grid), len(grid[0])):
                if grid[t[0]+x[i], t[1]+y[i]] == 1:
                    newGrid[t[0]+x[i], t[1]+y[i]] = 2
                    fire.append((t[0]+x[i], t[1]+y[i]))
        newGrid[t[0], t[1]] = 3
    return newGrid

def update(frameNum,img, grid, fire, x, y, neighbor):
    newGrid = spread(grid, fire, x, y, neighbor)
    img.set_data(newGrid)
    grid[:,:] = newGrid[:,:]
    return img

'''
Animation
'''
grid = init(nX,nY,d)
oldGrid = grid

fig = plt.figure(figsize=(25/3, 6.25))
ax = fig.add_subplot(111)
ax.set_axis_off()
img = ax.imshow(oldGrid, cmap=cmap, norm=norm)


# Interval between frames (ms).
interval = 200
anim = animation.FuncAnimation(fig, update, fargs=(img, oldGrid, fire, x, y, neighbor), interval=interval, frames=128)
#anim.save("forest_fire.mp4")
plt.show()

'''
Animation
'''

'''
def animate(i):
    im.set_data(animate.X)
    animate.X = iterate(animate.X)
# Bind our grid to the identifier X in the animate function's namespace.
animate.X = X
def iterate(X):
    X1 = X
    for n in range(100):
        if len(fire) == 0:
            break

        t = fire.pop(0)
        for i in range(10): 
            if isValid(t[0]+x_coor[i], t[1]+y_coord[i]) and neighbourhood[i] !=0:
                if X[t[0]+x_coor[i],  t[1]+y_coord[i]] == TREE:
                    X1[t[0]+x_coor[i],  t[1]+y_coord[i]] = FIRE
                    nBurn +=1
                    nTree -=1
                    fire.append((t[0]+x_coor[i], t[1]+y_coord[i]))

        X1[t[0],t[1]] = EMPTY
        nChared +=1
        nBurn-=1
        char.append(t)
    return X1
'''