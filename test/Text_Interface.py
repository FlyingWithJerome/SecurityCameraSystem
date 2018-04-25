'''
Text Interface.py

This module represents the text interface for the camera system
'''

import cProfile
import gc
import threading
import time
from datetime import datetime

import cv2

from face_detection import Detector

class TextInterface(object):

    def __init__(self, camera_num=0):

        print("Initializing Camera {}...".format(camera_num))
        self.__camera_num = camera_num
        self.__test_video = cv2.VideoCapture(camera_num)

        self.__event_str = None
        self.__event_changed = False
        self.__isrunning = True
        self.__event_level = 1

        self.__detector = Detector(method="Haar_upperbody", video_handler=self.__test_video, on_pi=False)

        print("Initialization Finished")

    def __get_frame(self):

        order = 0
        while(self.__isrunning):
            if (not self.__destroyed) and self.__test_video.isOpened():
                if order % 12 == 0:
                    self.__image = self.__detector.get_frame_single(skip=False)
                else:
                    self.__image = self.__detector.get_frame_single(skip=True)
                order += 1

    def __get_event_level(self):
        while(self.__isrunning):
            try:
                event_lvl = self.__detector.get_event_level()
            except AttributeError:
                break

            if event_lvl != self.__event_level:
                time_now = str(datetime.now())[:-7]
                verb = "raised to" if event_lvl > self.__event_level else "lowered to"

                fmt = "[Camera {}] <{}> Event {} {} {}\n".format(\
                self.__camera_num, time_now, self.__event_level, verb, event_lvl
                )
                self.__event_level = event_lvl
                print(fmt)

    
    def run(self):
        while(self.__isrunning):

                if self.__event_level == 3:
                    alarm = threading.Thread(target=alarm.send_alarm)
                    alarm.start()

                gc.collect()


    def __del__(self):
        del self.__detector
        self.__test_video.release()

if __name__ == "__main__":
    t = TextInterface()
    t.run()