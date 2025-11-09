# Deployment Instructions

## Prerequisites
- Python 3.7 or higher
- pip package manager

## Deployment Options

### Option 1: Direct Deployment

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   streamlit run app.py --server.port=8080 --server.address=0.0.0.0
   ```

### Option 2: Using the Deployment Script

1. Make the script executable (if not already):
   ```bash
   chmod +x start_app.sh
   ```

2. Run the deployment script:
   ```bash
   ./start_app.sh
   ```

### Option 3: Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t ssod-detection-app .
   ```

2. Run the container:
   ```bash
   docker run -p 8080:8080 ssod-detection-app
   ```

## Access the Application

Once deployed, access the application at:
- Local: http://localhost:8080
- Network: http://[your-ip]:8080

## Model Information

The application detects the following industrial safety objects:
- OxygenTank
- NitrogenTank
- FirstAidBox
- FireAlarm
- SafetySwitchPanel
- EmergencyPhone
- FireExtinguisher

Upload images containing these objects to see detections.
