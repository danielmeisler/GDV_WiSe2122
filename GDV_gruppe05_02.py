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

# configration of the colors
# name, hue, hue_range, saturation, saturation_range, value, value_range, kernel_size, kernel_shape, morph_operation, morph_iteration
blue = ('blue', 97, 4, 175, 100, 135, 100, 3, cv2.MORPH_ELLIPSE, 'none')
green = ('green', 41, 6, 245, 100, 135, 100, 3, cv2.MORPH_ELLIPSE, 'none')
yellow = ('yellow', 28, 5, 255, 100, 200, 60, 2, cv2.MORPH_ELLIPSE, 'none')
red = ('red', 173, 15, 115, 100, 170, 100, 4, cv2.MORPH_ELLIPSE,'morph_red')
pink = ('pink',0, 9, 45, 100, 255, 100, 2, cv2.MORPH_ELLIPSE,'morph_pink')
white =('white', 29, 6, 0, 100, 255, 100, 2, cv2.MORPH_ELLIPSE,'morph_white')

# all colors in one array
color_configuration = (red,green,blue,yellow,white,pink)

# dilation with parameters
def dilatation(img, size, shape):
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1),
                                        (size, size))
    return cv2.dilate(img, element)

# erosion with parameters
def erosion(img, size, shape):
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1),
                                        (size, size))
    return cv2.erode(img, element)

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

num_test_images_succeeded = 0
for img_name in glob.glob('Images/chewing_gum_balls*.jpg'):
    # load image
    print('Searching for colored balls in image:', img_name)

    all_colors_correct = True
    for c in range(0, len(color_configuration)):
        img = cv2.imread(img_name, cv2.IMREAD_COLOR)
        height = img.shape[0]
        width = img.shape[1]

        # convert to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # TODO: Insert your algorithm here
        lower_color = np.array([color_configuration[c][1] - color_configuration[c][2], 
                                color_configuration[c][3] - color_configuration[c][4], 
                                color_configuration[c][5] - color_configuration[c][6]])
        upper_color = np.array([color_configuration[c][1] + color_configuration[c][2], 
                                color_configuration[c][3] + color_configuration[c][4], 
                                color_configuration[c][5] + color_configuration[c][6]])
        # create a mask
        mask = cv2.inRange(hsv, lower_color, upper_color)
        # specific morph
        if(color_configuration[c][9] == "morph_red"):
            for i in range(3):
                mask = dilatation(mask, color_configuration[c][7], color_configuration[c][8])
            for i in range(4):
                mask = erosion(mask, color_configuration[c][7], color_configuration[c][8])
        if(color_configuration[c][9] == "morph_white"):
            for i in range(2):
                mask = dilatation(mask, color_configuration[c][7], color_configuration[c][8])
            for i in range(3):
                mask = erosion(mask, color_configuration[c][7], color_configuration[c][8])
        if(color_configuration[c][9] == "morph_pink"):
            #for i in range(1):
            #    mask = dilatation(mask, color_configuration[c][7], color_configuration[c][8])
            for i in range(1):
                mask = erosion(mask, color_configuration[c][7], color_configuration[c][8])
        # generel morph
        mask = opening(mask, color_configuration[c][7], color_configuration[c][8])
        # variables for counting
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
                  str(gt_list[c]), color_configuration[c][0]  , 'chewing gum balls. Yeah!')
        elif (num_final_labels > int(gt_list[c])):
            print('We have found too many (', str(num_final_labels), '/',
                  str(gt_list[c]), ') candidates for', color_configuration[c][0], 'chewing gum balls. Damn!')
            all_colors_correct = False
        else:
            print('We have not found enough (', str(num_final_labels), '/',
                  str(gt_list[c]), ') candidates for', color_configuration[c][0], 'chewing gum balls. Damn!')
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