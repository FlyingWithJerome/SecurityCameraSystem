'''
Text Interface.py

This module represents the text interface for the camera system
'''

from

class TextInterface(object):

    def __init__(self, camera_num=0):
        self.__camera_num = camera_num
        self.__test_video = cv2.VideoCapture(camera_num)

        self.__image = None
        self.__event_str = None
        self.__event_changed = False

        self.__detector = Detector(method="Haar_upperbody", video_handler=self.__test_video)