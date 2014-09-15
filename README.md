# Find out who the fuck is eating my lunch at night

## Goal
See title

## Installation

```python
pip install -r requirements.txt
```

OpenCV is not pip installed so follow the instructions for your OS at http://opencv.org/downloads.html (you can install it in a virtualenv by following https://medium.com/@manuganji/installation-of-opencv-numpy-scipy-inside-a-virtualenv-bf4d82220313).  

Don't forget to install dependencies (jpg lib and ffmpeg or something that works with opencv).  
On Ubuntu:

```bash
$ sudo apt-get install libjpeg-dev libavcodec-dev libavformat-dev libswscale-dev
```

## How to use
```python
$ python rodent.py --help
```
