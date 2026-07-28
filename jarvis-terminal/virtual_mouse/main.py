import cv2
import os
from virtual_mouse import config as vm_config
from virtual_mouse.hand_tracker import HandTracker
from virtual_mouse.mouse_controller import MouseController

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, vm_config.CAM_WIDTH)
    cap.set(4, vm_config.CAM_HEIGHT)

    tracker = HandTracker()
    mouse = MouseController()

    print("Virtual Mouse Active. Press 'q' in the window to quit.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Flip frame so movement acts naturally like looking in a mirror
        frame = cv2.flip(frame, 1)
        landmarks = tracker.find_hand_landmarks(frame)

        if landmarks:
            # Gather Thumb(4), Index(8), and Middle(12) positions
            thumb = landmarks.get(4)
            index = landmarks.get(8)
            middle = landmarks.get(12)

            if index:
                # MOVEMENT: Drive the mouse with the Index Finger normalized position
                # index[2], index[3] are normalized coordinates
                mouse.move_cursor(index[2], index[3])

            if index and thumb:
                # CLICK & DRAG: Track Thumb and Index spacing
                click_dist = tracker.get_distance(index, thumb)
                if click_dist < vm_config.CLICK_THRESHOLD:
                    cv2.putText(frame, "Action: Drag/Click Active", (20, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    mouse.left_click_down()
                else:
                    mouse.left_click_up()

            if index and middle:
                # ZOOMING / SCROLLING: Track Index and Middle finger spacing
                zoom_dist = tracker.get_distance(index, middle)
                if zoom_dist > vm_config.ZOOM_OUT_THRESHOLD:
                    cv2.putText(frame, "Action: Scroll/Zoom Out", (20, 90), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    mouse.scroll_action("down")
                elif zoom_dist < vm_config.ZOOM_IN_THRESHOLD and (not thumb or tracker.get_distance(index, thumb) > vm_config.CLICK_THRESHOLD):
                    cv2.putText(frame, "Action: Scroll/Zoom In", (20, 90), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    mouse.scroll_action("up")

        # Show webcam window stream
        cv2.imshow("AI Hand-Mouse Terminal Visualizer", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
