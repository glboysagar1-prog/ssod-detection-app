import os
from ultralytics import YOLO

def find_model_file(base_path="."):
    """
    Automatically find the .pt model file in the directory tree
    """
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".pt"):
                return os.path.join(root, file)
    return None

def load_model():
    """
    Load the YOLO model with automatic detection
    """
    model_path = find_model_file(".")
    if model_path:
        print(f"Found model at: {model_path}")
        return YOLO(model_path)
    else:
        raise FileNotFoundError("No model (.pt) file found. Please add your trained weights.")

# Example usage:
# model = load_model()
