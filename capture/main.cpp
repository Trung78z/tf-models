#include <opencv2/opencv.hpp>
#include <iostream>
using namespace cv;
int main()
{
    // Open the default camera
    VideoCapture cam(0);
    if (!cam.isOpened())
    {
        std::cout << "Error: Unable to access the camera!" << std::endl;
        return -1;
    }

    // Get the default frame width and height
    int frame_width = static_cast<int>(cam.get(CAP_PROP_FRAME_WIDTH));
    int frame_height = static_cast<int>(cam.get(CAP_PROP_FRAME_HEIGHT));

    // Define the codec and create VideoWriter object
    int fourcc = VideoWriter::fourcc('m', 'p', '4', 'v');
    VideoWriter out("output.mp4", fourcc, 20.0, Size(frame_width, frame_height));

    if (!out.isOpened())
    {
        std::cout << "Error: Could not open the output video file!" << std::endl;
        return -1;
    }

    while (true)
    {
        Mat frame;
        bool ret = cam.read(frame);
        if (!ret)
        {
            std::cout << "Error: Failed to capture image!" << std::endl;
            break;
        }

        // Write the frame to the output file
        out.write(frame);

        // Display the captured frame
        imshow("Camera", frame);

        // Press 'q' to exit the loop
        if (waitKey(1) == 'q')
        {
            break;
        }
    }

    // Release the capture and writer objects
    cam.release();
    out.release();
    destroyAllWindows();

    return 0;
}
