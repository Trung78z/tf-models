#include <opencv2/opencv.hpp>
#include <queue>
#include <thread>
#include <mutex>
#include <atomic>
#include <condition_variable>

using namespace cv;
using namespace std;

// Shared data structure
struct ThreadData {
    queue<Mat> frame_queue;
    mutex queue_mutex;
    condition_variable cond_var;
    atomic<bool> is_running{true};
    atomic<int> fps{0};
};

// Thread 1: Capture frames from camera
void capture_thread(VideoCapture& cap, ThreadData& data) {
    Mat frame;
    int frame_count = 0;
    auto start_time = chrono::steady_clock::now();
    
    while (data.is_running) {
        cap >> frame;
        if (!frame.empty()) {
            unique_lock<mutex> lock(data.queue_mutex);
            if (data.frame_queue.size() < 5) { // Limit queue size
                data.frame_queue.push(frame.clone());
                data.cond_var.notify_one();
            }
            
            // Calculate FPS
            frame_count++;
            auto current_time = chrono::steady_clock::now();
            auto elapsed = chrono::duration_cast<chrono::seconds>(current_time - start_time).count();
            if (elapsed >= 1) {
                data.fps = frame_count / elapsed;
                frame_count = 0;
                start_time = current_time;
            }
        }
    }
}

// Thread 2: Process frames
void process_thread(ThreadData& data) {
    while (data.is_running) {
        Mat frame;
        {
            unique_lock<mutex> lock(data.queue_mutex);
            data.cond_var.wait(lock, [&]{ 
                return !data.frame_queue.empty() || !data.is_running; 
            });
            
            if (!data.is_running) break;
            
            frame = data.frame_queue.front();
            data.frame_queue.pop();
        }
        
        // Your image processing here
        // Example: convert to grayscale
        cvtColor(frame, frame, COLOR_BGR2GRAY);
    }
}

// Thread 3: Display and save
void display_thread(ThreadData& data, const string& output_file) {
    VideoWriter writer;
    int fourcc = VideoWriter::fourcc('M','J','P','G');
    Size frame_size(640, 480);
    
    if (!output_file.empty()) {
        writer.open(output_file, fourcc, 30, frame_size);
    }
    
    while (data.is_running) {
        Mat frame;
        {
            unique_lock<mutex> lock(data.queue_mutex);
            if (!data.frame_queue.empty()) {
                frame = data.frame_queue.front();
            }
        }
        
        if (!frame.empty()) {
            // Display frame
            imshow("Processed Video", frame);
            
            // Save frame if writer is opened
            if (writer.isOpened()) {
                writer.write(frame);
            }
            
            // Exit on ESC
            if (waitKey(1) == 27) {
                data.is_running = false;
                data.cond_var.notify_all(); // Wake up all threads
                break;
            }
            
            // Display FPS
            string fps_str = "FPS: " + to_string(data.fps.load());
            putText(frame, fps_str, Point(10, 30), FONT_HERSHEY_SIMPLEX, 1, Scalar(0, 255, 0), 2);
        }
    }
    
    if (writer.isOpened()) {
        writer.release();
    }
}

int main() {
    // Initialize camera
    VideoCapture cap(0);
    if (!cap.isOpened()) {
        cerr << "Error: Could not open camera" << endl;
        return -1;
    }
    
    // Set camera parameters
    cap.set(CAP_PROP_FRAME_WIDTH, 640);
    cap.set(CAP_PROP_FRAME_HEIGHT, 480);
    cap.set(CAP_PROP_FOURCC, VideoWriter::fourcc('M','J','P','G'));
    cap.set(CAP_PROP_FPS, 30);

    // Shared data
    ThreadData data;
    string output_file = "output.avi";

    // Create threads
    thread t1(capture_thread, ref(cap), ref(data));
    thread t2(process_thread, ref(data));
    thread t3(display_thread, ref(data), output_file);

    // Wait for threads to finish
    t1.join();
    t2.join();
    t3.join();

    // Cleanup
    cap.release();
    destroyAllWindows();
    
    cout << "Video processing completed" << endl;
    return 0;
}