import cv2
import threading

# Global variables
cap = None
camera_running = False

def start_camera():
    global cap, camera_running
    if camera_running:
        return  # If already running, don't start again
    
    cap = cv2.VideoCapture(0)  # Open camera
    camera_running = True

    def capture():
        while camera_running:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Emotion Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
                stop_camera()

    thread = threading.Thread(target=capture)
    thread.start()

def stop_camera():
    global cap, camera_running
    camera_running = False
    if cap:
        cap.release()  # Release the camera
        cap = None
    cv2.destroyAllWindows()  # Close the window