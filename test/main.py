'''
main.py

The entry point of the program
'''

import multiprocessing
import sys

from GUI_Interface import GUIInterface
from Text_Interface import TextInterface

def _text_interface_wrapper(camera_serial, is_pi):
    instance = TextInterface(camera_num=camera_serial, on_pi=is_pi)
    instance.run()

def _gui_interface_wrapper(camera_serial, is_pi):
    instance = GUIInterface(camera_num=camera_serial, on_pi=is_pi)
    instance.run()

def launch_camera_instances(camera_num=0, interface_opt="text", is_pi=False):

    job_query = []
    for num in range(camera_num):
        if interface_opt == "text":
            job_query.append(multiprocessing.Process(target=_text_interface_wrapper, args=(num, is_pi)))
        else:
            job_query.append(multiprocessing.Process(target=_gui_interface_wrapper, args=(num, is_pi)))

    for job in job_query:
        job.start()

    # for job in job_query:
    #     job.join()

if __name__ == "__main__":
    # _text_interface_wrapper(0)
    camera_num = int(sys.argv[1])
    is_pi = True if sys.argv[2] == 1 else False
    launch_camera_instances(camera_num, "text", is_pi)
