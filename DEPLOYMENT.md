# SSOD Detection App Deployment Guide

This guide provides instructions for deploying the Safety Object Detection (SSOD) application to various platforms.

## Deployment Options

### 1. Local Deployment

#### Prerequisites
- Python 3.7 or higher
- pip package manager

#### Steps
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   streamlit run app.py --server.port=8080 --server.address=0.0.0.0
   ```

3. Access the application at http://localhost:8080

### 2. Docker Deployment

#### Prerequisites
- Docker installed and running

#### Steps
1. Build the Docker image:
   ```bash
   docker build -t ssod-detection-app .
   ```

2. Run the container:
   ```bash
   docker run -p 8080:8080 ssod-detection-app
   ```

3. Access the application at http://localhost:8080

### 3. Heroku Deployment

#### Prerequisites
- Heroku CLI installed
- Heroku account

#### Steps
1. Login to Heroku:
   ```bash
   heroku login
   ```

2. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```

3. Set the Python buildpack:
   ```bash
   heroku buildpacks:set heroku/python
   ```

4. Deploy the application:
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

5. Scale the web dyno:
   ```bash
   heroku ps:scale web=1
   ```

6. Open the application:
   ```bash
   heroku open
   ```

### 4. AWS Deployment

#### Prerequisites
- AWS CLI installed and configured
- AWS account with appropriate permissions

#### Steps
1. Create a deployment package (already created as ssod-deployment.zip)

2. Upload to AWS Elastic Beanstalk:
   - Go to AWS Elastic Beanstalk console
   - Create a new application
   - Choose "Python" platform
   - Upload the ssod-deployment.zip file
   - Configure environment variables if needed
   - Deploy the application

3. Alternatively, deploy to AWS ECS:
   - Push the Docker image to Amazon ECR
   - Create an ECS task definition
   - Create an ECS service
   - Configure load balancing

### 5. Google Cloud Platform Deployment

#### Prerequisites
- Google Cloud SDK installed
- Google Cloud account

#### Steps
1. Authenticate with Google Cloud:
   ```bash
   gcloud auth login
   ```

2. Build and push Docker image to Container Registry:
   ```bash
   docker tag ssod-detection-app gcr.io/your-project-id/ssod-detection-app
   docker push gcr.io/your-project-id/ssod-detection-app
   ```

3. Deploy to Cloud Run:
   ```bash
   gcloud run deploy ssod-detection-app \
     --image gcr.io/your-project-id/ssod-detection-app \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

## Environment Variables

The application supports the following environment variables:

- `PORT`: Port number (default: 8080)
- `MODEL_PATH`: Path to the YOLO model file

## Health Check

The application includes a health check endpoint at `/healthz` on port 8081 for monitoring purposes.

## Model Information

The application uses a YOLOv8 model trained on industrial safety equipment with the following performance metrics:
- Precision: 0.9076
- Recall: 0.6353
- mAP@0.5: 0.7229
- mAP@0.5:0.95: 0.5781

## Troubleshooting

### Common Issues

1. **Model loading errors**: Ensure the model files are present in the `runs/detect/exp_m4_train1/weights/` directory.

2. **Port conflicts**: Change the port using the `PORT` environment variable or the `--server.port` flag.

3. **Memory issues**: The application may require significant memory for model loading. Ensure adequate resources are available.

4. **Docker build failures**: Ensure Docker is installed and running. Check Docker logs for specific error messages.

### Support

For issues with deployment, please check the application logs and ensure all prerequisites are met. The application has been tested with Python 3.9 and the dependencies listed in `requirements.txt`.

Built by Sagar | CodeAlchemy Hackathon 2025