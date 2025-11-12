# Safety Object Detection (SSOD) Application

This is a Smart Object Detection application built with YOLOv8 to detect industrial safety equipment. The application can identify 7 classes of safety objects:
- OxygenTank
- NitrogenTank
- FirstAidBox
- FireAlarm
- SafetySwitchPanel
- EmergencyPhone
- FireExtinguisher

## Features
- Real-time object detection using YOLOv8
- Modern web interface built with Streamlit
- Automatic model updates via Falcon integration
- Docker support for easy deployment
- Health check endpoint for monitoring

## Prerequisites
- Python 3.7 or higher
- pip package manager

## Local Deployment

### Option 1: Direct Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py --server.port=8080 --server.address=0.0.0.0
```

### Option 2: Using the Deployment Script
```bash
# Make the script executable
chmod +x deploy.sh

# Run the deployment script
./deploy.sh
```

## Docker Deployment

### Build and Run Locally
```bash
# Build the Docker image
docker build -t ssod-detection-app .

# Run the container
docker run -p 8080:8080 ssod-detection-app
```

### Push to Container Registry
```bash
# Tag the image
docker tag ssod-detection-app your-registry/ssod-detection-app:latest

# Push to registry
docker push your-registry/ssod-detection-app:latest
```

## Cloud Deployment

### Heroku Deployment
1. Install Heroku CLI
2. Login to Heroku: `heroku login`
3. Create Heroku app: `heroku create your-app-name`
4. Set buildpack: `heroku buildpacks:set heroku/python`
5. Deploy: `git push heroku main`
6. Scale dyno: `heroku ps:scale web=1`

### AWS Deployment
1. Install AWS CLI and configure credentials
2. Create deployment package: `zip -r ssod-deployment.zip . -x "*.git*"`
3. Deploy to AWS Elastic Beanstalk or ECS

### Google Cloud Platform Deployment
1. Install Google Cloud SDK
2. Authenticate: `gcloud auth login`
3. Build and push to Container Registry
4. Deploy to Cloud Run or GKE

## Environment Variables
- `PORT`: Port number (default: 8080)
- `MODEL_PATH`: Path to the YOLO model file

## Health Check
The application includes a health check endpoint at `/healthz` for monitoring purposes.

## Accessing the Application
Once deployed, access the application at:
- Local: http://localhost:8080
- Docker: http://localhost:8080
- Cloud platforms: Provided URL after deployment

## Model Information
The application uses a YOLOv8 model trained on industrial safety equipment with the following performance metrics:
- Precision: 0.9076
- Recall: 0.6353
- mAP@0.5: 0.7229
- mAP@0.5:0.95: 0.5781

## Built by
Sagar | CodeAlchemy Hackathon 2025