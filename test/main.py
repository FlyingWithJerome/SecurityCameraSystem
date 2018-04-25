'''
main.py

The entry point of the program
'''

import threading
import multiprocessing
import sys

# import gevent

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
    for num in range(0, camera_num, 1):
        if interface_opt == "text":
            job_query.append(multiprocessing.Process(target=_text_interface_wrapper, args=(num, is_pi)))
            # job_query.append(gevent.spawn(_text_interface_wrapper, num, is_pi))

    for job in job_query:
        job.start()

    # gevent.joinall(job_query)


if __name__ == "__main__":
    camera_num = int(sys.argv[1])
    is_pi = True if sys.argv[2] == "pi" else False

    launch_camera_instances(camera_num=camera_num, interface_opt="text", is_pi=is_pi)
