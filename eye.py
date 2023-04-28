import cv2
import mediapipe as mp
import pyautogui

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()
while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
#    print(landmark_points)

    frame_h, frame_w, _ = frame.shape
    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))

            #control mouse according to screen ratio
            if id == 1:
                screen_x = 1.25*screen_w * landmark.x
                screen_y = 1.25*screen_h * landmark.y
                pyautogui.moveTo(screen_x, screen_y)

        #handle click
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        
        #measure value for operation click
        #print(left[0].y - left[1].y)
        if (left[0].y - left[1].y) < 0.007:
            print("click>>")
            pyautogui.click()
            pyautogui.sleep(1)
    cv2.imshow('Eye Controlled Mouse', frame)
    key = cv2.waitKey(10)
    if key == 27:
        break
cam.release()
cv2.destroyAllWindows()