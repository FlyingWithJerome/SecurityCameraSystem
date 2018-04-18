#include <opencv2/opencv.hpp>
#include <vector>

namespace eecs488
{
    #ifndef CAMERA_MANAGER_
    #define CAMERA_MANAGER_

    class CameraManager
    {
    public:
        CameraManager();

        CameraManager(const int num_of_camera);

        ~CameraManager();

        cv::Mat get_frames(const int camera_num);

    private:
        std::vector<cv::VideoCapture*> cameras;

        int number_of_camera;
        
        void register_cameras(const int num_of_camera);
    };
    #endif
}
