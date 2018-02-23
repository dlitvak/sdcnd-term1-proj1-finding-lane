# **Finding Lane Lines on the Road** 
[![Udacity - Self-Driving Car NanoDegree](https://s3.amazonaws.com/udacity-sdc/github/shield-carnd.svg)](http://www.udacity.com/drive)

<img src="examples/laneLines_thirdPass.jpg" width="480" alt="Combined Image" />

Overview
---

The goal of the project is to find the lane lines on the road in the images 
using OpenCV-Python library.  A processing pipeline was designed similar to 
the one presented during the class. 

Running the Code 
---

*Python 3 is required to run this code.  The instructions are for Mac OS*

Install git and clone the project first
```
$> git clone https://gitlab.com/dmit.litvak/sdcnd-term1-proj1-finding-lane.git
$> cd sdcnd-term1-proj1-finding-lane
```

You can run the project either with Conda or in Python environment.
In the former case, you would need to install either Microconda or Anaconda.
In the latter case, you will need *pip*, python's package manager.

For Conda, create the environment first 

```conda env create -f conda_sdcnd_term1_env.yml```

Verify that *carnd-term1* environment was created  

```conda info --envs```

Activate the environment 

```source activate carnd-term1```

Now you can execute either *image_pipe.py* or *movie_pipe.py*.
To deactivate, run `source deactivate`.

For Python, you would need to learn to work with virtual environments
```
$> pip3 install virtualenv
$> virtualenv venv
$> pip3 install pip3_requirements.txt
$> source venv/bin/activate
$> image_pipe.py
$> deactivate
```
_**Disclaimer:**_ I have not tested the pip3 vurtualenv.



Project Files and Directories 
---

* __P1.ipynb__  Jupyter notebook for the project		

* __image_pipe.py__   MAIN1: reads images from *test_images* directory and 
sends them to *draw_lane_pipeline* in *pipeline_functions.py*		
* __movie_pipe.py__   MAIN2: same as *image_pipe.py* for processing video clips from *test_videos*
directory
* __pipeline_functions.py__    Pipeline implementation with *draw_lane_pipeline* main function 
* __pip3_requirements.txt__    *pip3 freeze* output to run the pipeline 
* __conda_sdcnd_term1_env.yml__ Anaconda environment for pipeline execution		

* __test_images, test_images_output__	image in and output directories	
* __test_videos, test_videos_output__	image in and output directories	

* __examples__ solution example directory	

