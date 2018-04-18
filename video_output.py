'''
video_output.py

video_output module handles everything on video writting
'''

try:
    import Queue as queue
except ImportError:
    import queue

import sys
sys.path.append("..")

import cv2

from utils.serial_number import FileName

class VideoExporter(object):

    def __init__(self, queue_, format_='MJPG'):
        
        self.__video_format = cv2.VideoWriter_fourcc(*format_)
        self.__master_writter = cv2.VideoWriter("out.avi", self.__video_format, 20.0, (1280, 720))
        self.__queue      = queue_
        cv2.startWindowThread() 
        self.__show = False

    def start(self):
        while(True):
            try:
                frame = self.__queue.get_nowait()
                print("video export gets one")
                # if frame == -1:
                #     raise EOFError("BREAK")

                self.__write(frame, "picture")

            except (EOFError, KeyboardInterrupt):
                break
            
            except queue.Empty:
                pass

    def __write(self, frame, mode='video'):
        
        if mode == "video":
            self.__master_writter.write(frame)

        elif mode == "picture":
            print("write one")
            cv2.imwrite("picture.png", frame)
        
    def __del__(self):
        self.__master_writter.release()
        cv2.destroyAllWindows()