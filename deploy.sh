#!/bin/bash

# SSOD Detection App Deployment Script

echo "SSOD Detection App Deployment Options:"
echo "====================================="
echo "1. Local Deployment"
echo "2. Docker Deployment"
echo "3. Heroku Deployment"
echo "4. AWS Deployment"
echo ""
echo "Select deployment option (1-4):"
read option

case $option in
    1)
        echo "Starting local deployment..."
        echo "Installing dependencies..."
        pip install -r requirements.txt
        echo "Starting Streamlit app..."
        streamlit run app.py --server.port=8080 --server.address=0.0.0.0
        ;;
    2)
        echo "Starting Docker deployment..."
        if command -v docker &> /dev/null; then
            echo "Building Docker image..."
            docker build -t ssod-detection-app .
            echo "Running Docker container..."
            docker run -p 8080:8080 ssod-detection-app
        else
            echo "Docker is not installed. Please install Docker first."
        fi
        ;;
    3)
        echo "Starting Heroku deployment..."
        echo "Make sure you have Heroku CLI installed and logged in."
        echo "Creating Heroku app..."
        heroku create ssod-detection-app-$(date +%s)
        echo "Setting Python buildpack..."
        heroku buildpacks:set heroku/python
        echo "Deploying to Heroku..."
        git add .
        git commit -m "Deploy to Heroku"
        git push heroku main
        echo "Opening app..."
        heroku open
        ;;
    4)
        echo "Starting AWS deployment..."
        echo "This requires AWS CLI to be installed and configured."
        echo "Creating deployment package..."
        zip -r ssod-deployment.zip . -x "*.git*" "runs/detect/exp_m4_train1/weights/*.pt" "sample_images/*"
        echo "Deployment package created. You can now deploy to AWS Elastic Beanstalk."
        ;;
    *)
        echo "Invalid option. Please select 1, 2, 3, or 4."
        ;;
esac