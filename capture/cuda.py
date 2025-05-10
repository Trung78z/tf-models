import cv2
import numpy as np

# Check CUDA availability
if cv2.cuda.getCudaEnabledDeviceCount() == 0:
    print("CUDA not available - falling back to CPU")
    use_cuda = False
else:
    use_cuda = True
    print(f"CUDA is available with {cv2.cuda.getCudaEnabledDeviceCount()} device(s)")

# Initialize camera
cam = cv2.VideoCapture(0)
current_filter = "original"
filters = ["original", "gaussian", "median", "sobel", "laplacian", "canny"]

def apply_cuda_filter(gpu_frame, filter_name):
    """Apply CUDA-accelerated filter"""
    if filter_name == "original":
        return gpu_frame
    elif filter_name == "gaussian":
        return cv2.cuda_GaussianBlur(gpu_frame, (15, 15), 0)
    elif filter_name == "median":
        gray = cv2.cuda.cvtColor(gpu_frame, cv2.COLOR_BGR2GRAY)
        return cv2.cuda.medianBlur(gray, 15)
    elif filter_name == "sobel":
        gray = cv2.cuda.cvtColor(gpu_frame, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.cuda.Sobel(gray, cv2.CV_32F, 1, 0)
        sobely = cv2.cuda.Sobel(gray, cv2.CV_32F, 0, 1)
        abs_grad_x = cv2.cuda.abs(sobelx)
        abs_grad_y = cv2.cuda.abs(sobely)
        return cv2.cuda.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    elif filter_name == "laplacian":
        gray = cv2.cuda.cvtColor(gpu_frame, cv2.COLOR_BGR2GRAY)
        return cv2.cuda.Laplacian(gray, cv2.CV_32F)
    elif filter_name == "canny":
        gray = cv2.cuda.cvtColor(gpu_frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.cuda_GaussianBlur(gray, (5, 5), 0)
        canny = cv2.cuda.createCannyEdgeDetector(50, 150)
        return canny.detect(blurred)
    return gpu_frame

print("Available CUDA filters:", ", ".join(filters))
print("Press 1-6 to change filter, 'q' to quit")

gpu_frame = cv2.cuda_GpuMat()

while True:
    ret, frame = cam.read()
    if not ret:
        break
    
    if use_cuda:
        gpu_frame.upload(frame)
        filtered = apply_cuda_filter(gpu_frame, current_filter)
        result = filtered.download()
        
        # Convert single-channel results to 3-channel for display
        if len(result.shape) == 2:
            result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
    else:
        # Fallback to CPU implementation
        result = frame
    
    # Display filter name
    cv2.putText(result, f"Filter: {current_filter} {'(CUDA)' if use_cuda else '(CPU)'}", 
               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    cv2.imshow('CUDA Filter', result)
    
    # Keyboard controls
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif ord('1') <= key <= ord('6'):
        filter_index = key - ord('1')
        if filter_index < len(filters):
            current_filter = filters[filter_index]
            print(f"Switched to filter: {current_filter}")

cam.release()
cv2.destroyAllWindows()