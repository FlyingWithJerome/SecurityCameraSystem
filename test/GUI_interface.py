'''
GUI_Interface.py
'''

from PIL import Image
from PIL import ImageTk
import Tkinter as tk
import threading
import imutils
import cv2
import time

from datetime import datetime

from face_detection import Detector

class Interface(object):

    def __init__(self, camera_num=0):
        self.__gui_root = tk.Tk()
        self.__btn = tk.Button(self.__gui_root, text="Exit!", command=self.__destroy)
        self.__btn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)
        self.__process_window = tk.Text()
        self.__process_window.pack(side="right")
        self.__process_window.insert(tk.END, "Initializing Camera {}...".format(camera_num))
        self.__gui_root.wm_title("Test")

        self.__panel = None
        self.__destroyed = False
        self.__isrunning = True
        self.__event_level = 1
        self.__camera_num = camera_num
        self.__test_video = cv2.VideoCapture(camera_num)

        self.__image = None
        self.__event_str = None
        self.__event_changed = False

        self.__detector = Detector(method="Haar_upperbody", video_handler=self.__test_video)

        self.__frame_executor = threading.Thread(target=self.__get_frame)
        self.__frame_executor.setDaemon(True)
        self.__frame_executor.start()

        self.__event_lvl_executor = threading.Thread(target=self.__get_event_level)
        self.__event_lvl_executor.setDaemon(True)
        self.__event_lvl_executor.start()
        # self.__executor.join()

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

                fmt = "[{:}] Camera {} Event {} {} {}\n".format(\
                time_now, self.__camera_num, self.__event_level, verb, event_lvl
                )
                self.__event_level = event_lvl
                self.__event_str = fmt
                self.__event_changed = True

    
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
                
                if self.__event_changed:
                    self.__process_window.insert(tk.END, self.__event_str)
                    self.__event_changed = False
                self.__gui_root.update()

    def __del__(self):
        print("released")
        self.__test_video.release()
        # self.__destroy
        self.__gui_root.quit()

if __name__ == "__main__":
    i = Interface()
    i.run()
    # except KeyboardInterrupt:
    exit(0)