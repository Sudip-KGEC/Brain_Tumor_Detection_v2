import os
import time
import numpy as np
from tensorflow.keras.models import load_model

# Import our dedicated hardware controller and preprocessor
from serial_controller import hardware
from preprocess import preprocess_image_from_bytes

# -----------------------------
# CONFIGURATION
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

STAGE2_CLASSES = {0: "Glioma", 1: "Meningioma", 2: "Pituitary"}

# -----------------------------
# LOAD MODELS (Global State)
# -----------------------------
print("[INFO] Loading AI Models...")
try:
    stage0_model = load_model(os.path.join(MODEL_DIR, "brain_classifier.keras"))
    stage1_model = load_model(os.path.join(MODEL_DIR, "tumor_detector.keras"))
    stage2_model = load_model(os.path.join(MODEL_DIR, "tumor_type_classifier.keras"))
    print("[INFO] All Models Loaded Successfully")
except Exception as e:
    print(f"[ERROR] Model loading failed: {e}")

# -----------------------------
# ML PREDICTION LOGIC
# -----------------------------
def predict_stage0(image):
    prediction = stage0_model.predict(image, verbose=0)[0][0]
    return ("Brain", (1 - prediction) * 100) if prediction < 0.5 else ("NotBrain", prediction * 100)

def predict_stage1(image):
    prediction = stage1_model.predict(image, verbose=0)[0][0]
    return ("Normal", (1 - prediction) * 100) if prediction < 0.5 else ("Tumor", prediction * 100)

def predict_stage2(image):
    prediction = stage2_model.predict(image, verbose=0)[0]
    index = np.argmax(prediction)
    return STAGE2_CLASSES[index], float(prediction[index]) * 100

# -----------------------------
# API ORCHESTRATOR
# -----------------------------
def process_image_pipeline(image_bytes: bytes):
    start_time = time.time()
    
    # 1. Decode and Preprocess image from memory
    try:
        image = preprocess_image_from_bytes(image_bytes)
    except Exception as e:
        raise ValueError(f"Image processing failed: {str(e)}")

    # 2. Stage 0: Brain Verification
    stage0_label, stage0_conf = predict_stage0(image)
    if stage0_label == "NotBrain":
        hardware.send_command("INVALID")
        return build_response(start_time, stage0_label, stage0_conf, message="Invalid Brain MRI")

    # 3. Stage 1: Tumor Detection
    stage1_label, stage1_conf = predict_stage1(image)
    if stage1_label == "Normal":
        hardware.send_command("NORMAL")
        return build_response(start_time, stage0_label, stage0_conf, stage1_label, stage1_conf, message="Normal Brain")

    # 4. Stage 2: Classification
    stage2_label, stage2_conf = predict_stage2(image)
    hardware.send_command(stage2_label.upper())

    return build_response(
        start_time, stage0_label, stage0_conf, 
        stage1_label, stage1_conf, stage2_label, stage2_conf, 
        message="Prediction Completed"
    )

def build_response(start, s0_lab, s0_conf, s1_lab=None, s1_conf=None, s2_lab=None, s2_conf=None, message=""):
    """Helper to build standardized JSON API responses."""
    cmd = "INVALID"
    if s1_lab == "Normal": cmd = "NORMAL"
    elif s2_lab: cmd = s2_lab.upper()

    return {
        "stage0": {"label": s0_lab, "confidence": round(s0_conf, 2)},
        "stage1": {"label": s1_lab, "confidence": round(s1_conf, 2)} if s1_lab else None,
        "stage2": {"label": s2_lab, "confidence": round(s2_conf, 2)} if s2_lab else None,
        "led": {
            "command": cmd, 
            "status": "ON" if (hardware.serial_conn and hardware.serial_conn.is_open) else "OFFLINE"
        },
        "processing_time": round(time.time() - start, 3),
        "message": message
    }