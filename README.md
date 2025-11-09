# SSOD Detection App (YOLOv8 + Falcon)

## Overview
This application uses YOLOv8 for industrial safety object detection and integrates with Falcon for automatic model updates. The app allows users to upload images and detect 7 specific industrial safety objects:
- OxygenTank
- NitrogenTank
- FirstAidBox
- FireAlarm
- SafetySwitchPanel
- EmergencyPhone
- FireExtinguisher

## Features
- Real-time object detection using YOLOv8
- Automatic model updates via Falcon integration
- Cross-platform compatibility
- Streamlit-based web interface
- Docker support for easy deployment

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ssod-detection-app
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```
streamlit run app.py --server.port=8080 --server.address=0.0.0.0
```

The app will be available at http://localhost:8080

## Deployment

### Option 1: Direct Deployment
```
python3 -m pip install -r requirements.txt
streamlit run app.py --server.port=8080 --server.address=0.0.0.0
```

### Option 2: Using the Deployment Script
```
chmod +x start_app.sh
./start_app.sh
```

### Option 3: Docker Deployment
```
docker build -t ssod-detection-app .
docker run -p 8080:8080 ssod-detection-app
```

## Directory Structure
```
ssod_detection_app/
├── app.py
├── requirements.txt
├── Dockerfile
├── start_app.sh
├── runs/
│   └── detect/exp_m4_train1/weights/best.pt
├── configs/
│   └── data.yaml
└── utils/
    └── falcon_update.py
```

## Model Performance
- Precision: 0.9076
- Recall: 0.6353
- mAP@0.5: 0.7229
- mAP@0.5:0.95: 0.5781

Built by Sagar | CodeAlchemy Hackathon 2025
