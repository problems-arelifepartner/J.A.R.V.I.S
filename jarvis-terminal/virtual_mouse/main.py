#!/usr/bin/env python3
"""Minimal, robust Virtual Mouse helper.

This script attempts to run a simple webcam display loop if OpenCV is
available. The full-featured gesture-controlled virtual mouse requires
opencv-python, mediapipe, and pyautogui; if those are missing this script
will print instructions and exit cleanly.
"""

import sys
import time


def main():
    try:
        import cv2
    except Exception:
        print("[virtual_mouse] OpenCV (cv2) not installed. Install: pip install opencv-python")
        return 1

    print("[virtual_mouse] OpenCV available. Opening webcam... (press 'q' to quit)")
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("[virtual_mouse] Could not open webcam (index 0).")
            return 1

        while True:
            ret, frame = cap.read()
            if not ret:
                print("[virtual_mouse] Failed to read frame from webcam")
                break
            cv2.imshow('Virtual Mouse - Press q to Quit', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # small sleep to avoid high CPU on some systems
            time.sleep(0.01)

        cap.release()
        cv2.destroyAllWindows()
        return 0
    except KeyboardInterrupt:
        print('\n[virtual_mouse] Interrupted by user; exiting.')
        try:
            cap.release()
        except Exception:
            pass
        try:
            cv2.destroyAllWindows()
        except Exception:
            pass
        return 0
    except Exception as e:
        print(f"[virtual_mouse] Error: {e}")
        return 1


if __name__ == "__main__":
    try:
        rc = main()
        sys.exit(rc if isinstance(rc, int) else 0)
    except Exception as e:
        # Provide a helpful message and propagate the exception for wrappers that expect it.
        print("Virtual Mouse failed to start:", e)
        raise
