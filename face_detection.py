'''
face_detection.py
'''

try:
    import Queue as queue
except ImportError:
    import queue

import numpy as np
import cv2
# import video_capture

from frame_tag import Tag

class Detector(object):

    def __init__(self, queue_capture, queue_output, method="Haar"):

        # print("detector initializing")

        if method == "Haar":
            self.__cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
        elif method == "HOG":
            self.__cascade = cv2.HOGDescriptor()
            self.__cascade.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        self.__method = method
        self.__output_buffer  = None
        self.__size_buffer    = []
        self.__queue_in       = queue_capture
        self.__queue_out      = queue_output

        self.__event_level    = 1
        self.__frame_step     = 5

        print("detector initialized")

    def start(self):
        self.__get_frame_block()

    def __get_frame_block(self):
        skip_iteration = 0
        while(True):
            try:
                frame = self.__queue_in.get_nowait()
                self.__detect_face(frame)
                if skip_iteration % 30 == 0:
                    self.__check_event_logic()
                print("Event level: %d"%self.__event_level)

                if self.__event_level == 2:
                    self.__queue_out.put(("lo-res picture", frame))

                elif self.__event_level == 3:
                    self.__queue_out.put(("hi-res picture", frame))

                elif self.__event_level == 4:
                    self.__queue_out.put(("video", frame))

                skip_iteration += 1

            except queue.Empty:
                pass

            except (EOFError, IOError, KeyboardInterrupt):
                break

    def __append_to_size_buffer(self, size):
        '''
        append to the size buffer, remove the earliest
        one if it reaches the size limit
        '''
        if len(self.__size_buffer) == 75:
            del self.__size_buffer[0]

        self.__size_buffer.append(size)

    def __is_approaching_for_long(self, is_approaching=True):
        '''
        check if the suspicious is keep approaching for
        the whole size buffer

        is_approaching: check it is approaching if true
        check it is leaving if false
        '''
        size_buffer_copy = self.__size_buffer[::self.__frame_step]
        size_buffer_copy.sort(reverse=not is_approaching)

        return size_buffer_copy == self.__size_buffer[::self.__frame_step]

    def __detect_face(self, frame):
        '''
        detect human faces and changes the event level if the condition
        matches
        '''
        faces = self.__cascade.detectMultiScale(frame)
        # if self.__method == "Haar":
        if len(faces) > 0:
            if self.__method == "Haar":
                (x, y, w, h)  = faces[0]
                self.__append_to_size_buffer(w*2 + h*2)
                return

            elif self.__method == "HOG":
                if len(faces[0]) > 0 and len(faces[0][0]) > 0: 
                    (x, y, w, h)  = faces[0][0]
                    self.__append_to_size_buffer(w*2 + h*2)
                    return
        
        self.__append_to_size_buffer(0)

    def __check_event_logic(self):
        '''
        change the event level based on the
        logic designed
        '''
        if 2 <= self.__event_level < 4:
            if len(self.__size_buffer) == 75:
                if self.__is_approaching_for_long(True):
                    self.__event_level += 1

                elif self.__is_approaching_for_long(False):
                    self.__event_level = 1

        elif self.__event_level == 1:
            if any(i > 0 for i in self.__size_buffer):
                self.__event_level += 1

        
