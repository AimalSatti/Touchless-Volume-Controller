# Touchless OS Master System Controller

An advanced, real-time Human-Computer Interaction (HCI) software tool developed as part of the Software Engineering curriculum. This desktop automation pipeline enables users to dynamically adjust and manage their operating system's master volume using continuous hand gestures, entirely bypassing the need for physical input devices.

---

## 🚀 Key Features
* **Computer Vision Tracking:** Utilizes deep learning architectures via Google MediaPipe to track 21 hand skeletal landmarks under variable lighting in real-time.
* **Signal Smoothing Filter:** Implements a custom mathematical Exponential Moving Average (EMA) algorithm to completely stabilize input tracking and eliminate involuntary hand tremors.
* **Intelligent Dead-Zone Calibration:** Features a specialized cutoff threshold mapping to ensure a definitive 0% system mute, overcoming camera resolution noise.
* **Kernel-Level Interaction:** Leverages PyAutoGUI to directly inject virtual hardware media keys into the host operating system loop.

---

## 🛠️ System Architecture & Mechanics

The system operates on a dual-module decoupled framework separating core mathematical business logic from the visual frame acquisition pipeline:

1. **`gesture.py` (Core Logic Framework):** Manages the state variables, mathematical Euclidean distance calculations, low-pass EMA signal filtering ($\alpha = 0.28$), and virtual hardware hotkey injection.
2. **`test.py` (Execution Stream Engine):** Spins up the live video acquisition pipeline, handles color space conversions (BGR to RGB) required by the deep learning models, and overlays analytical telemetry data onto the GUI window.

### Mathematical Mapping Process
The direct operational distance between the user's thumb-tip (Landmark 4) and index-finger-tip (Landmark 8) is extracted using the Euclidean distance formula:

$$d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$

This pixel value is smoothed via the EMA filter:

$$S_t = \alpha \cdot Y_t + (1 - \alpha) \cdot S_{t-1}$$

The resulting filtered signal is scaled mapping a calibrated range ($26\text{px} - 230\text{px}$) to a relative master volume output ($0\% - 100\%$).

---

## 📦 Project Directory Structure

```text
├── gesture.py       # Structural backend containing filters, distance math, and automation
├── test.py          # Operational execution pipeline managing CV video stream loops
└── README.md        # Comprehensive technical documentation and user setup guide
