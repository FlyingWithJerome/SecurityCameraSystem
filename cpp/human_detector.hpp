#include <opencv2/opencv.hpp>
#include <vector>

namespace eecs488
{
    class HumanDetector
    {
    public:
        HumanDetector();

        ~HumanDetector();

        int detect_people(cv::Mat frame);

    private:
        std::vector<float> human_sizes;

        cv::HOGDescriptor hog;
        
        bool is_approaching();
    };
}