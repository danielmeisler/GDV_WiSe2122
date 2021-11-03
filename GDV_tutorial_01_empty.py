# first step is to import the opencv module which is called 'cv2'

import cv2

# load an image with image reading modes using 'imread'

img = cv2.imread('images/coolcatwithhat.jpg', cv2.IMREAD_COLOR) 

# cv2.IMREAD_UNCHANGED  - If set, return the loaded image as is (with alpha channel, otherwise it gets cropped). Ignore EXIF orientation.
# cv2.IMREAD_GRAYSCALE  - If set, always convert image to the single channel grayscale image (codec internal conversion).
# cv2.IMREAD_COLOR      - If set, always convert image to the 3 channel BGR color image. 

# resize image with 'resize'

newWidth = 640
newHeight = 480
newSize = (newWidth, newHeight)
img = cv2.resize(img, newSize)


# rotate image (but keep it rectangular) with 'rotate'


# save image with 'imwrite'

cv2.imwrite('images/img_out.jpg', img)

title = 'cool cat with hat'
cv2.namedWindow(title,cv2.WINDOW_GUI_NORMAL)

# show the image with 'imshow' 

cv2.imshow(title, img)
cv2.waitKey(0)
cv2.destroyAllWindows()



