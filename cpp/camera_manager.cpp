#include "camera_manager.hpp"

#include <iostream>
eecs488::CameraManager::CameraManager()
: number_of_camera(1)
{
    cv::VideoCapture* camera = new cv::VideoCapture(0);

    cameras.push_back(camera);
    
}

eecs488::CameraManager::CameraManager(const int num_of_camera)
: number_of_camera(num_of_camera)
{
    for(int camera_index = 0; camera_index < number_of_camera; camera_index++)
    {
        cv::VideoCapture* camera = new cv::VideoCapture(camera_index);
    
        cameras.push_back(camera);
    }
}

cv::Mat eecs488::CameraManager::get_frames(const int camera_num)
{
    cv::Mat image;

    if(cameras[camera_num] -> isOpened())
    {
        cameras[camera_num] -> read(image);
    }

    return image;
}


eecs488::CameraManager::~CameraManager()
{
    for(auto cam : cameras)
    {
        delete cam;
    }
}