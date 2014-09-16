# Find out who/what the fuck is eating my lunch at night

## Goal
See title.  
Takes picture every time interval (defaults to one picture a second) and make a video of it at the end.  
It has a motion detection mode that will detect motion and put a purple rectangle around it.  
By default it does not do a video at the end but you can call make_video manually if you want to.

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
$ python rodent.py --help
```
