import os

import cv2
from PIL import Image


def clear_directory(folder):
    """
    Delete all the pics in the given folder
    """
    for filename in os.listdir(folder):
        os.remove('%s/%s' % (folder, filename))


def save_image(image, folder, now):
    """
    Save an image using OpenCV and then resaves it using
    PIL for better compression
    """
    filename = '%s/%s.jpg'
    filepath = filename % (folder, now)
    cv2.imwrite(filepath, image)

    # Resave it with pillow to do a better compression
    img = Image.open(filepath)
    img.save(filepath, optimize=True, quality=80)


def time_over(until, now):
    """
    Checks if we are over the time we want to film until.
    Splits on every loop but it's not like it's a big
    performance drain.
    """
    if until is None:
        return False

    until_hour, until_minutes = until.split(':')
    hour = int(until_hour)
    minutes = int(until_minutes)

    # If we want to watch something overnight, now will be greater before midnight
    if hour < 12 and now.hour > 12:
        return False
    if now.hour > hour or (now.hour == hour and now.minute >= minutes):
        return True


def find_motion_boundaries(data):
    """
    data is a numpy ndarray of the image following the format
    [
        [0, 0, 0, 0, 255, 0, ...]
        [..]
    ]
    255 are the values we are interested in, which means a motion was
    detected at that pixel.
    We want to find out the smallest rectangle that matches all the
    motions.
    Returns 2 points forming the diagonal for the rectangle or None, None
    if it didn't have any motion.
    """
    number_changes = 0
    # Bear with me with these names
    # this is going to be used to put a rectangle around where the motion
    # is
    low_x = len(data[0])
    high_x = 0
    low_y = len(data)
    high_y = 0

    for i, row in enumerate(data):
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

    if number_changes == 0:
        return None, None

    low_x = low_x - 5 if low_x >= 5 else low_x
    low_y = low_y - 5 if low_y >= 5 else low_y
    high_x = high_x + 5 if high_x >= len(data[0]) - 6 else high_x
    high_y = high_y + 5 if high_y >= len(data) - 6 else high_y

    return (low_x, low_y), (high_x, high_y)
