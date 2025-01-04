import cv2
import mediapipe as mp
import pyautogui

# Initialize camera and MediaPipe face mesh detector
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

while True:
    # Capture and process camera frame
    _, frame = cam.read()
    frame = cv2.resize(frame, (640, 360))
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detect facial landmarks
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    
    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            if id == 1:
                # Convert eye position to screen coordinates
                screen_x = screen_w * landmark.x
                screen_x = screen_w * landmark.x
                screen_y = screen_h * landmark.y 
                pyautogui.moveTo(screen_x, screen_y)
                
                
        # Track left eye blink (landmarks 145, 159) for mouse click        
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
            
        # Detect blink (eye close) to trigger mouse click
        if (left[0].y - left[1].y) < 0.004:
            pyautogui.click()
            pyautogui.sleep(1) # Delay to prevent multiple clicks
            
    # Display the processed frame    
    cv2.imshow('Eye Controlled Mouse', frame)
    cv2.waitKey(1)
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# Clean up
cam.release()
cv2.destroyAllWindows()