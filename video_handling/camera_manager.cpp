#include "camera_manager.hpp"

CameraManager::CameraManger()
: number_of_camera(1)
{
    this->cameras.reserve(1);
    
}

CameraManager::CameraManger(const int num_of_camera)
: number_of_camera(1)
{
    this->cameras.reserve(1);
}