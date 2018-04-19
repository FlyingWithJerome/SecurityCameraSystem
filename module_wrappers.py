'''
module_wrappers.py

This module contains the wrappers for all the modules,
for multiprocessing jobs
'''

import cv2

# from video_handling import video_capture
import video_output

import face_detection

def video_export_wrapper(queue):
    
    video_exporter = video_output.VideoExporter(queue)
    video_exporter.start()

def detector_wrapper(queue_in, queue_out):
    detector = face_detection.Detector(queue_in, queue_out)
    detector.start()

# def video_capture_wrapper(queue):

#     camera_handler = video_capture.CameraHandler(queue)
#     camera_handler.start()

    