'''
main.py

The entry point of the program
'''

import argparse
import threading
import multiprocessing
import signal
import sys

# import gevent

from GUI_Interface import GUIInterface
from Text_Interface import TextInterface

def parse_arguments():
    parser = argparse.ArgumentParser(description='Security Camera Parser')

    parser.add_argument('number of cameras', type=int, nargs=1, default=1, help='number of cameras connected')
    parser.add_argument('detection method', type=str, nargs='?', default="haar_face", help="methods of classifier")
    parser.add_argument('event logic', type=str, nargs='?', default="threshold", help="how the system intensifies the alarms")
    parser.add_argument('running on Pi', type=str, nargs='?', default="nopi", help="whether it is running on Pi")

    args = parser.parse_args()
    args = vars(args)

    detection_map =\
    {
        "haar_face" : "Haar_frontalface",
        "haar_upper": "Haar_upperbody",
        "hog"       : "HOG"
    }
    
    [camera_num]  = args["number of cameras"]
    detect_method = detection_map[args["detection method"]]
    event_logic   = args["event logic"]
    is_onpi       = args["running on Pi"].lower() == "pi"

    return [
        {
            "camera_serial" : i,
            "detect_method" : detect_method,
            "event_logic"   : event_logic,
            "on_pi"         : is_onpi
        }
        for i in range(camera_num)
    ]


def _exit_handler(sig, frame):
    exit(0)

def _text_interface_wrapper(camera_serial, **arguments):
    signal.signal(signal.SIGINT, _exit_handler)
    instance = TextInterface(camera_num=camera_serial, **arguments)
    instance.run()

def _gui_interface_wrapper(camera_serial, **arguments):
    signal.signal(signal.SIGINT, _exit_handler)
    instance = GUIInterface(camera_num=camera_serial, **arguments)
    instance.run()

def launch_camera_instances(list_of_args, interface_opt="text"):

    job_query = []
    for arg in list_of_args:
        if interface_opt == "text":
            job_query.append(multiprocessing.Process(target=_text_interface_wrapper, kwargs=arg))
        else:
            job_query.append(multiprocessing.Process(target=_gui_interface_wrapper, kwargs=arg))

    for job in job_query:
        job.start()


if __name__ == "__main__":

    args = parse_arguments()

    try:
        multiprocessing.set_start_method("spawn")
    except:
        print("Please note that some OpenCV libraries and tkinter require to be executed in main process/thread")
        pass
    finally:
        launch_camera_instances(args, interface_opt="gui")
