# gesture_yolo.py
import cv2
import numpy as np
import math
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        print("MediaPipe Zero-Gap Precision Core Active!")

    def process_frame(self, frame):
        h, w, c = frame.shape
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        vol_per = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Keypoints: 4 = Thumb Tip, 8 = Index Finger Tip
                thumb = hand_landmarks.landmark[4]
                index_finger = hand_landmarks.landmark[8]

                tx, ty = int(thumb.x * w), int(thumb.y * h)
                ix, iy = int(index_finger.x * w), int(index_finger.y * h)

                # Real-time physical distance calculation
                distance = math.hypot(ix - tx, iy - ty)

                # --- DEAD-ZONE LOGIC FOR PERFECT ZERO ---
                # Agar distance 26 pixels se kam ho, toh bina interpolation ke zero kar do
                if distance <= 26:
                    vol_per = 0
                else:
                    # Alignment calibration range tweaked to handle physical offsets
                    vol_per = np.interp(distance, [26, 160], [0, 100])
                    vol_per = int(np.clip(vol_per, 0, 100))

                # Visual overlay feedback layers
                cv2.circle(frame, (tx, ty), 10, (255, 0, 0), -1)   
                cv2.circle(frame, (ix, iy), 10, (0, 0, 255), -1)   
                cv2.line(frame, (tx, ty), (ix, iy), (0, 255, 0), 3) 

                cx, cy = (tx + ix) // 2, (ty + iy) // 2
                cv2.putText(frame, f"Gap: {vol_per}%", (cx + 15, cy), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                break

        return frame, vol_per

def load_yolo_model(path=None):
    return HandTracker()
