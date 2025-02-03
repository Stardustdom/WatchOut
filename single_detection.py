import cv2
import mediapipe as mp
import time
import threading
import winsound  # For beeping sound on Windows

# Initialize MediaPipe modules
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Video capture setup
cap = cv2.VideoCapture(1)  # Change to 3 if using an external camera
fourcc = cv2.VideoWriter_fourcc(*'XVID')
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# MediaPipe configurations
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Variables for recording
out = None
recording = False
start_time = None
beep_active = False  # To track if beeping is active
beep_thread = None  # To handle the beeping thread

# Function to play beep sound continuously
def beep_continuously():
    while beep_active:
        winsound.Beep(1000, 500)  # Beep at 1000 Hz for 500 ms
        time.sleep(0.5)  # Add a small delay between beeps

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect hands and pose
        hand_results = hands.process(frame_rgb)
        pose_results = pose.process(frame_rgb)

        human_detected = False

        # Draw hand landmarks
        if hand_results.multi_hand_landmarks:
            human_detected = True
            for hand_landmarks in hand_results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2))

        # Draw pose landmarks
        if pose_results.pose_landmarks:
            human_detected = True
            mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2))

        # Start recording and beeping if a human is detected
        if human_detected:
            if not recording:
                video_filename = f'output_{time.strftime("%Y%m%d_%H%M%S")}.avi'
                print(f"Human figure detected, starting recording to {video_filename}...")
                out = cv2.VideoWriter(video_filename, fourcc, 20.0, (frame_width, frame_height))
                recording = True
                start_time = time.time()

            # Start beeping if not already active
            if not beep_active:
                beep_active = True
                beep_thread = threading.Thread(target=beep_continuously)
                beep_thread.start()

            if out:
                out.write(frame)

        # Stop recording and beeping after 30 seconds of inactivity
        elif recording:
            elapsed_time = time.time() - start_time
            if elapsed_time < 30:
                if out:
                    out.write(frame)
            else:
                print(f"30 seconds elapsed, stopping recording...")
                recording = False
                beep_active = False  # Stop beeping
                if out:
                    out.release()
                    out = None

        # Display the output
        cv2.imshow("Human Figure Detection", frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # When everything is done, release the capture and writer objects
    if out:
        out.release()
    cap.release()
    cv2.destroyAllWindows()
    print("Resources released. Exiting program.")