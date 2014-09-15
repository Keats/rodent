"""
Rodent

Usage:
  rodent.py capture [--until=<time>]
  rodent.py make_video
  rodent.py automate [--until=<time>]

Options:
  -h --help          Show this screen
  --until=<time>     Until when to record, needs to be a HH:MM format (ie 12:45)

"""

import datetime
import os
import time
import sys

import cv2
from docopt import docopt


def clear_directory():
    """
    Delete all the pics in the photos directory
    """
    for filename in os.listdir('photos'):
        os.remove('photos/%s' % filename)

def start_camera(until=None, interval=1):
    """
    Start taking pictures every interval.
    If until is specified, it will take pictures
    until that time is reached (24h format).
    Needs to be of the following format: HH:MM
    """
    clear_directory()

    camera = cv2.VideoCapture(0)
    filename = 'photos/%s.png'
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
        cv2.imwrite(filename % now, image)

        if until:
            if now.hour > until_hour or (now.hour == until_hour and now.minute >= until_minutes):
                break

        time.sleep(interval)

    # We don't really care here, we will Ctrl+C anyway
    del(camera)


def make_video():
    # Cheating a bit, dimensions are 640x380
    # Sorting on dates, ISO ftw
    filenames = sorted(os.listdir('photos'))

    # Find out size of the pictures we're taking
    filename = 'photos/%s.png'
    first_pic = cv2.imread('photos/%s' % filenames[0])

    # first_pic.shape gives a tuple (height, width, layer)
    height, width, _ = first_pic.shape
    fourcc = cv2.cv.CV_FOURCC(*'XVID')

    video = cv2.VideoWriter('output.avi', fourcc, 10, (width, height))

    for filename in filenames:
        video.write(cv2.imread('photos/%s' % filename))

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    arguments = docopt(__doc__)

    if arguments['capture']:
        start_camera(arguments['--until'])
    elif arguments['make_video']:
        make_video()
    elif arguments['automate']:
        start_camera(arguments['--until'])
        make_video()
