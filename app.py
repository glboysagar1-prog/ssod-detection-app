import streamlit as st
from PIL import Image
import tempfile, os
import numpy as np

# Try to import cv2, but provide fallback if not available
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    st.warning("⚠️ OpenCV not available in this environment. Some image processing features may be limited.")

# Import health check functionality
try:
    from health_check import start_health_check_server
    health_server = start_health_check_server(8081)
except ImportError:
    health_server = None
    print("Health check module not available")

# Global variable to store the model
model = None

# Function to safely import and load the model
def load_model_safely():
    """Safely load the YOLO model with error handling"""
    global model
    try:
        # Import YOLO only when needed
        from ultralytics import YOLO  # type: ignore
        
        # Try to use the model locator for automatic detection
        try:
            from model_locator import load_model
            model = load_model()
            st.success("✅ Model loaded successfully using automatic detection")
            return model
        except FileNotFoundError as e:
            st.error(f"Model file not found: {e}")
            st.info("ℹ️ The application will run in demo mode without object detection")
            return None
        except Exception as e:
            st.warning(f"Automatic model detection failed: {e}")
            # Fallback to fixed path with update checking
            default_model_path = "runs/detect/exp_rtx4060_150epoch/weights/best.pt"
            if not os.path.exists(default_model_path):
                st.error(f"Default model file not found at: {default_model_path}")
                st.info("ℹ️ The application will run in demo mode without object detection")
                return None
            try:
                # Import the update function only when needed
                from utils.falcon_update import check_falcon_update
                # Check for updates from Falcon
                updated_model_path = check_falcon_update(default_model_path)
                model = YOLO(updated_model_path)
                if updated_model_path != default_model_path:
                    st.success("✅ Model updated automatically from Falcon retraining!")
                else:
                    st.info("ℹ️ Using the latest available model")
                return model
            except Exception as e2:
                st.error(f"Failed to load model: {e2}")
                # Final fallback - try to load the default model directly
                try:
                    model = YOLO(default_model_path)
                    st.info("ℹ️ Using default model path")
                    return model
                except Exception as e3:
                    st.error(f"Critical error: Could not load any model. {e3}")
                    st.info("ℹ️ The application will run in demo mode without object detection")
                    return None
    except ImportError as e:
        st.error(f"Failed to import YOLO: {e}")
        st.info("ℹ️ The application will run in demo mode without object detection")
        return None
    except Exception as e:
        st.error(f"Unexpected error loading model: {e}")
        st.info("ℹ️ The application will run in demo mode without object detection")
        return None

# Function to convert BGR to RGB (fallback if cv2 not available)
def bgr_to_rgb(image_array):
    if CV2_AVAILABLE and len(image_array.shape) == 3 and image_array.shape[2] == 3:
        return image_array[:, :, ::-1]  # Reverse the last dimension to convert BGR to RGB
    return image_array

# Load the model when the app starts
model = load_model_safely()

st.set_page_config(page_title="YOLOv8 Object Detection", layout="wide")

st.title("🚀 Smart Object Detection (YOLOv8 + Falcon)")
st.write("Upload an image to test the trained model on cluttered/uncluttered environments.")

# Show supported classes
st.info("This model detects the following industrial safety objects: OxygenTank, NitrogenTank, FirstAidBox, FireAlarm, SafetySwitchPanel, EmergencyPhone, FireExtinguisher")

# Manual model refresh button
if st.button("🔄 Check for Model Updates"):
    with st.spinner("Checking for model updates..."):
        if model is None:
            st.warning("❌ No model available. Cannot check for updates.")
        else:
            try:
                # Import the update function only when needed
                from utils.falcon_update import check_falcon_update
                
                # Get current model path - handle cases where it might not exist
                current_model_path = "runs/detect/exp_rtx4060_150epoch/weights/best.pt"
                if hasattr(model, 'overrides') and model.overrides.get('model'):
                    current_model_path = str(model.overrides.get('model', current_model_path))
                
                new_model_path = check_falcon_update(current_model_path)
                if new_model_path != current_model_path:
                    # Import YOLO here as well for model update
                    from ultralytics import YOLO  # type: ignore
                    model = YOLO(new_model_path)
                    st.success("✅ Model updated successfully!")
                    st.rerun()
                else:
                    st.info("ℹ️ Your model is already up to date")
            except Exception as e:
                st.error(f"Error updating model: {e}")

# File uploader
uploaded_file = st.file_uploader("📷 Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Get the file extension
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    # Create a temporary file with the correct extension
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}')
    temp_file.write(uploaded_file.getvalue())
    temp_file.close()  # Close the file so YOLO can access it

    # Display uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    
    if model is None:
        st.warning("❌ No model available for object detection. Running in demo mode.")
        st.info("In a deployed environment, make sure the model files are included in the deployment package.")
    else:
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
                result_image_rgb = bgr_to_rgb(result_image)
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
                # Convert boxes to numpy for easier handling
                boxes_data = boxes.cpu().numpy()
                
                # Access box data directly using numpy array indexing
                cls_data = boxes_data.cls if boxes_data.cls.ndim > 0 else np.array([boxes_data.cls])
                conf_data = boxes_data.conf if boxes_data.conf.ndim > 0 else np.array([boxes_data.conf])
                
                for i in range(len(cls_data)):
                    class_id = int(cls_data[i])
                    confidence = float(conf_data[i])
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