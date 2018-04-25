'''
main.py

The entry point of the program
'''

import multiprocessing
import sys

from GUI_Interface import GUIInterface
from Text_Interface import TextInterface

def _text_interface_wrapper(camera_serial):
    instance = TextInterface(camera_num=camera_serial)
    instance.run()

def _gui_interface_wrapper(camera_serial):
    instance = GUIInterface(camera_num=camera_serial)
    instance.run()

def launch_camera_instances(camera_num=0, interface_opt="text"):

    job_query = []
    for num in range(camera_num):
        if interface_opt == "text":
            job_query.append(multiprocessing.Process(target=_text_interface_wrapper, args=(num,)))
        else:
            job_query.append(multiprocessing.Process(target=_gui_interface_wrapper, args=(num,)))

    for job in job_query:
        job.start()

    # for job in job_query:
    #     job.join()

if __name__ == "__main__":
    _text_interface_wrapper(0)
    # camera_num = int(sys.argv[1])
    # launch_camera_instances(camera_num, "text")
