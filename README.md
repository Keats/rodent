# Find out who the fuck is eating my lunch at night

## Goal
See title

## Installation

```python
pip install -r requirements.txt
```

OpenCV is not pip installable so follow the instructions for your OS at [the download page](http://opencv.org/downloads.html) (you can install it in a virtualenv by following this post: [Installation of Opencv, numpy, scipy inside a virtualenv](https://medium.com/@manuganji/installation-of-opencv-numpy-scipy-inside-a-virtualenv-bf4d82220313)).  

Don't forget to install dependencies (jpg lib and ffmpeg or something that works with opencv, libav for Ubuntu).  
On Ubuntu:

```bash
$ sudo apt-get install libjpeg-dev libavcodec-dev libavformat-dev libswscale-dev
```

## How to use
```python
$ python rodent.py --help
```
