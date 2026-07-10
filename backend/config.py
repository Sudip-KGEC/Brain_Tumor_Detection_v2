import os

# ===============================
# DATASET PATHS
# ===============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(BASE_DIR, "dataset", "stage0")

MODEL_DIR = os.path.join(BASE_DIR, "models")

MODEL_NAME = "brain_classifier.keras"

MODEL_PATH = os.path.join(MODEL_DIR, MODEL_NAME)

# ===============================
# IMAGE SETTINGS
# ===============================

IMAGE_SIZE = (224, 224)

BATCH_SIZE = 32

EPOCHS = 20

LEARNING_RATE = 0.0001

# ===============================
# RANDOM SEED
# ===============================

SEED = 42