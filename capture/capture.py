import cv2
import numpy as np
# Initialize camera
cam = cv2.VideoCapture(0)

# Get frame dimensions
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Filter selection (start with original)
current_filter = "original"
filters = ["original", "gaussian", "median", "bilateral", "edges", "grayscale", "sepia", "sketch"]

def apply_filter(frame, filter_name):
    """Apply selected filter to the frame"""
    if filter_name == "original":
        return frame
    elif filter_name == "gaussian":
        return cv2.GaussianBlur(frame, (15, 15), 0)
    elif filter_name == "median":
        return cv2.medianBlur(frame, 15)
    elif filter_name == "bilateral":
        return cv2.bilateralFilter(frame, 15, 75, 75)
    elif filter_name == "edges":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    elif filter_name == "grayscale":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    elif filter_name == "sepia":
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        return cv2.transform(frame, kernel)
    elif filter_name == "sketch":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        inverted = cv2.bitwise_not(gray)
        blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
        inverted_blurred = cv2.bitwise_not(blurred)
        sketch = cv2.divide(gray, inverted_blurred, scale=256.0)
        return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)
    return frame

print("Available filters:", ", ".join(filters))
print("Press 1-8 to change filter, 'q' to quit")

while True:
    ret, frame = cam.read()
    if not ret:
        break
    
    # Apply selected filter
    filtered_frame = apply_filter(frame, current_filter)
    
    # Display filter name on frame
    cv2.putText(filtered_frame, f"Filter: {current_filter}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow('Camera Filter', filtered_frame)
    
    # Keyboard controls
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif ord('1') <= key <= ord('8'):
        filter_index = key - ord('1')
        if filter_index < len(filters):
            current_filter = filters[filter_index]
            print(f"Switched to filter: {current_filter}")

cam.release()
cv2.destroyAllWindows()