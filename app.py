# Import necessary libraries
import cv2
import mediapipe as mp
import pyautogui

# Initialize camera, face mesh detection, and screen dimensions
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

# Start the loop to capture frames from the camera
while True:
    # Read the camera frame and flip horizontally
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB and detect landmarks on the face
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks

    # Draw landmarks on the face
    frame_h, frame_w, _ = frame.shape
    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))

            # Move the mouse cursor based on the position of the landmark
            if id == 1:
                screen_x = 1.25*screen_w * landmark.x
                screen_y = 1.25*screen_h * landmark.y
                pyautogui.moveTo(screen_x, screen_y)

        # Detect the left eye and draw landmarks on it
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        
        # Click the mouse if the left eye is closed
        if (left[0].y - left[1].y) < 0.007:
            print("click>>")
            pyautogui.click()
            pyautogui.sleep(1)

    # Display the frame and wait for the user to press a key
    cv2.imshow('Eye Controlled Mouse', frame)
    key = cv2.waitKey(10)
    if key == 27:  # Exit if the user presses the Esc key
        break

# Release the camera and destroy all windows
cam.release()
cv2.destroyAllWindows()
