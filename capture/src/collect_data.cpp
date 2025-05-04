#include <opencv2/opencv.hpp>
#include <iostream>
#include <chrono>
#include <ctime>
#include <csignal>

const int WIDTH = 1280;
const int HEIGHT = 720;
const int FPS = 30;
bool running = true;

void signalHandler(int signum) {
    running = false;
}

std::string get_output_filename() {
    auto now = std::chrono::system_clock::now();
    std::time_t now_time = std::chrono::system_clock::to_time_t(now);
    char buffer[80];
    std::strftime(buffer, sizeof(buffer), "video_%Y%m%d_%H%M%S.mp4", std::localtime(&now_time));
    return std::string(buffer);
}

int main() {
    signal(SIGINT, signalHandler);
    signal(SIGTERM, signalHandler);

    // Capture pipeline
    std::string capture_pipeline = 
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), width=" + std::to_string(WIDTH) + 
        ", height=" + std::to_string(HEIGHT) + 
        ", format=NV12, framerate=" + std::to_string(FPS) + "/1 ! "
        "nvvidconv flip-method=0 ! "
        "video/x-raw, format=BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=BGR ! "
        "appsink drop=true";

    cv::VideoCapture cap(capture_pipeline, cv::CAP_GSTREAMER);
    
    if (!cap.isOpened()) {
        std::cerr << "Cannot open camera" << std::endl;
        return -1;
    }

    std::string output_file = get_output_filename();
    
    // Encoding pipeline - modified to use NVMM memory
    std::string encode_pipeline = 
        "appsrc ! "
        "videoconvert ! "
        "video/x-raw, format=NV12 ! "
        "nvvidconv ! "
        "video/x-raw(memory:NVMM), format=NV12 ! "
        "nvv4l2h264enc insert-sps-pps=true insert-vui=true bitrate=8000000 ! "
        "h264parse ! "
        "qtmux ! "
        "filesink location=" + output_file;

    cv::VideoWriter out;
    out.open(encode_pipeline, cv::CAP_GSTREAMER, 0, FPS, cv::Size(WIDTH, HEIGHT), true);
    
    if (!out.isOpened()) {
        std::cerr << "Cannot create video writer" << std::endl;
        std::cerr << "Make sure you have the proper GStreamer plugins installed" << std::endl;
        return -1;
    }

    std::cout << "Recording started (720p H.264). Saving to " << output_file << std::endl;
    std::cout << "Press Ctrl+C to stop recording..." << std::endl;

    cv::Mat frame;
    int frame_count = 0;
    auto start_time = std::chrono::steady_clock::now();

    try {
        while (running) {
            if (!cap.read(frame)) {
                std::cerr << "Can't receive frame. Exiting..." << std::endl;
                break;
            }

            // Add timestamp
            auto now = std::chrono::system_clock::now();
            std::time_t now_time = std::chrono::system_clock::to_time_t(now);
            char time_str[100];
            std::strftime(time_str, sizeof(time_str), "%Y-%m-%d %H:%M:%S", std::localtime(&now_time));
            cv::putText(frame, time_str, cv::Point(10, 30), 
                       cv::FONT_HERSHEY_SIMPLEX, 1, cv::Scalar(0, 255, 0), 2);

            out.write(frame);
            frame_count++;

            if (frame_count % 30 == 0) {
                auto current_time = std::chrono::steady_clock::now();
                auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(current_time - start_time);
                double fps = frame_count / elapsed.count();
                std::cout << "Captured " << frame_count << " frames (" << fps << " fps)" << std::endl;
            }
        }
    } catch (...) {
        std::cerr << "Exception occurred" << std::endl;
    }

    cap.release();
    out.release();

    auto end_time = std::chrono::steady_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::seconds>(end_time - start_time);
    std::cout << "Recording saved to " << output_file << std::endl;
    std::cout << "Total frames: " << frame_count << std::endl;
    std::cout << "Duration: " << duration.count() << " seconds" << std::endl;

    return 0;
}
