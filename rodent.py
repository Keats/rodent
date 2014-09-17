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


def start_camera(camera, folder, interval, until=None):
    """
    Start taking pictures every interval.
    If until is specified, it will take pictures
    until that time is reached (24h format).
    Needs to be of the following format: HH:MM
    """
    clear_directory(folder)

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
    video = cv2.VideoWriter('output.avi', fourcc, 30, (width, height))

    for filename in filenames:
        video.write(cv2.imread('%s/%s' % (folder, filename)))

    video.release()


def motion_detection(camera, folder, until):
    clear_directory(folder)

    filename = '%s/%s.jpg'
    if until:
        until_hour, until_minutes = until.split(':')
        until_hour = int(until_hour)
        until_minutes = int(until_minutes)

    previous_image = None
    current_image = None

    while True:
        now = datetime.datetime.now()
        ret, image = camera.read()
        gray_image = cv2.cvtColor(image, cv2.cv.CV_RGB2GRAY)
        # Haven't got a previous image, meaning first image at all
        if previous_image is None:
            previous_image = gray_image
            continue

        if current_image is None:
            current_image = gray_image;
            continue

        difference1 = cv2.absdiff(previous_image, gray_image)
        difference2 = cv2.absdiff(current_image, gray_image)
        result = cv2.bitwise_and(difference1, difference2)

        _, result = cv2.threshold(result, 35, 255, cv2.THRESH_BINARY)


        # Let's show a square around the detected motion in the original pic
        result = result.tolist()
        number_changes = 0
        # Bear with me with these names
        # this is going to be used to put a rectangle around where the motion
        # is
        low_x = len(result[0])
        high_x = 0
        low_y = len(result)
        high_y = 0

        for i, row in enumerate(result):
            for j, column in enumerate(row):
                if column != 255:
                    continue

                number_changes += 1
                if low_y > i:
                    low_y = i
                if high_y < i:
                    high_y = i

                if low_x > j:
                    low_x = j
                if high_x < j:
                    high_x = j

        # Don't bother if no pixels changed
        if number_changes > 1:
            low_x = low_x - 5 if low_x >= 5 else low_x
            low_y = low_y - 5 if low_y >= 5 else low_y
            high_x = high_x + 5 if high_x >= len(result[0]) - 6 else high_x
            high_y = high_y + 5 if high_y >= len(result) - 6 else high_y

            cv2.rectangle(image, (low_x, low_y), (high_x, high_y), (140, 25, 71), 3) # purple
            print 'Motion detected ! Taking picture'
            cv2.imwrite(filename % (folder, now), image)

        previous_image = current_image
        current_image = gray_image


        if until:
            # If we want to watch something overnight, now will be greater before midnight
            if until_hour < 12 and now.hour > 12:
                time.sleep(interval)
                continue
            if now.hour > until_hour or (now.hour == until_hour and now.minute >= until_minutes):
                break

        time.sleep(0.1)

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
        del(camera)
