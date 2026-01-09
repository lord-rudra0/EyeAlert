# 👁️ EyeAlert: Your Vigilant Co-Pilot

> **Stay Safe. Stay Alert. Arrive Alive.**

Driving is demanding. We all have moments where our focus drifts, we get distracted, or our eyelids start to feel heavy. **EyeAlert** is designed to be your silent guardian—a smart Driver Monitoring System (DMS) that watches out for you so you can focus on the road.

---

## ✨ What Does It Do?

EyeAlert uses your webcam and advanced AI to monitor your attentiveness in real-time. It's designed to be **helpful, not annoying**.

*   **😴 Sleep Detection**: Instantly detects if you are dozing off (head dropping) or if your eyes close for too long.
*   **🕶️ Smart Sunglasses Mode**: Wearing shades? No problem! The system automatically detects sunglasses and switches to tracking your head movements instead of your eyes, so your score remains accurate.
*   **😷 Mask Friendly**: Optimized to work even if you are wearing a face mask.
*   **🛣️ Mirror-Check Friendly**: We know good drivers check their mirrors. EyeAlert allows you to look to the side for a few seconds without marking you as "distracted".
*   **📱 Distraction Warnings**: If you look away from the road (e.g., at a phone) for more than **3 seconds**, it will flash a warning to **"FOCUS ON ROAD!"**.

## 🚦 How It Works

The system calculates a **Reliability Score (0-100%)** that represents your focus level.

*   🟢 **Green (80-100%)**: You are driving safe!
*   🟡 **Yellow (50-80%)**: Your attention is degrading. Take a deep breath.
*   🔴 **Red (< 50%)**: **DANGER!** You are likely sleeping or severely distracted. Pull over!

## 🚀 Getting Started

### Prerequisites
You need a computer with **Python 3.10+** and a **Webcam**.

### Installation
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/EyeAlert.git
    cd EyeAlert
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Usage
Simply run the main script:
```bash
python main.py
```
A window will open showing your video feed and your safety status. Just drive naturally!

## ⚙️ Customization
Want to tweak the sensitivity? Check out `config.py`:
*   `DISTRACTION_TIMEOUT`: How many seconds before the "Focus" alert triggers (Default: 3s).
*   `DECAY_RATE_POSE`: How fast the score drops when looking away.

---
*Built with ❤️ using OpenCV and MediaPipe.*
