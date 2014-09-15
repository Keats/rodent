"""
Rodent

Usage:
  rodent.py capture [--until=<time>] [--folder=<folder>] [--interval=<interval>]
  rodent.py make_video [--folder=<folder>]
  rodent.py automate [--until=<time>] [--folder=<folder>] [--interval=<interval>]

Options:
  -h --help               Show this screen
  --until=<time>          Until when to record, needs to be a HH:MM format (ie 12:45)
  --folder=<folder>       The folder in which the pictures are stored [default: photos]
  --interval=<interval>   The interval between 2 photos [default: 1]
"""

import datetime
import os
import time
import sys

import cv2
from docopt import docopt
from PIL import Image


def clear_directory(folder):
    """
    Delete all the pics in the photos directory
    """
    for filename in os.listdir(folder):
        os.remove('%s/%s' % (folder, filename))


def start_camera(folder, interval, until=None):
    """
    Start taking pictures every interval.
    If until is specified, it will take pictures
    until that time is reached (24h format).
    Needs to be of the following format: HH:MM
    """
    clear_directory(folder)

    camera = cv2.VideoCapture(0)
    filename = '%s/%s.jpg'
    number = 0

    if until:
        until_hour, until_minutes = until.split(':')
        until_hour = int(until_hour)
        until_minutes = int(until_minutes)

    while True:
        number += 1
        _, image = camera.read()
        now = datetime.datetime.now()
        print 'Taking picture number %d at %s' % (number, now.isoformat())
        # Tried [cv2.cv.CV_IMWRITE_PNG_COMPRESSION, 3] but still atrocious compression
        filepath = filename % (folder, now)
        cv2.imwrite(filepath, image)

        # Resave it with pillow to do a better compression
        img = Image.open(filepath)
        img.save(filepath, optimize=True, quality=80)

        if until:
            # If we want to watch something overnight, now will be greater before midnight
            if until_hour < 12 and now.hour > 12:
                time.sleep(interval)
                continue
            if now.hour > until_hour or (now.hour == until_hour and now.minute >= until_minutes):
                break

        time.sleep(interval)

    del(camera)


def make_video(folder):
    """
    Takes all the pics in the folder given and make a video
    out of it.
    """
    # Sorting on dates, ISO ftw
    filenames = sorted(os.listdir(folder))

    # Find out size of the pictures we're taking
    first_pic = cv2.imread('%s/%s' % (folder, filenames[0]))

    # shape gives a tuple (height, width, layer)
    height, width, _ = first_pic.shape
    # magic below, might need to change the codec for your own webcam
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    video = cv2.VideoWriter('output.avi', fourcc, 10, (width, height))

    for filename in filenames:
        video.write(cv2.imread('%s/%s' % (folder, filename)))

    video.release()


def motion_detection():
    pass

if __name__ == "__main__":
    arguments = docopt(__doc__)

    folder = arguments['--folder']
    interval = int(arguments['--interval'])
    until = arguments['--until']

    if arguments['capture']:
        start_camera(folder, interval, until)
    elif arguments['make_video']:
        make_video(folder)
    elif arguments['automate']:
        start_camera(folder, interval, until)
        make_video(folder)
