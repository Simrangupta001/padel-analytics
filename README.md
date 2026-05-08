# 🏓 Padel Analytics System

AI-powered computer vision system for analyzing padel matches using YOLO, OpenCV, and custom analytics modules.

The system detects and tracks players, ball movement, and match events, then generates structured insights such as shot classification, trajectory analysis, and performance analytics.

---

# 🚀 Features

## 🔍 Detection & Tracking

- Player detection using YOLO
- Ball tracking across frames
- Pose estimation using YOLO-Pose
- Racket interaction analysis

---

## 🎯 Shot Analysis

- Forehand detection
- Backhand detection
- Smash detection
- Serve detection
- Bounce detection

---

## 📊 Analytics System

- Shot classification engine
- Ball trajectory analysis
- Direction-based shot analysis
- Match timeline statistics

---

## 📈 Visualization

- Live video overlay analytics
- Shot distribution graphs
- Heatmap visualization
- Interactive HTML report

---

## 📦 Outputs Generated

- 🎥 Annotated match video
- 📁 Shot statistics CSV file
- 🌐 Interactive HTML dashboard

---

# 🧠 System Architecture

```text
Input Video
    ↓
YOLO Object Detection (Players + Ball + Racket)
    ↓
Tracking Module (Frame-by-frame association)
    ↓
Pose Estimation (YOLO-Pose)
    ↓
Shot Classification Engine
    ↓
Ball Tracking & Trajectory Analysis
    ↓
Analytics Engine (Stats + Metrics)
    ↓
Visualization Layer (Graphs + Overlay)
    ↓
Output Generation
   ├── Annotated Video
   ├── CSV Stats
   └── HTML Dashboard
```

---

# 📁 Project Structure

```text
padel-analytics/
│
├── models/
│   ├── yolov8m.pt
│   └── yolov8m-pose.pt
│
├── input/
│   └── input_video.mp4
│
├── output/
│   ├── final001_output.mp4
│   ├── shot_results001.csv
│   └── padel_report.html
│
├── utils/
│   ├── shot_classifier.py
│   ├── analytics.py
│   ├── visualization.py
│   ├── ball_tracker.py
│   └── helpers.py
│
├── main.py
├── bonus_dashboard.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Create Virtual Environment

### Mac / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 2️⃣ Install Dependencies

Create a file named:

```text
requirements.txt
```

Paste the following:

```txt
ultralytics
opencv-python
numpy
pandas
matplotlib
scipy
torch
torchvision
torchaudio
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Add YOLO Models

Place the following files inside:

```text
models/
```

Required model files:

```text
yolov8m.pt
yolov8m-pose.pt
```

---

## 4️⃣ Add Input Video

Place your video inside:

```text
input/input_video.mp4
```

---

# ▶️ How to Run

## Step 1 — Run Main Pipeline

```bash
python main.py
```

Generated outputs:

```text
🎥 output/final001_output.mp4
📁 output/shot_results001.csv
```

---

## Step 2 — Generate Dashboard Report

```bash
python bonus_dashboard.py
```

Generated output:

```text
🌐 output/padel_report.html
```

---

# 🌐 View Results

Open the following file in your browser:

```text
output/padel_report.html
```

The dashboard includes:

- Shot distribution graphs
- Timeline analysis
- Player performance statistics
- Bounce analysis
- Shot direction analysis
- Match analytics visualization

---

# 📊 Analytics Modules

## 🎯 Shot Classifier

Located in:

```text
utils/shot_classifier.py
```

Handles:

- Shot type classification
- Forehand / backhand detection
- Smash / serve recognition

---

## 🔁 Ball Tracker

Located in:

```text
utils/ball_tracker.py
```

Handles:

- Ball movement tracking
- Frame-by-frame trajectory analysis
- Bounce detection logic

---

## 📈 Analytics Engine

Located in:

```text
utils/analytics.py
```

Handles:

- Match statistics
- Shot frequency analysis
- Direction trends
- Performance metrics

---

## 🎨 Visualization Module

Located in:

```text
utils/visualization.py
```

Handles:

- Heatmaps
- Graph generation
- Video overlay dashboard
- Interactive visualization UI

---

# 💻 System Requirements

- Python 3.10+
- 8GB+ RAM recommended
- YOLO-compatible CPU/GPU
- macOS / Windows / Linux supported

---

# 🔮 Future Improvements

- Real-time match analytics
- AI coaching recommendations
- Player movement heatmaps
- Shot speed estimation
- Automatic score detection
- Advanced tactical analysis

---

# 👨‍💻 Author

**Simran Kumari Gupta**  
AI/ML & Computer Vision Enthusiast

