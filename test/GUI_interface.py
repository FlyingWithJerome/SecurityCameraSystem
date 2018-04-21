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

from face_detection import Detector

class Interface(object):

    def __init__(self):
        self.__gui_root = tk.Tk()
        self.__btn = tk.Button(self.__gui_root, text="Exit!", command=self.__destroy)
        self.__btn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

        self.__gui_root.wm_title("Test")
        self.__panel = None
        self.__destroyed = False

        self.__test_video = cv2.VideoCapture(0)
        

        self.__detector = Detector(method="Haar_frontalface", video_handler=self.__test_video)
        self.__executor = threading.Thread(target=self.__get_frame)
        self.__image = None
        self.__executor.isdaemon = True
        self.__executor.start()
        # self.__executor.join()

    def __destroy(self):
        del self.__detector
        self.__destroyed = True
        self.__gui_root.destroy()
        self.__gui_root.quit()
        self.__test_video.release()

        exit(1)

    def __get_frame(self):

        order = 0
        while(True):
            if (not self.__destroyed) and self.__test_video.isOpened():
                if order % 7 == 0:
                    self.__image = self.__detector.get_frame_single(skip=False)
                else:
                    self.__image = self.__detector.get_frame_single(skip=True)
                # ret, frame = self.__test_video.read()
                # if ret:
                #     self.__image = frame
                # time.sleep(2)
            
    def run(self):
        while(True):
            if self.__image is not None:
                # print("running GUI")

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
                self.__gui_root.update()

    def __del__(self):
        print("released")
        self.__test_video.release()
        # self.__destroy
        self.__gui_root.quit()

if __name__ == "__main__":
    i = Interface()
    try:
        i.run()
    except KeyboardInterrupt:
        exit(0)