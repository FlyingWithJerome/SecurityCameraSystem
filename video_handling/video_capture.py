'''
video_capture.py

video capture module. This module handles everything
about the camera, and wraps the av into a stream
'''
import cv2
import atexit

capture_base = cv2.VideoCapture(0)

atexit.register(lambda : capture_base.release())

class CameraHandler(object):
    '''
    CameraHandler is in singleton mode, because we do not
    want handlers to compete one single camera. It is OK we
    have more camera in the future

    CameraHandler is also a generator, which is mainly the way it generates
    frames to others.
    '''
    num_of_instance = 0

    def __init__(self, queue_, camera_serial=0):
        # if CameraHandler.num_of_instance > 0:
        #     raise TypeError("Cannot have more than one camera handler")
        # else:
        CameraHandler.num_of_instance += 1

        self.__queue     = queue_
        self.__isworking = False

    def start(self):
        self.start_capture()
        while(True):
            try:
                ret, frame = next(self)
                if ret:
                    self.__queue.put(frame)
            except KeyboardInterrupt:
                break
            except:
                break
        self.end_capture()

    def isworking(self):
        return self.__isworking and capture_base.isOpened()

    def start_capture(self):
        self.__isworking = True

    def __iter__(self):
        return self

    def __next__(self):
        return self.__next_frame()

    def next(self):
        return self.__next__()

    def __next_frame(self):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.end_capture()

        ret, frame = capture_base.read()
        return ret, frame


    def end_capture(self):
        capture_base.release()

    def __del__(self):
        self.__isworking = False
        CameraHandler.num_of_instance -= 1

        capture_base.release()

if __name__ == "__main__":
    cap = CameraHandler(None)
    while(True):
    # Capture frame-by-frame
        ret, frame = next(cap)

        # Our operations on the frame come here
        # Display the resulting frame
        if not frame is None:
            cv2.imshow('frame',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

