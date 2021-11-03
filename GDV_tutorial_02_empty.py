import cv2
import numpy as np
""" import copy """

# loading images in grey and color

img_color = cv2.imread('images/coolcatwithhat.jpg', cv2.IMREAD_COLOR) 
img_grayscale = cv2.imread('images/coolcatwithhat.jpg', cv2.IMREAD_GRAYSCALE) 

# changing color and gray versions

img_array = [img_color, img_grayscale]

img = img_array[1] 

# do some print out about the loaded data

print (type(img))
print (img.shape)

""" img = copy.copy(img_grayscale) """

# Continue with the color image or the grayscale image

# Extract the size or resolution of the image

height = img.shape[0]
width = img.shape[1]

# resize image

 
# print first row

""" print(img[0]) """

# print first column

""" print(img[:][0]) """

# set area of the image to black

""" for i in range (250, 300):
  for j in range (220, 290):
    img[i][j] = (180, 255, 40)

for i in range (250, 300):
  for j in range (320, 390):
    img[i][j] = (250, 100, 150) """
        
# find all used colors in the image

""" colors = []
for i in range (height):
    for j in range (width):
        curr_color = img[i][j]
        if colors.count(curr_color) == 0:
            colors.append(curr_color)
print(colors) """


# copy one part of an image into another one

""" letters = img[145:220,220:345]
img[265:340,240:365] = letters """

# test

quarter_frame = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
img[:height//2,:width//2] = quarter_frame
img[:height//2,:width//2] = cv2.flip(quarter_frame, 0)

# save image

# show the image

cv2.imwrite('images/img_out2.jpg', img)
title = 'cool cat with hat'
cv2.namedWindow(title,cv2.WINDOW_GUI_NORMAL)

# show the original image (copy demo)

cv2.imshow(title, img)
cv2.waitKey(0)
cv2.destroyAllWindows()

