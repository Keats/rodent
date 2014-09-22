# Find out who/what the fuck is eating my lunch at night

![Rodent](/logo.png)

## Goal
See title.  
Takes picture every time interval (defaults to one picture a second) and make a video of it at the end.  
It has a motion detection mode that will detect motion and put a purple rectangle around it (by default it does not do a video at the end but you can call make_video manually if you want to).

## Installation

```python
pip install -r requirements.txt
```
Don't forget to install dependencies (jpg lib and ffmpeg or something that works with opencv, libav for Ubuntu) for OpenCV before installing it, otherwise things won't work.
On Ubuntu:

```bash
$ sudo apt-get install libjpeg-dev libavcodec-dev libavformat-dev libswscale-dev
```

OpenCV is not pip installable so either install it from your package manager or follow the instructions for your OS at [the download page](http://opencv.org/downloads.html) (you can install it in a virtualenv by following this post: [Installation of Opencv, numpy, scipy inside a virtualenv](https://medium.com/@manuganji/installation-of-opencv-numpy-scipy-inside-a-virtualenv-bf4d82220313)).  


## How to use
```python
$ python rodent.py
```
There are 4 commands:

- capture: takes a picture from the webcam at a given interval forever or until the time specified in the folder given
- make_video: takes all the pictures in the folder and makes a video out of it (better than watching pictures!)
- automate: does both capture and make_video, I use it for example to record until 15 minutes before I wake up and the video will be ready by the time I get to the kitchen for example
- motion: takes a picture only if it detects a movement


## How it works
Look at the [article on my blog](http://vincent.is/turning-a-laptop-into-cctv/)
