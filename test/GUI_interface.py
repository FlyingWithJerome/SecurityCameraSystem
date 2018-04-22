'''
GUI_Interface.py
'''

import cProfile
import threading
import time
from datetime import datetime

from PIL import Image
from PIL import ImageTk
import Tkinter as tk
import imutils
import cv2


from face_detection import Detector

class Interface(object):

    def __init__(self, camera_num=0):
        self.__gui_root = tk.Tk()

        self.__btn_frame = tk.Frame()
        self.__btn_frame.pack(side="bottom")

        self.__exit_btn = tk.Button(self.__btn_frame, text="Exit", command=self.__destroy)
        self.__exit_btn.pack(side="left", fill="both", expand="yes", padx=5, pady=5)

        self.__start_btn = tk.Button(self.__btn_frame, text="Start", command=self.__start)
        self.__start_btn.pack(side="left", fill="both", expand="yes", padx=5, pady=5)

        self.__pause_btn = tk.Button(self.__btn_frame, text="Pause", command=self.__pause)
        self.__pause_btn.pack(side="left", fill="both", expand="yes", padx=5, pady=5)

        self.__process_window = tk.Text()
        self.__process_window.pack(side="right")
        self.__process_window.insert(tk.END, "Initializing Camera {}...\n".format(camera_num))
        self.__gui_root.wm_title("Camera {:d}".format(camera_num))

        self.__panel = None
        self.__destroyed = False
        self.__isrunning = True
        self.__event_level = 1
        self.__camera_num = camera_num
        self.__test_video = cv2.VideoCapture(camera_num)

        self.__image = None
        self.__event_str = None
        self.__event_changed = False

        self.__detector = Detector(method="Haar_frontalface", video_handler=self.__test_video)

        self.__event_lock = threading.Lock()

        self.__frame_executor = threading.Thread(target=self.__get_frame)
        self.__frame_executor.setDaemon(True)
        self.__frame_executor.start()

        self.__event_lvl_executor = threading.Thread(target=self.__get_event_level)
        self.__event_lvl_executor.setDaemon(True)
        self.__event_lvl_executor.start()

    
    def __start(self):
        self.__isrunning = True

    def __pause(self):
        self.__isrunning = False

    def __destroy(self):
        del self.__detector
        self.__test_video.release()
        self.__destroyed = True

        self.__isrunning = False
        self.__gui_root.destroy()
        self.__gui_root.quit()

    def __get_frame(self):

        order = 0
        while(self.__isrunning):
            if (not self.__destroyed) and self.__test_video.isOpened():
                if order % 12 == 0:
                    self.__image = self.__detector.get_frame_single(skip=False)
                else:
                    self.__image = self.__detector.get_frame_single(skip=True)

                order += 1
                # ret, frame = self.__test_video.read()
                # if ret:
                #     self.__image = frame
                # time.sleep(2)

    def __get_event_level(self):
        while(self.__isrunning):
            if not self.__destroyed:
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
                self.__event_lock.acquire()
                self.__event_level = event_lvl
                self.__event_str = fmt
                self.__event_changed = True
                self.__event_lock.release()

    
    def run(self):
        while(self.__isrunning):
            if self.__image is not None:
                im = Image.fromarray(self.__image)

                if not self.__destroyed:
                    im = ImageTk.PhotoImage(im)
                else:
                    break

                if not self.__panel:
                    self.__panel = tk.Label(self.__gui_root, image=im)
                    self.__panel.image = im
                    self.__panel.pack(side="left", padx=10, pady=10)
                else:
                    self.__panel.configure(image=im)
                    self.__panel.image = im
                
                self.__event_lock.acquire()
                if self.__event_changed:
                    self.__process_window.insert(tk.END, self.__event_str)
                    self.__event_changed = False
                self.__event_lock.release()

                self.__gui_root.update()

    def __del__(self):
        self.__test_video.release()
        self.__gui_root.quit()

if __name__ == "__main__":
    i = Interface()
    cProfile.run("i.run()")
