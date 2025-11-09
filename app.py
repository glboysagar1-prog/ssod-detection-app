import streamlit as st
from ultralytics import YOLO
from PIL import Image
import tempfile, os, requests
from utils.falcon_update import check_falcon_update
import numpy as np
import cv2

# Optional: Dynamic model detection
try:
    from model_locator import load_model
    model = load_model()
except ImportError:
    # Fallback to fixed path
    model_path = "runs/detect/exp_m4_train1/weights/best.pt"
    model = YOLO(model_path)

st.set_page_config(page_title="YOLOv8 Object Detection", layout="wide")

st.title("🚀 Smart Object Detection (YOLOv8 + Falcon)")
st.write("Upload an image to test the trained model on cluttered/uncluttered environments.")

# Show supported classes
st.info("This model detects the following industrial safety objects: OxygenTank, NitrogenTank, FirstAidBox, FireAlarm, SafetySwitchPanel, EmergencyPhone, FireExtinguisher")

# Falcon auto-update check
new_model_path = check_falcon_update("runs/detect/exp_m4_train1/weights/best.pt")
if new_model_path != "runs/detect/exp_m4_train1/weights/best.pt":
    model = YOLO(new_model_path)
    st.success("✅ Model updated automatically from Falcon retraining!")

# File uploader
uploaded_file = st.file_uploader("�� Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Get the file extension
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    # Create a temporary file with the correct extension
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}')
    temp_file.write(uploaded_file.getvalue())
    temp_file.close()  # Close the file so YOLO can access it

    # Display uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    st.write("🔍 Detecting objects...")

    try:
        # Use the temporary file path for prediction
        with st.spinner('Processing image...'):
            results = model.predict(source=temp_file.name, conf=0.4, device="cpu")
        
        # Plot the results
        result_image = results[0].plot()
        
        # Ensure the image is in the correct format for display
        if len(result_image.shape) == 3:
            # If it's a 3-channel image, it's likely BGR, convert to RGB
            if result_image.shape[2] == 3:
                # Convert BGR to RGB
                result_image_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)
            else:
                result_image_rgb = result_image
        else:
            # Grayscale image
            result_image_rgb = result_image
            
        # Display detection result
        st.image(result_image_rgb, caption="Detection Result", use_container_width=True)
        
        # Show detection details
        boxes = results[0].boxes
        if boxes is not None and len(boxes) > 0:
            st.success(f"✅ Detected {len(boxes)} objects")
            
            # Show details of detected objects
            class_names = model.names
            for i, box in enumerate(boxes):
                class_id = int(box.cls.item())
                confidence = float(box.conf.item())
                class_name = class_names.get(class_id, f"Class {class_id}")
                st.write(f"Object {i+1}: {class_name} (Confidence: {confidence:.2f})")
        else:
            st.info("ℹ️ No industrial safety objects detected. This model only detects: OxygenTank, NitrogenTank, FirstAidBox, FireAlarm, SafetySwitchPanel, EmergencyPhone, FireExtinguisher")
            
    except Exception as e:
        st.error(f"Error during detection: {str(e)}")
        st.write("This might happen if the image format is not supported or if there's an issue with the model.")

    # Clean up the temporary file
    os.unlink(temp_file.name)

st.markdown("---")
st.subheader("📊 Model Summary")
st.json({
    "Precision": 0.9076,
    "Recall": 0.6353,
    "mAP@0.5": 0.7229,
    "mAP@0.5:0.95": 0.5781
})

st.caption("Built by Sagar | CodeAlchemy Hackathon 2025")
