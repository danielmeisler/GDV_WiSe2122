import cv2
import math
import operator

# capture webcam image
cap = cv2.VideoCapture(0)

# get camera image parameters from get()
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print ('Frame height : ', str(height))

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print ('Frame width : ', str(width))


# drawing helper variables
## thickness
thick = 10
thin = 3

## color
blue = (255, 0, 0)
green = (0, 255, 0)
red = (0, 0, 255)

## fonts

# variables for moving rectangle

# create a window for the video
title = 'Keine Webcam'
cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)
print('Press q to close window.')

# start a loop
while True:

    ret, frame = cap.read()
    
    if (ret):

    # capture the image

    # check if capture succeeded
        
        # draw a blue diagonal cross over the image
        pt1 = (0,0)
        pt2 = (width, height)
        cv2.line(frame, pt1, pt2, blue, thick)

        pt3 = (0, height)
        pt4 = (width, 0)
        cv2.line(frame, pt3, pt4, red, thin)

        # draw a circle

        # write some text

        # draw arrows (potential assignment)

        # draw a rectangle that moves on a circular path
        
        # display the image
        cv2.imshow(title, frame)
        
        # press q to close the window
        if cv2.waitKey(10) == ord('q'):
            break
    else:
        print ('Could not retrieve frame.')
        break

# release the video capture object and window
