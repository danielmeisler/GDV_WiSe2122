import numpy as np
import cv2
import copy

# print keyboard usage
print ('This is a HSV color detection demo. Use the keys to adjust the selection color in HSV space. Circle in bottom left.')
print ('The masked image shows only the pixels with the given HSV color within a given range.')
print ('Use h/H to de-/increase the hue.')
print ('Use s/S to de-/increase the saturation.')
print ('Use v/V to de-/increase the (brightness) value.\n')

# capture webcam image
cap = cv2.VideoCapture(0)

# get camera image parameters from get()
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
codec = int(cap.get(cv2.CAP_PROP_CODEC_PIXEL_FORMAT))
print ('Video properties:')
print ('  Width = ' + str(width))
print ('  Height = ' + str(height))
print ('  Codec = ' + str(codec))

# drawing helper variables
thick = 10
thin = 3
thinner = 2
font_size_large = 3
font_size_small = 1
font_size_smaller = .6
font = cv2.FONT_HERSHEY_SIMPLEX


# TODO: define  RGB colors as variables
red_rgb = (255, 0, 0)
green_rgb = (0, 255, 0)
blue_rgb = (0, 0, 255)
darker_blue_rgb = (0, 0, 150)

##### exemplary color conversion (only for the class), tests usage of cv2.cvtColor
img_red_rgb = np.zeros((1,1,3), np.uint8)
img_red_rgb[0, 0] = red_rgb
img_red_hsv = cv2.cvtColor(img_red_rgb, cv2.COLOR_RGB2HSV)

print('Red in RGB and HSV')
print(img_red_rgb)
print(img_red_hsv)

img_green_rgb = np.zeros((1,1,3), np.uint8)
img_green_rgb[0, 0] = green_rgb
img_green_hsv = cv2.cvtColor(img_green_rgb, cv2.COLOR_RGB2HSV)

print('Green in RGB and HSV')
print(img_green_rgb)
print(img_green_hsv)

img_blue_rgb = np.zeros((1,1,3), np.uint8)
img_blue_rgb[0, 0] = blue_rgb
img_blue_hsv = cv2.cvtColor(img_blue_rgb, cv2.COLOR_RGB2HSV)

print('Blue in RGB and HSV')
print(img_blue_rgb)
print(img_blue_hsv)

# color ranges, enter found default values and uncomment
hue = 120
hue_range = 10
saturation = 200
saturation_range = 100
value = 200
value_range = 100

lower_bound = (hue - hue_range, saturation - saturation_range, value - value_range)
upper_bound = (hue + hue_range, saturation + saturation_range, value + value_range)

while True:
    # get video frame (always BGR format!)
    ret, frame = cap.read()
    if (ret):
        # copy image to draw on
        img = copy.copy(frame) 
       
        # draw arrows (coordinate system)
        
        # computing color ranges for display
        

        # draw selection color circle and text for HSV values        
        # img = cv2.circle(img, (width - 50, height - 50), 30, , -1)
        # img = cv2.putText(img,'H = ' + str(hue), (width - 200, height - 75), font, font_size_smaller, blue, thinner)
        # img = cv2.putText(img,'S = ' + str(saturation), (width - 200, height - 50), font, font_size_smaller, blue, thinner)
        # img = cv2.putText(img,'V = ' + str(value), (width - 200, height - 25), font, font_size_smaller, blue, thinner)
        
        # convert to HSV        
        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # create a bitwise mask
        mask = cv2.inRange(img_hsv, lower_bound, upper_bound)
        #mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_DILATE, (3,3)))

        # apply mask 
        img_masked = cv2.bitwise_and(frame, frame, mask = mask)
        
        # show the original image with drawings in one window
        cv2.imshow('Original image', img)
        
        # show the masked image in another window
        cv2.imshow('Masked image', img_masked)
        
        # show the mask image in another window
        

        # deal with keyboard input
        key = cv2.waitKey(10)
        if key == ord('q'):
            break
        
    else:
        print('Could not start video camera')
        break

cap.release()
cv2.destroyAllWindows()