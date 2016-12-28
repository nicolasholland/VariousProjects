from sqlite3 import dbapi2 as sqlite
import numpy as np
from matplotlib import pyplot as plt
import cv2

def drawPuzzle(piece, img, width, height, check):
    filename = piece[0]
    posX = piece[2]
    posY = piece[3]
    
    widthStep = int(width/10)
    heightStep = int(height/10)

    if (posX,posY) not in check:    
      puzzlePiece = cv2.imread('puzzlePieces/' + filename)
      check.append((posX,posY))
    else:    
      puzzlePiece = cv2.imread('puzzlePieces/' + 'A5B5D.png')
    
    ix = 0
    for x in range(posX * widthStep, (posX+1) * widthStep):
        iy = 0
        for y in range(posY * heightStep, (posY+1) * heightStep):
            for c in range(0,3):
                img[x,y,c] = puzzlePiece[ix, iy, c]
            iy = iy + 1
        ix = ix + 1


    return check

# open database
con=sqlite.connect('puzzlebase.db')

# open query file
sqlfile = open('Query.sql','r')
query = ""

for line in sqlfile:
    if 'minus' in line:
      line = 'except\n'
    query = query + line

# get data from database
data = con.execute(query).fetchall()

# draw puzzle
WIDTH = 1024
HEIGHT = 768
img = np.zeros((HEIGHT, WIDTH, 3), np.uint8)
check = []

print len(data)
for piece in data:
    check = drawPuzzle(piece, img, HEIGHT, WIDTH, check)

# close database
con.close()

# show puzzle
plt.imshow(img)
plt.axis('off')
plt.show()
