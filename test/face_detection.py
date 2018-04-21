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

# from frame_tag import Tag

class Detector(object):

    def __init__(self, camera_serial=0, method="Haar", video_format="MJPG"):

        # print("detector initializing")

        if method == "Haar":
            # self.__cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')
            self.__cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

        elif method == "HOG":
            self.__cascade = cv2.HOGDescriptor()
            self.__cascade.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        self.__camera  = cv2.VideoCapture(camera_serial)
        self.__writer = cv2.VideoWriter("out.avi", cv2.VideoWriter_fourcc(*video_format), 24, (1280, 720))
        self.__method = method
        self.__output_buffer  = None
        self.__size_buffer    = []
        # self.__queue_in       = queue_capture
        # self.__queue_out      = queue_output

        self.__event_level    = 1
        self.__frame_step     = 5

    def main_loop(self):
        self.__get_frame_block()

    def __get_frame_block(self):
        skip_iteration = 0
        while(True):
            try:
                ret, frame = self.__camera.read()
                if not ret:
                    continue
                self.__detect_face(frame)

                if skip_iteration % 30 == 0:
                    self.__check_event_logic()
                print("Event level: %d"%self.__event_level)

                if self.__event_level == 2:
                    self.__output_media(frame, "lo-res pic")

                elif self.__event_level == 3:
                    self.__output_media(frame, "hi-res pic")

                elif self.__event_level == 4:
                    self.__output_media(frame, "video")

                skip_iteration += 1

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
        (x, y, w, h) = (0, 0, 0, 0)

        if len(faces) > 0:
            if self.__method == "Haar":
                (x, y, w, h)  = faces[0]
                self.__append_to_size_buffer(w*2 + h*2)

            elif self.__method == "HOG":
                if len(faces[0]) > 0 and len(faces[0][0]) > 0: 
                    (x, y, w, h)  = faces[0][0]

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.imshow("frame", frame)
        cv2.waitKey(1)        
        
        self.__append_to_size_buffer(w*2 + h*2)

    
    def __output_media(self, frame, option="lo-res pic"):
        if option == "lo-res pic":
            cv2.imwrite("low resolution picture.jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
        elif option == "hi-res pic":
            cv2.imwrite("hi resolution picture.jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

        elif option == "video":
            self.__writer.write(frame)


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

    def __del__(self):
        cv2.destroyAllWindows()
        self.__camera.release()
        self.__writer.release()


if __name__ == "__main__":
    f = Detector()
    f.main_loop()


        
