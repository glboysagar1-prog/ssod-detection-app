import os

def find_model_file(base_path="."):
    """
    Automatically find the .pt model file in the directory tree,
    prioritizing specific models and then by modification time
    """
    # Priority model paths (in order of preference)
    priority_models = [
        "runs/detect/exp_rtx4060_150epoch/weights/best.pt",
        "runs/detect/exp_m4_yolov8m_50epoch/weights/best.pt",
        "runs/detect/exp_m4_train1/weights/best.pt",
        "runs/detect/exp_m4_train1/weights/last.pt"
    ]
    
    # Check for priority models first
    for model_path in priority_models:
        if os.path.exists(model_path):
            print(f"Found priority model at: {model_path}")
            return model_path
    
    # If no priority models found, search for any .pt file
    model_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".pt"):
                full_path = os.path.join(root, file)
                model_files.append((full_path, os.path.getmtime(full_path)))
    
    # Sort by modification time (newest first)
    if model_files:
        model_files.sort(key=lambda x: x[1], reverse=True)
        return model_files[0][0]  # Return path of newest model
    
    return None

def load_model():
    """
    Load the YOLO model with automatic detection, prioritizing the latest model
    """
    model_path = find_model_file(".")
    if model_path:
        print(f"Loading model from: {model_path}")
        # Import YOLO only when needed
        from ultralytics import YOLO  # type: ignore
        return YOLO(model_path)
    else:
        raise FileNotFoundError("No model (.pt) file found. Please add your trained weights.")