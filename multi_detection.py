import cv2
import time
import winsound  # For generating beep sound on Windows
import threading  # To handle the beep sound in a separate thread

# Load the pre-trained Haar Cascade for full body, upper body, and lower body detection
full_body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
upper_body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')
lower_body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_lowerbody.xml')

# Start video capture from the camera
cap = cv2.VideoCapture(1)  # Change to 0 if using the default camera

# Use the MP4V codec (which is compatible with .mp4 format)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))


# Function to detect human figures (full body, upper body, and lower body) in the frame
def detect_human_figures(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect full bodies
    full_bodies = full_body_cascade.detectMultiScale(
        gray,
        scaleFactor=1.05, 
        minNeighbors=5,
        minSize=(80, 80),
        maxSize=(500, 500)
    )
    
    # Detect upper bodies
    upper_bodies = upper_body_cascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=5,
        minSize=(60, 60),
        maxSize=(400, 400)
    )
    
    # Detect lower bodies
    lower_bodies = lower_body_cascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=5,
        minSize=(60, 60),
        maxSize=(400, 400)
    )
    
    # Combine the detections
    return full_bodies, upper_bodies, lower_bodies

# Function to beep for 30 seconds
def beep_for_30_seconds():
    end_time = time.time() + 30  # Set the end time for 30 seconds
    while time.time() < end_time:
        winsound.Beep(1000, 500)  # Beep at 1000 Hz for 500 ms

# Initialize variables for video recording
out = None
recording = False
start_time = None  # To track the recording duration

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Detect human figures in the frame
    full_bodies, upper_bodies, lower_bodies = detect_human_figures(frame)
    
    # Draw rectangles around detected full bodies
    for (x, y, w, h) in full_bodies:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Green for full body
    
    # Draw rectangles around detected upper bodies
    for (x, y, w, h) in upper_bodies:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)  # Blue for upper body
    
    # Draw rectangles around detected lower bodies
    for (x, y, w, h) in lower_bodies:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)  # Red for lower body

    # Check if there are multiple human figures
    if len(full_bodies) > 1 or len(upper_bodies) > 1 or len(lower_bodies) > 1:
        if not recording:
            # Generate a new file name based on the current time
            video_filename = f'output_{time.strftime("%Y%m%d_%H%M%S")}.avi'
            print(f"Multiple human figures detected, starting recording to {video_filename}...")
            out = cv2.VideoWriter(video_filename, fourcc, 20.0, (frame_width, frame_height))
            recording = True
            start_time = time.time()  # Start the 30-second timer
            
            # Start the beep sound in a separate thread
            threading.Thread(target=beep_for_30_seconds).start()

        out.write(frame)  # Continue recording while multiple figures are detected

    elif recording:
        # Continue recording
        elapsed_time = time.time() - start_time
        if elapsed_time < 30:
            out.write(frame)  # Continue writing even if figures drop below threshold
        else:
            # Stop recording after 30 seconds
            print(f"30 seconds elapsed, stopping recording...")
            recording = False
            if out:
                out.release()
    
    # Display the resulting frame
    cv2.imshow('Human Figure Detection', frame)
    
    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture and writer objects
cap.release()

if out:
    out.release()

cv2.destroyAllWindows()