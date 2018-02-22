import math
import cv2
import numpy as np

"""Pipeline to process images and draw road lanes"""


def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)


def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def region_of_interest(img, vertices):
    """
    Applies an image mask.

    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    # defining a blank mask to start with
    mask = np.zeros_like(img)

    # defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    # filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    # returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def extrapolate_line(list_x, list_y, min_allowed_slope, max_allowed_slope, img, color, thickness):
    """
    Fits listx, list_y to 1st deg polynomial.
    Tries polifit 1st and average if that does not work

    :param list_x: list of x's of points to be extrapolated
    :param list_y: list of y's of points to be extrapolated
    :param min_allowed_slope: min slope allowed
    :param max_allowed_slope: max slope allowed
    :param img:  image to be extrapolated on
    :param color: line color
    :param thickness:  line thickness
    :return :
    """
    if not list_x or not list_y:
        return

    imgy = img.shape[0]
    extrap_base_y = imgy  # lower y coord of extrapolation
    extrap_horizon_y = math.floor(imgy * 2. / 3.)  # upper y coord of extrapolation

    # Try polyfit
    m, b = np.polyfit(list_x, list_y, 1)
    if m < min_allowed_slope or m > max_allowed_slope:
        # Problem: all the lines are close by.  Try average slope for this.
        num_lines = int(len(list_x) / 2)
        sum_slope = 0
        sum_b = 0
        for i in np.arange(0, num_lines):
            p1, p2 = 2*i, 2*i+1
            x1, x2 = list_x[p1], list_x[p2]
            y1, y2 = list_y[p1], list_y[p2]
            slope = (y2 - y1) / (x2 - x1)
            bval = y1 - slope * x1
            sum_slope += slope
            sum_b += bval

        m, b = sum_slope/num_lines, sum_b/num_lines

    base_x = math.ceil((extrap_base_y - b) / m)
    horizon_x = math.ceil((extrap_horizon_y - b) / m)
    cv2.line(img, (base_x, extrap_base_y), (horizon_x, extrap_horizon_y), color, thickness)


def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    """
    Draws Hough lines on the image
    :param img: original image
    :param lines: Hough line list
    :param color: line color
    :param thickness: line thickness
    :return:
    """

    # Calculate max and min allowed line slopes on the left and the right side of the image
    extrap_imgshape = img.shape
    imgx = extrap_imgshape[1]
    imgy = extrap_imgshape[0]
    midx = imgx/2

    max_allowed_slope_right = imgy / (imgx / 2.)
    min_allowed_slope_right = (imgy / 2.) / imgx

    max_allowed_slope_left = -min_allowed_slope_right
    min_allowed_slope_left = -max_allowed_slope_right

    # Go through the lines deciding if they are on the right or the left side
    # of the image.  Skip the lines that are not aligned with the motion.
    left_x, left_y = [], []
    right_x, right_y = [], []
    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2-y1)/(x2-x1)
            if x1 > midx < x2:  # right side of img
                if not (max_allowed_slope_right > slope > min_allowed_slope_right):
                    continue
                right_x += [x1, x2]
                right_y += [y1, y2]
            elif x1 < midx > x2:   # left side of img
                if not (min_allowed_slope_left < slope < max_allowed_slope_left):
                    continue
                left_x += [x1, x2]
                left_y += [y1, y2]


    # draw left line
    if left_x and left_y:
        extrapolate_line(left_x, left_y, min_allowed_slope_left, max_allowed_slope_left, img, color, thickness)

    # draw right line
    if right_x and right_y:
        extrapolate_line(right_x, right_y, min_allowed_slope_right, max_allowed_slope_right, img, color, thickness)


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.

    Returns an image with Hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines, thickness=10)
    return line_img


def weighted_img(img, initial_img, a=0.8, b=1., y=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.

    `initial_img` should be the image before any processing.

    The result image is computed as follows:

    initial_img * α + img * β + γ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, a, img, b, y)


def filter_color(rgb_img, hsv_img, lower_color, upper_color):
    """Filter colors between lower and upper rnages in hsv"""
    mask = cv2.inRange(hsv_img, lower_color, upper_color)
    return cv2.bitwise_and(rgb_img, rgb_img, mask=mask)


def draw_lane_pipeline(orig_img):
    """
    Pipeline: draw lane lines on the `orig_img` array
    Yellow Filter & White Filter ->  Gray Scale -> Gaussian Blur -> Canny > Hough Transform -> Draw Lines

    Return modified image arrays
    """

    # Pipeline parameters
    blur_kernel_size = 5
    canny_low_threshold = 50
    canny_high_threshold = 150

    # Define the Hough transform parameters
    rho = 2 # distance resolution in pixels of the Hough grid
    theta = np.pi/180 # angular resolution in radians of the Hough grid
    threshold = 1     # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 20 #minimum number of pixels making up a line
    max_line_gap = 20    # maximum gap in pixels between connectable line segments

    # define range of yellow and white colors in HSV
    lower_yellow = np.array([15, 100, 150])
    upper_yellow = np.array([30, 255, 255])
    lower_white = np.array([0, 0, 215])
    upper_white = np.array([255, 50, 255])

    hsv = cv2.cvtColor(orig_img, cv2.COLOR_RGB2HSV)
    res_y = filter_color(orig_img, hsv, lower_yellow, upper_yellow)
    res_w = filter_color(orig_img, hsv, lower_white, upper_white)
    yw_image = cv2.bitwise_or(res_y, res_w)  # combine image

    gray_img = grayscale(yw_image)
    blur_gray = gaussian_blur(gray_img, blur_kernel_size)
    edges = canny(blur_gray, canny_low_threshold, canny_high_threshold)

    # Define a four sided polygon to mask a region to be analized with Hough
    imy,imx,dummy = orig_img.shape
    v1, v2, v3, v4 = (0, imy), (math.floor(imx/2), math.floor(imy/2 + 50)), (math.floor(imx/2 + 50), math.floor(imy/2) + 50), (imx, imy)
    vertices = np.array([[v1, v2, v3, v4]], dtype=np.int32)
    masked_image = region_of_interest(edges, vertices)

    hough_line_img = hough_lines(masked_image, rho, theta, threshold, min_line_length, max_line_gap)

    return weighted_img(hough_line_img, orig_img)


