import cv2
import threading
import time
from queue import Queue

# Camera settings
camera_index = 0
output_filename = 'output.avi'
fps = 30.0
frame_width = 640
frame_height = 480

# Open camera
cap = cv2.VideoCapture(camera_index)
if not cap.isOpened():
    print(f"Error: Could not open camera {camera_index}")
    exit()

# Camera warm-up
print("Warming up camera...")
for _ in range(10):
    ret, _ = cap.read()
    if not ret:
        print("Error: Camera warm-up failed")
        cap.release()
        exit()
    time.sleep(0.1)

# Set camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
cap.set(cv2.CAP_PROP_FPS, fps)

# Get actual resolution
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
actual_fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Recording at {frame_width}x{frame_height}, {actual_fps or fps:.2f} fps")

# Initialize VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height))
if not out.isOpened():
    print("Error: Could not initialize VideoWriter")
    cap.release()
    exit()

# Create display window
cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)

# Thread control
stop_thread = False
frame_count = 0
frame_queue = Queue(maxsize=10)  # Buffer for frames

# Frame writing thread
def write_frames():
    global frame_count
    write_start_time = time.time()
    while not stop_thread:
        try:
            frame = frame_queue.get(timeout=1.0)  # Wait for frame
            out.write(frame)
            frame_count += 1
            print(f"Frames captured: {frame_count}", end='\r')
        except Queue.Empty:
            if stop_thread:
                break
    write_end_time = time.time()
    write_duration = write_end_time - write_start_time
    print(f"\nTime taken for write_frames: {write_duration:.2f} seconds")

# Start thread
write_thread = threading.Thread(target=write_frames)
write_thread.start()

# Main loop
start_time = time.time()
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to read frame")
        stop_thread = True
        break
    frame = cv2.resize(frame, (frame_width, frame_height))
    if not frame_queue.full():
        frame_queue.put(frame)
    try:
        cv2.imshow('Frame', frame)
    except Exception as e:
        print(f"Error displaying frame: {e}")
        stop_thread = True
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        stop_thread = True
        break

# Record end time
end_time = time.time()
total_duration = end_time - start_time

# Cleanup
write_thread.join()
cap.release()
out.release()
cv2.destroyAllWindows()

# Print results
print(f"\nVideo saved as {output_filename} with {frame_count} frames")
print(f"Total time taken to save video: {total_duration:.2f} seconds")