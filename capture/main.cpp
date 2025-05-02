#include <opencv2/opencv.hpp>

#include <iostream>

using namespace cv;
using namespace std;

int main()
{
    VideoCapture cam(0);
    if (!cam.isOpened())
    {
        cerr << "Camera error!" << endl;
        return -1;
    }

    int width = static_cast<int>(cam.get(CAP_PROP_FRAME_WIDTH));
    int height = static_cast<int>(cam.get(CAP_PROP_FRAME_HEIGHT));

    int fourcc = VideoWriter::fourcc('M', 'J', 'P', 'G');
    VideoWriter out("output.avi", fourcc, 20.0, Size(width, height));

    if (!out.isOpened())
    {
        cerr << "Failed to create video writer!" << endl;
        return -1;
    }

    cout << "Recording started (press 'q' to stop)..." << endl;

    Mat frame, processed;
    while (true)
    {
        cam >> frame;
        if (frame.empty())
            break;

        // CPU processing (example: convert to grayscale)
        cvtColor(frame, processed, COLOR_BGR2GRAY);
        cvtColor(processed, frame, COLOR_GRAY2BGR);

        out.write(frame);
        imshow("Live", frame);

        if (waitKey(1) == 'q')
            break;
    }

    cam.release();
    out.release();
    destroyAllWindows();
    return 0;
}