'''
serial_number.py

This module generates the output file names
for videos and pictures

'''

import time
from datetime import date

class FileName:
    _VIDEO_SERIAL   = 1
    _PICTURE_SERIAL = 1

    def get_filename(type_='video'):
        '''
        get the next available file name
        '''
        if type_ == "video":
            # suffix = str(_VIDEO_SERIAL) + '.avi'
            # _VIDEO_SERIAL += 1
            suffix = ".avi"

        elif type_ == "picture":
            suffix = str(FileName._PICTURE_SERIAL) + '.jpg'
            _PICTURE_SERIAL += 1
            suffix = ".png"

        else:
            raise ValueError()

        time_string_format = "%H_%M_%A_%B_%d_%Y" 
        time_string = date.fromtimestamp(time.time()).strftime(time_string_format)
        return time_string + suffix 
