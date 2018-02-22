import os
import pipeline_functions as pf
import imageio
imageio.plugins.ffmpeg.download()
# Import everything needed to edit/save/watch video clips
from moviepy.editor import VideoFileClip
from IPython.display import HTML

TEST_INPUT_DIR = "test_videos/"
TEST_OUTPUT_DIR = "test_videos_output/"


def dir_exists(dir):
    """Test if dir exists"""
    return os.path.exists(dir) and os.path.isdir(dir)


def process_image(image):
    """Process movie image"""
    return pf.draw_lane_pipeline(image)


def process_movie(mov):
    mov_output = TEST_OUTPUT_DIR + mov
    clip = VideoFileClip(TEST_INPUT_DIR + mov)
    mov_clip = clip.fl_image(process_image)  # NOTE: this function expects color images!!
    mov_clip.write_videofile(mov_output, audio=False)


if not dir_exists(TEST_OUTPUT_DIR):
    os.mkdir(TEST_OUTPUT_DIR)

process_movie('solidWhiteRight.mp4')
process_movie('solidYellowLeft.mp4')
process_movie('challenge.mp4')