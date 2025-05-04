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



// #include <opencv2/opencv.hpp>
// #include <opencv2/cudaimgproc.hpp>
// #include <iostream>
// #include <chrono>
// #include <iomanip>
// #include <ctime>

// using namespace cv;
// using namespace std;

// string getCurrentLocalTime() {
//     auto now = chrono::system_clock::now();
//     time_t now_time = chrono::system_clock::to_time_t(now);
//     tm local_time = *localtime(&now_time);
    
//     stringstream ss;
//     ss << put_time(&local_time, "%Y-%m-%d %H:%M:%S");
//     return ss.str();
// }

// int main()
// {
//     // Check CUDA availability
//     if (!cuda::getCudaEnabledDeviceCount()) {
//         cerr << "CUDA not available!" << endl;
//         return -1;
//     }

//     VideoCapture cam(0);
//     if (!cam.isOpened()) {
//         cerr << "Camera error!" << endl;
//         return -1;
//     }

//     int width = cam.get(CAP_PROP_FRAME_WIDTH);
//     int height = cam.get(CAP_PROP_FRAME_HEIGHT);

//     // Try different codecs for VideoWriter
//     VideoWriter out;
//     vector<pair<string, int>> codecs = {
//         {"MJPG", VideoWriter::fourcc('M','J','P','G')},
//         {"X264", VideoWriter::fourcc('X','2','6','4')},
//         {"AVC1", VideoWriter::fourcc('a','v','c','1')}
//     };

//     bool writer_opened = false;
//     for (const auto& codec : codecs) {
//         out.open("output.avi", codec.second, 20, Size(width, height));
//         if (out.isOpened()) {
//             cout << "Using codec: " << codec.first << endl;
//             writer_opened = true;
//             break;
//         }
//     }

//     if (!writer_opened) {
//         cerr << "Failed to create video writer!" << endl;
//         return -1;
//     }

//     cout << "Recording started (press 'q' to stop)..." << endl;

//     Mat frame;
//     cuda::GpuMat gpu_frame, gpu_processed;
    
//     while (true) {
//         cam >> frame;
//         if (frame.empty()) break;

//         // Upload frame to GPU
//         gpu_frame.upload(frame);
        
//         // Download processed frame
//         gpu_frame.download(frame);

//         // Add timestamp (CPU operation)
//         string timeStr = getCurrentLocalTime();
//         putText(frame, timeStr, Point(10, 30), FONT_HERSHEY_SIMPLEX, 0.8, Scalar(0, 255, 0), 2);

//         out.write(frame);
//         imshow("Live", frame);

//         if (waitKey(1) == 'q') break;
//     }

//     cam.release();
//     out.release();
//     destroyAllWindows();
//     return 0;
// }






// #include <opencv2/opencv.hpp>
// #include <opencv2/cudaimgproc.hpp>
// #include <iostream>
// #include <chrono>
// #include <iomanip>
// #include <ctime>

// using namespace cv;
// using namespace std;

// string getCurrentLocalTime() {
//     auto now = chrono::system_clock::now();
//     time_t now_time = chrono::system_clock::to_time_t(now);
//     tm local_time = *localtime(&now_time);
    
//     stringstream ss;
//     ss << put_time(&local_time, "%Y-%m-%d %H:%M:%S");
//     return ss.str();
// }

// int main()
// {
//     // Check CUDA availability
//     if (!cuda::getCudaEnabledDeviceCount()) {
//         cerr << "CUDA not available!" << endl;
//         return -1;
//     }

//     VideoCapture cam(0);
//     if (!cam.isOpened()) {
//         cerr << "Camera error!" << endl;
//         return -1;
//     }

//     // Set camera to 30 FPS if supported
//     cam.set(CAP_PROP_FPS, 30);
//     double actual_fps = cam.get(CAP_PROP_FPS);
//     cout << "Camera FPS: " << actual_fps << endl;

//     int width = cam.get(CAP_PROP_FRAME_WIDTH);
//     int height = cam.get(CAP_PROP_FRAME_HEIGHT);

//     // VideoWriter at 30 FPS
//     VideoWriter out;
//     vector<pair<string, int>> codecs = {
//         {"MJPG", VideoWriter::fourcc('M','J','P','G')},
//         {"X264", VideoWriter::fourcc('X','2','6','4')},
//         {"AVC1", VideoWriter::fourcc('a','v','c','1')},
//         {"H264", VideoWriter::fourcc('H','2','6','4')}
//     };

//     bool writer_opened = false;
//     for (const auto& codec : codecs) {
//         out.open("output.avi", codec.second, 30, Size(width, height));
//         if (out.isOpened()) {
//             cout << "Using codec: " << codec.first << endl;
//             writer_opened = true;
//             break;
//         }
//     }

//     if (!writer_opened) {
//         cerr << "Failed to create video writer with any codec!" << endl;
//         return -1;
//     }

//     cout << "Recording started at 30 FPS (press 'q' to stop)..." << endl;

//     Mat frame;
//     cuda::GpuMat gpu_frame, gpu_processed;
//     TickMeter timer;
//     int frame_count = 0;
    
//     while (true) {
//         timer.start();
        
//         cam >> frame;
//         if (frame.empty()) break;

//         // Upload frame to GPU
//         gpu_frame.upload(frame);

//         // CUDA processing pipeline
//         cuda::cvtColor(gpu_frame, gpu_processed, COLOR_BGR2GRAY);
//         cuda::cvtColor(gpu_processed, gpu_frame, COLOR_GRAY2BGR);
        
//         // Download processed frame
//         gpu_frame.download(frame);

//         // Add timestamp
//         string timeStr = getCurrentLocalTime();
//         putText(frame, timeStr, Point(10, 30), FONT_HERSHEY_SIMPLEX, 0.8, Scalar(0, 255, 0), 2);
        
//         // Performance metrics
//         frame_count++;
//         timer.stop();
//         double current_fps = 1.0 / (timer.getTimeSec() / frame_count);
//         string fpsStr = "FPS: " + to_string((int)round(current_fps));
//         putText(frame, fpsStr, Point(10, 70), FONT_HERSHEY_SIMPLEX, 0.8, Scalar(0, 255, 255), 2);

//         out.write(frame);
//         imshow("Live", frame);

//         if (waitKey(1) == 'q') break;
//     }

//     // Release resources
//     cam.release();
//     out.release();
//     destroyAllWindows();
    
//     cout << "Average FPS: " << frame_count / timer.getTimeSec() << endl;
//     return 0;
// }