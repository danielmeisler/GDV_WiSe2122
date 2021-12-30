'''
Assignement 02: Object counting
Group: Group 5
Names: David Niemann, Samuel Noah Kasper, Daniel Meisler
Date: 3. November 2021
Sources: GDV
'''

import cv2
import glob  # for loading all images from a directory
import numpy as np

# Goal: Count the number of all colored balls in the images

# ground truth
num_yellow = 30
num_blue = 5
num_pink = 8
num_white = 10
num_green = 2
num_red = 6
gt_list = (num_red, num_green, num_blue, num_yellow, num_white, num_pink)

# define color ranges in HSV, note that OpenCV uses the following ranges H: 0-179, S: 0-255, V: 0-255
blue_hsv = (97, 175, 134)
green_hsv = (41, 245, 135)
red_hsv = (173, 115, 170)
yellow_hsv = (28, 255, 255)
pink_hsv = (0, 39, 255)
white_hsv = (29, 0, 255)

# morphological operations
# optional mapping of values with morphological shapes


def morph_shape(val):
    if val == 0:
        return cv2.MORPH_RECT
    elif val == 1:
        return cv2.MORPH_CROSS
    elif val == 2:
        return cv2.MORPH_ELLIPSE

# dilation with parameters


def dilatation(img, size, shape):
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1),
                                        (size, size))
    return cv2.dilate(img, element, iterations=2)

# erosion with parameters


def erosion(img, size, shape):
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1),
                                        (size, size))
    return cv2.erode(img, element, iterations=2)

# dilation with parameters


def dilatation_red(img, size, shape):
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1),
                                        (size, size))
    return cv2.dilate(img, element, iterations=3)

# erosion with parameters


def erosion_red(img, size, shape):
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1),
                                        (size, size))
    return cv2.erode(img, element, iterations=4)

# opening


def opening(img, size, shape):
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1),
                                        (size, size))
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, element)

# closing


def closing(img, size, shape):
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1),
                                        (size, size))
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, element)


# setting the parameters
kernel_shape = morph_shape(2)
kernel_size = 2

# set color under test
color_names = ['red', 'green', 'blue', 'yellow', 'white', 'pink']
color_hsv = [red_hsv, green_hsv, blue_hsv, yellow_hsv, white_hsv, pink_hsv]

# setting the parameters that work for all colors
hue_range = 7
saturation_range = 95
value_range = 95

# set individual (per color) parameters
#adjustments for color red
hue_range_red = 10
saturation_range_red = 100
value_range_red = 100

num_test_images_succeeded = 0
for img_name in glob.glob('Images/chewing_gum_balls*.jpg'):
    # load image
    print('Searching for colored balls in image:', img_name)

    all_colors_correct = True

    for c in range(0, len(color_hsv)):

        img = cv2.imread(img_name, cv2.IMREAD_COLOR)
        height = img.shape[0]
        width = img.shape[1]
 
        # convert to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # TODO: Insert your algorithm here
        if (color_hsv[c] == red_hsv):
            #if color is red
            lower_color = np.array([color_hsv[c][0] - hue_range_red, color_hsv[c]
                               [1] - saturation_range_red, color_hsv[c][2] - value_range_red])
            upper_color = np.array([color_hsv[c][0] + hue_range_red, color_hsv[c]
                               [1] + saturation_range_red, color_hsv[c][2] + value_range_red])
             # create a mask
            mask = cv2.inRange(hsv, lower_color, upper_color)
            #kernel
            kernel_size = 4
            # morph
            mask = dilatation_red(mask, kernel_size, kernel_shape)
            mask = erosion_red(mask, kernel_size, kernel_shape)
        
        else:
            lower_color = np.array([color_hsv[c][0] - hue_range, color_hsv[c]
                               [1] - saturation_range, color_hsv[c][2] - value_range])
            upper_color = np.array([color_hsv[c][0] + hue_range, color_hsv[c]
                               [1] + saturation_range, color_hsv[c][2] + value_range])
            #kernel
            kernel_size = 2 
             # create a mask
            mask = cv2.inRange(hsv, lower_color, upper_color)
            # morph
            mask = erosion(mask, kernel_size, kernel_shape)
            mask = dilatation(mask, kernel_size, kernel_shape)
        connectivity = 8
        (num_labels, labels, stats, centroids) = cv2.connectedComponentsWithStats(
            mask, connectivity, cv2.CV_32S)

        # TODO: implement something to set this variable
        min_size = 10
        num_rejected = 1
        num_final_labels = num_labels-num_rejected
        roundness = 0

        # go through all (reasonable) found connected components
        for i in range(1, num_labels):
            # check size and roundness as plausibility
            x = stats[i, cv2.CC_STAT_LEFT]
            y = stats[i, cv2.CC_STAT_TOP]
            w = stats[i, cv2.CC_STAT_WIDTH]
            h = stats[i, cv2.CC_STAT_HEIGHT]
            if w < min_size or h < min_size:
                print('Found a too small component.')
                num_rejected += 1
                continue  # found component is too small to be correct
            if w > h:
                roundness = 1.0 / (w/h)
            elif h > w:
                roundness = 1.0 / (h/w)
            if (roundness < .5):
                print('Found a component that is not round enough.')
                num_rejected += 1
                continue  # ratio of width and height is not suitable

            # find and draw center
            center = centroids[i]
            center = np.round(center)
            center = center.astype(int)
            cv2.circle(img, center, 7, (0, 0, 255), 2)

            # find and draw bounding box
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

        success = (num_final_labels == int(gt_list[c]))

        if success:
            print('We have found all', str(num_final_labels), '/',
                  str(gt_list[c]), color_names[c], 'chewing gum balls. Yeah!')
            foo = 0
        elif (num_final_labels > int(gt_list[c])):
            print('We have found too many (', str(num_final_labels), '/',
                  str(gt_list[c]), ') candidates for', color_names[c], 'chewing gum balls. Damn!')
            all_colors_correct = False
        else:
            print('We have not found enough (', str(num_final_labels), '/',
                  str(gt_list[c]), ') candidates for', color_names[c], 'chewing gum balls. Damn!')
            all_colors_correct = False

        # debug output of the test images
        if ((img_name == 'Images\chewing_gum_balls01.jpg')
            or (img_name == 'Images\chewing_gum_balls04.jpg')
                or (img_name == 'Images\chewing_gum_balls06.jpg')):
            # show the original image with drawings in one window
            cv2.imshow('Original image', img)
            # show other images!
            cv2.imshow('Masked Image', mask)
            # q for fast quit
            if cv2.waitKey(0) == ord('q'):
                break  
            cv2.destroyAllWindows()
    if all_colors_correct:
        num_test_images_succeeded += 1
        print('Yeah, all colored objects have been found correctly in ', img_name)

print('Test result:', str(num_test_images_succeeded), 'test images succeeded.')