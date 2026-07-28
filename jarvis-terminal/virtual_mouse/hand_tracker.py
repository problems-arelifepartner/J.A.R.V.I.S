import cv2
import mediapipe as mp
import math

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hand_landmarks(self, frame):
        # Convert BGR to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        lm_list = {}

        if results.multi_hand_landmarks:
            for hand_lms in results.multi_hand_landmarks:
                # Draw the skeleton lines over your hand on the screen
                self.mp_draw.draw_landmarks(frame, hand_lms, self.mp_hands.HAND_CONNECTIONS)

                # Extract landmark pixel positions
                for id, lm in enumerate(hand_lms.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list[id] = (cx, cy, lm.x, lm.y) # returns pixels & raw normalized scale

        return lm_list

    @staticmethod
    def get_distance(p1, p2):
        """Calculates Euclidean distance between two points."""
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])
