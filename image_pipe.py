import os
import matplotlib.image as mpimg
import pipeline_functions as pf

"""
Process images from TEST_INPUT_DIR and output them into TEST_OUTPUT_DIR
"""
TEST_INPUT_DIR = "test_images/"
TEST_OUTPUT_DIR = "test_images_out/"

def dir_exists(dir):
    """Test if dir exists"""
    return os.path.exists(dir) and os.path.isdir(dir)

if not dir_exists(TEST_OUTPUT_DIR):
    os.mkdir(TEST_OUTPUT_DIR)

test_imgs = os.listdir(TEST_INPUT_DIR)
for img_name in test_imgs:
    img_read = mpimg.imread(TEST_INPUT_DIR + img_name)
    lane_img = pf.draw_lane_pipeline(img_read)
    mpimg.imsave(TEST_OUTPUT_DIR + img_name, lane_img, format='jpg')
