# gesture.py
import cv2
import numpy as np
import pyautogui
from test import load_yolo_model

# PyAutoGUI performance tuning delays
pyautogui.PAUSE = 0.01

def main():
    tracker = load_yolo_model()
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not capture camera device pipeline.")
        return

    print("\n" + "="*50)
    print("SUCCESS: SYSTEM INJECTION MAP ACTIVE WITH ZERO-GAP FILTER!")
    print("="*50 + "\n")

    last_stable_vol = 50
    alpha = 0.28  # Filter scale matrix

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        processed_frame, vol_level = tracker.process_frame(frame)

        if vol_level is not None:
            # Special bypass check for absolute zero state handling
            if vol_level == 0:
                target_vol = 0
            else:
                smoothed = (alpha * vol_level) + ((1 - alpha) * last_stable_vol)
                target_vol = int(smoothed)

            # Rapid KeyPress Mapping Sequencer
            if target_vol > last_stable_vol + 2:
                steps = max(1, int((target_vol - last_stable_vol) / 2))
                for _ in range(steps):
                    pyautogui.press('volumeup')
                last_stable_vol = target_vol

            elif target_vol < last_stable_vol - 2:
                steps = max(1, int((last_stable_vol - target_vol) / 2))
                for _ in range(steps):
                    pyautogui.press('volumedown')
                last_stable_vol = target_vol
                
            # Master override case update logic
            if target_vol == 0 and last_stable_vol != 0:
                for _ in range(15):  # Secure drops directly down to absolute floor mute
                    pyautogui.press('volumedown')
                last_stable_vol = 0

            cv2.putText(processed_frame, f"STABLE VOL: {target_vol}%", (30, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
        else:
            cv2.putText(processed_frame, "Fingers Status: OUT OF FRAME", (30, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Direct System Master Control UI", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
