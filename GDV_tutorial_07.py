import cv2
import numpy as np

### Goal: Count the number of green smarties in the images
# define green in HSV
hue = 60  # 60 is pure green
hue_range = 10
saturation = 155
saturation_range = 100
value = 155
value_range = 100
lower_green = np.array([hue - hue_range,saturation - saturation_range,value - value_range])
upper_green = np.array([hue + hue_range,saturation + saturation_range,value + value_range])

# load image
img = cv2.imread('images\smarties01.JPG',cv2.IMREAD_COLOR)
img = cv2.resize(img,(800,600))

# convert to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# create a mask
mask = cv2.inRange(hsv, lower_green, upper_green)

## morphological operations code
# optional mapping of values with morphological shapes
def morph_shape(val):
    if val == 0:
        return cv2.MORPH_RECT
    elif val == 1:
        return cv2.MORPH_CROSS
    elif val == 2:
        return cv2.MORPH_ELLIPSE

# dilation with parameters
def dilatation(img,size,shape): 
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1),
                                       (size, size))
    return cv2.dilate(img, element)

# opening
def opening(img,size,shape): 
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1),
                                       (size, size))
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, element)

#setting the parameters
kernel_shape = morph_shape(2)
kernel_size = 7
#mask = dilatation(mask,kernel_size,kernel_shape)
mask = opening(mask,kernel_size,kernel_shape)

# mask out green parts as binary image
result = cv2.bitwise_and(img, img, mask=mask)

# find connected components
connectivity = 4
(numLabels, labels, stats, centroids) = cv2.connectedComponentsWithStats(mask, connectivity, cv2.CV_32S)


# print out number of connected components and be aware that The first connected component, with an ID of 0
# is always the background. We typically ignore the background, but if you ever need it, keep in mind that ID 0
# contains it.
print('We have found ', str(numLabels-1),' green smarties.')

# find center of mass and draw a mark in the original image
red_BGR = (0,0,255)
circle_size = 10
circle_thickness = 5
min_size = 10

# go through all (reasonable) found connected components
for i in range(1,numLabels):
    # check size and roundness as plausibility
    x = stats[i, cv2.CC_STAT_LEFT]
    y = stats[i, cv2.CC_STAT_TOP]
    w = stats[i, cv2.CC_STAT_WIDTH]
    h = stats[i, cv2.CC_STAT_HEIGHT]
    if w < min_size or h < min_size:
        print ('Found a too small component.')
        break # found component is too small to be correct 
    if w > h:
        roundness = 1.0 / (w/h)
    elif h > w:
        roundness = 1.0 / (h/w)  
    if (roundness > 2):
        print ('Found a component that is not round enough.')
        break # ratio of width and height is not suitable

    # find and draw center
    center = centroids[i]
    center = np.round(center)
    center = center.astype(int)
    cv2.circle(img,center,circle_size,red_BGR,circle_thickness)
    # find and draw bounding box
    
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3) 




# show the original image with drawings in one window
cv2.imshow('Original image', img)
# show the masked image in another window
cv2.imshow('Masked image', result)
# show the mask image in another window
cv2.imshow('Mask image', mask)

cv2.waitKey(0)
cv2.destroyAllWindows()
