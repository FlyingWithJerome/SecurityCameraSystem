'''
main.py

main entry of the project
'''
import atexit
import time
import multiprocessing
import threading

import cv2
import module_wrappers
import face_detection


_CAMERAS = []


def _camera_exit_hook():
    for camera_index in range(len(_CAMERAS)):
        _CAMERAS[camera_index].release()

atexit.register(_camera_exit_hook)
atexit.register(cv2.destroyAllWindows)

def _register_camera(serial_num):
    cap_base = cv2.VideoCapture(serial_num)
    _CAMERAS.append(cap_base)

    return cap_base

def get_frames(num_of_cameras=0, queues=[]):
    '''
    main process, which get frames from
    all cameras
    '''
    assert num_of_cameras == len(queues), "need to have more/less queues"
    cv2.namedWindow("image")
    for i in range(num_of_cameras):
        _register_camera(i)

    while(True):
        for camera, queue in zip(_CAMERAS, queues):
            ret, frame = camera.read()
            cv2.imshow("image", frame)
            cv2.waitKey(1)
            if ret: queue.put(frame)
        # time.sleep(0.2)


def main_runner():
    '''
    the entrance of the program
    '''
    smart_manager = multiprocessing.Manager()
    capture_to_detector_queue   = smart_manager.Queue()
    detector_to_output_queue    = smart_manager.Queue()

    # detector_in_out = multiprocessing.Process(target=module_wrappers.detector_wrapper, args=(capture_to_detector_queue, detector_to_output_queue))
    # frame_out = multiprocessing.Process(target=module_wrappers.video_export_wrapper,  args=(detector_to_output_queue,))

    detector_in_out = threading.Thread(target=module_wrappers.detector_wrapper, args=(capture_to_detector_queue, detector_to_output_queue))
    frame_out = threading.Thread(target=module_wrappers.video_export_wrapper,  args=(detector_to_output_queue,))

    try:
        detector_in_out.start()
        frame_out.start()

        get_frames(num_of_cameras=1, queues=[capture_to_detector_queue,])

        detector_in_out.join()
        frame_out.join()

    except KeyboardInterrupt:
        exit(0)  

def main():
    main_runner()


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    main()