#include "human_detector.hpp"

eecs488::HumanDetector::HumanDetector()
{
    hog.setSVMDetector(cv::HOGDescriptor::getDefaultPeopleDetector());

    human_sizes.reserve(50);
}

eecs488::HumanDetector::~HumanDetector()
{
}

int eecs488::HumanDetector::detect_people(cv::Mat frame)
{
    std::vector<cv::Rect> found;
    
    hog.detectMultiScale(frame, found);

    return found.size();
}