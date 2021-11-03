import cv2
import numpy as np
import copy as cp

width = 750
height = 500
squareSize = 50

halfSquare = round(squareSize/2)
middleX = round(width/2)
middleY = round(height/2)

img = np.zeros((height, width), np.uint8)

# black to white gradient
for i in range(width):
    img[:, i] = 255*i/width
# set square from middle of the image
square = img[middleX-halfSquare:middleX+halfSquare,
             middleY-halfSquare:middleY+halfSquare]
# insert square in top corners
img[0:squareSize, 0:squareSize] = square
img[0:squareSize, width-squareSize:width] = square
# copy image
defaultImg = cp.copy(img)
# insert quare at the middle left edge
img[middleY-halfSquare:middleY+halfSquare, 0:squareSize] = square

# window
title = 'Abgabe 1'
cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)

# video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = cv2.VideoWriter('videos/optical_illusion.mp4', fourcc, 60.0, (width, height))

#animation
for i in range(width-squareSize):
    img = defaultImg
    img = cp.copy(defaultImg)
    img[middleY-halfSquare:middleY+halfSquare, i:squareSize+i] = square
    cv2.imshow(title, img)
    #save image
    cv2.imwrite('frame.jpg', img)
    #load image as frame
    frame = cv2.imread('frame.jpg')
    #add frame to video
    writer.write(frame)
    cv2.waitKey(1)

cv2.destroyAllWindows()