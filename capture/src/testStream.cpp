#include <opencv2/opencv.hpp>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <vector>
#include <iostream>

int main() {
    // Initialize OpenCV video capture (0 for default camera)
    cv::VideoCapture cap(0);
    if (!cap.isOpened()) {
        std::cerr << "Error opening video capture" << std::endl;
        return -1;
    }

    // Create TCP socket
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) {
        std::cerr << "Socket creation failed" << std::endl;
        return -1;
    }

    // Connect to Node.js server
    sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(3000); // Node.js server port
    inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr);

    if (connect(sock, (sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        std::cerr << "Connection failed" << std::endl;
        return -1;
    }

    // Capture and send frames
    cv::Mat frame;
    std::vector<uchar> buffer;
    while (cap.read(frame)) {
        // Encode frame as JPEG
        cv::imencode(".jpg", frame, buffer);

        // Send frame size first
        uint32_t size = buffer.size();
        size = htonl(size); // Convert to network byte order
        send(sock, &size, sizeof(size), 0);

        // Send frame data
        send(sock, buffer.data(), buffer.size(), 0);

        // Display locally (optional)
        cv::imshow("Frame", frame);
        if (cv::waitKey(1) == 27) break; // Exit on ESC
    }

    // Cleanup
    close(sock);
    cap.release();
    cv::destroyAllWindows();
    return 0;
}