// #include <boost/thread/thread.hpp>
// #include <boost/interprocess/ipc/message_queue.hpp>

#include "camera_manager.hpp"
#include "human_detector.hpp"

#include <unistd.h>

// using namespace boost::interprocess;

// void video_manager_wrapper(eecs488::CameraManager& manager, message_queue& threadwise_queue)
// {
//     for(;;)
//     {
//         cv::Mat frame = manager.get_frames(0);

//         threadwise_queue.push(frame);
//     }
// }

// void detector_wrapper(eecs488::HumanDetector& detector, message_queue& threadwise_queue)
// {
//     cv::namedWindow("edges", cv::WINDOW_AUTOSIZE);

//     for(;;)
//     {
//         cv::Mat frame;
        
//         threadwise_queue.pop(frame);

//         int people = detector.detect_people(frame);

//         cv::imshow("edges", frame);

//         if(cv::waitKey(30) >= 0) break;
//     }
// }

int main()
{
    eecs488::CameraManager manager;

    eecs488::HumanDetector detector;

    pid_t pid = fork();

    if(pid == 0)
    {
        for(;;)
        {
            cv::Mat frame = manager.get_frames(0);

            cv::imshow("edges", frame);

            if(cv::waitKey(1) >= 0) break;
        }

    }
    else
    {
        wait(NULL);
    }

    // message_queue mq(create_only, "queue", 100, sizeof(cv::Mat));


    
    // for(;;)
    // {
    //     cv::Mat frame = manager.get_frames(0);

    //     int people = detector.detect_people(frame);

    //     cv::imshow("edges", frame);

    //     if(cv::waitKey(1) >= 0) break;
    // }

    return 0;
}