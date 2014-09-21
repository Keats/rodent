"""
Rodent

Usage:
  rodent.py capture [--until=<time>] [--folder=<folder>] [--interval=<interval>]
  rodent.py make_video [--folder=<folder>]
  rodent.py automate [--until=<time>] [--folder=<folder>] [--interval=<interval>]
  rodent.py motion [--until=<time>] [--folder=<folder>]

Options:
  -h --help               Show this screen
  --until=<time>          Until when to record, needs to be a HH:MM format (ie 12:45)
  --folder=<folder>       The folder in which the pictures are stored [default: photos]
  --interval=<interval>   The interval between 2 photos [default: 1]
"""

import datetime
import os
import time

import cv2
from docopt import docopt

import utils


def start_camera(camera, folder, interval, until=None):
    """
    Start taking pictures every interval.
    If until is specified, it will take pictures
    until that time is reached (24h format).
    Needs to be of the following format: HH:MM
    """
    utils.clear_directory(folder)
    number = 0

    while True:
        _, image = camera.read()
        now = datetime.datetime.now()

        number += 1
        print 'Taking picture number %d at %s' % (number, now.isoformat())
        utils.save_image(image, folder, now)

        if utils.time_over(until, now):
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

    # Completely arbitrary values, probably will need to fix that later
    # If the video is too fast or too slow, change the fps value manually
    fps = 2
    if 20 <= len(filenames) <= 40:
        fps = 4
    elif 41 <= len(filenames) <= 200:
        fps = 10
    elif 201 <= len(filenames) <= 500:
        fps = 20
    elif len(filenames) > 500:
        fps = 40

    # Find out size of the pictures we're taking
    first_pic = cv2.imread('%s/%s' % (folder, filenames[0]))

    # shape gives a tuple (height, width, layer)
    height, width, _ = first_pic.shape

    # magic below, might need to change the codec for your own webcam
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    video = cv2.VideoWriter('output.avi', fourcc, fps, (width, height))

    for filename in filenames:
        video.write(cv2.imread('%s/%s' % (folder, filename)))

    video.release()


def motion_detection(camera, folder, until):
    """
    Uses 3 frames to look for motion, can't remember where
    I found it but it gives better result than my first try
    with comparing 2 frames.
    """
    utils.clear_directory(folder)

    # Need to get 2 images to start with
    previous_image = cv2.cvtColor(camera.read()[1], cv2.cv.CV_RGB2GRAY)
    current_image = cv2.cvtColor(camera.read()[1], cv2.cv.CV_RGB2GRAY)
    purple = (140, 25, 71)

    while True:
        now = datetime.datetime.now()
        _, image = camera.read()
        gray_image = cv2.cvtColor(image, cv2.cv.CV_RGB2GRAY)

        difference1 = cv2.absdiff(previous_image, gray_image)
        difference2 = cv2.absdiff(current_image, gray_image)
        result = cv2.bitwise_and(difference1, difference2)

        # Basic threshold, turn the bitwise_and into a black or white (haha)
        # result, white (255) being a motion
        _, result = cv2.threshold(result, 40, 255, cv2.THRESH_BINARY)

        # Let's show a square around the detected motion in the original pic
        low_point, high_point = utils.find_motion_boundaries(result.tolist())
        if low_point is not None and high_point is not None:
            cv2.rectangle(image, low_point, high_point, purple, 3)
            print 'Motion detected ! Taking picture'
            utils.save_image(image, folder, now)

        previous_image = current_image
        current_image = gray_image

        if utils.time_over(until, now):
            break

    del(camera)

if __name__ == "__main__":
    arguments = docopt(__doc__)

    folder = arguments['--folder']
    interval = int(arguments['--interval'])
    until = arguments['--until']

    camera = cv2.VideoCapture(0)

    try:
        if arguments['capture']:
            start_camera(camera, folder, interval, until)
        elif arguments['make_video']:
            make_video(folder)
        elif arguments['automate']:
            start_camera(camera, folder, interval, until)
            make_video(folder)
        elif arguments['motion']:
            motion_detection(camera, folder, until)
    except KeyboardInterrupt:
        # OpenCV doesn't like CTRL+C sometimes.
        del(camera)
