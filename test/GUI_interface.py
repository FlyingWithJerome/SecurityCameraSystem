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


class Interface(object):

    def __init__(self):
        self.__gui_root = tk.Tk()
        self.__btn = tk.Button(self.__gui_root, text="Exit!", command=exit)
        self.__btn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

        self.__gui_root.wm_title("Test")
        self.__panel = None
        self.__test_video = cv2.VideoCapture(0)
        self.__executor = threading.Thread(target=self.__get_frame)
        self.__image = None
        self.__executor.start()
        # self.__executor.join()

    def __destroy(self):
        self.__gui_root.destroy()

    def __get_frame(self):

        while(True):
            ret, frame = self.__test_video.read()
            if ret:
                # image = Image.fromarray(frame)
                self.__image = frame
                # time.sleep(2)
            
    def run(self):
        while(True):
            if self.__image is not None:
                im = Image.fromarray(self.__image)
                im = ImageTk.PhotoImage(im)
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
        # self.__gui_root.quit()

if __name__ == "__main__":
    i = Interface()
    try:
        i.run()
    except KeyboardInterrupt:
        exit(0)