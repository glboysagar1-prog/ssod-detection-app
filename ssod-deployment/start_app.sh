#!/bin/bash
# Deployment script for SSOD Detection App

# Install dependencies
python3 -m pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py --server.port=8080 --server.address=0.0.0.0
