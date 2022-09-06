# import libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors
import FWI
import random
import copy

# colors for visualization
EMPTY, TREE, FIRE, CHAR = 0, 1, 2, 3
colors_list = [(0.2,0,0), (0,0.5,0), (1,0,0), 'orange', 'black']
cmap = colors.ListedColormap(colors_list)
bounds = [0,1,2,3,4]
norm = colors.BoundaryNorm(bounds, cmap.N)


def windDirection(windOp):
  #N - 1
  if windOp == 0:
     return [(-1,-1), (-1,0), (-1,1)]
  #S - 2
  elif windOp == 1:
    return [(1,-1), (1,0), (1,1)]
  #W - 3 
  elif windOp == 2:
    return [(-1,-1), (0,-1), (1,-1)]
  #E - 4
  elif windOp == 3:
    return [(-1,1), (0, 1), (1,1)]
  #NW - 5
  elif windOp == 4:
    return [(-1,-1), (-1,0), (0,-1)]
  #NE - 6
  elif windOp == 5:
    return [(-1,0), (-1,1), (0, 1)]
  #SW - 7 
  elif windOp == 6:
    return [(0,-1), (1,-1), (1,0)]
  #SE - 8
  elif windOp == 7:
    return [(0, 1), (1,0), (1,1)]
  else:
    return [(-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1)]

def isValid(i, j, x, y):
  if 0<=i<x and 0<=j<y:
    return True
  else:
    return False

'''
Parameters
'''
# inits 
# density
d = 0.70
# forest size
nX, nY = 100,100

# neihborhood
# Moore neighborhood =((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1)) 

'''
The Fire Weather Index (FWI) system provides fire danger information following the European Forest Fire Information System (EFFIS) classification:
very low (0.0 – 5.2)
low (5.2 – 11.2)
moderate (11.2 – 21.3)
high (21.3 – 38.0)
very high (38.0 – 50.0)
extreme (50.0 – 100.0)
'''


# wind
windOp = 10
neighbor = [(-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1)]
#windDirection(windOp) #return proper

# humidity level 1-low, 2-med ,3-high
humidity = 0

# humidity level 1-low, 2-med ,3-high
temp = 0

'''
Parameters
'''

def init(nX, nY, d):
    grid = np.zeros((nX,nY))
    empty = []
    tree = []

    nEmpty = 0
    nTree = 0
    nFire = 0
    nChar = 0
    treeData = []
    fireData = []
    charData = []

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
        nFire += 1

    treeData.append(nTree)
    fireData.append(nFire)
    charData.append(nChar)
    return grid, treeData, fireData, charData



def spread(g, n, nX, nY):
    g1 = np.zeros((nX, nY))
    nTree = 0
    nFire = 0
    nChar = 0
    for x in range(nX):
        for y in range(nY):
            if g[x, y] == TREE:
                nTree+=1
                g1[x, y] = TREE
                for i, j in n:
                    if x+i in range(nX) and y+j in range(nY) and g[x+i, y+j] == FIRE and random.random() > 1-0.5:
                        g1[x, y] = FIRE
                        nTree-=1
                        nFire+=1
                        break
            if g[x, y] == FIRE:
                nChar+=1
                g1[x,y] = CHAR
            if g[x, y] == EMPTY:
                g1[x,y] = EMPTY
            if g[x, y] == CHAR:
                nChar+=1
                g1[x,y] = CHAR

    return g1, nTree, nFire, nChar


def update(frameNum,img, X, neighbor,nX,nY,treeData, fireData, charData):
    if frameNum%20 > 9:
        neighbor = windDirection(random.randint(0,8))
    X1, nTree, nFire, nChar = spread(X, neighbor, nX, nY)
    n.append(frameNum)
    treeData.append(nTree)
    fireData.append(nFire)
    charData.append(nChar)
    #display = copy.deepcopy(X1)
    img.set_data(X1)
    X[:,:] = X1[:,:]
    axs[1].plot(n, treeData, color="green")
    axs[1].plot(n, fireData, color="orange")
    axs[1].plot(n, charData, color="blue")
    axs[1].legend(['Tree', 'Burning', 'Char'],loc='upper right')
    return img,

'''
Animation
'''
index = FWI.calcFWI(4,17,45,25,0, 85,6,15,45.98)
grid, treeData, fireData, charData = init(nX,nY,d)
#oldGrid = grid
title = f'Forest_Fire_d={d}, FWI={index}, Wind Diretion Changes'
fig, axs = plt.subplots(1, 2, figsize=(10, 5), gridspec_kw={'width_ratios': [2, 2]})

axs[0].set_axis_off()

img = axs[0].imshow(grid, cmap=cmap, norm=norm)
axs[1].set_ylim(0, treeData[0])
n=[0]

fig.suptitle(title)

# Interval between frames (ms). slows down change of plot
interval = 200
#frames -> how long will animation run
anim = animation.FuncAnimation(fig, update, fargs=(img, grid, neighbor, nX, nY, treeData, fireData, charData), interval=interval, frames=135,blit=True)
path = f'./{title}_2.mp4'
#writervideo = animation.FFMpegWriter(fps=60) 
anim.save(path, fps = 60)
#anim.save(path, fps=30)
#plt.show()

'''
plt.plot(n, treeData, color="green")
plt.plot(n, fireData, color="orange")
plt.plot(n, charData, color="blue")
plt.legend(['Tree', 'Burning', 'Char'],loc='upper right')
plt.title(title)
plt.show()
'''
'''
#Animation
'''


#month, temperature, relative humidity, wind speed, rain,   previous FFMC, DMC, DC, and latitude
print('Done')