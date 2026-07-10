import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(BASE_DIR, "dataset", "stage2")

MODEL_DIR = os.path.join(BASE_DIR, "models")

MODEL_NAME = "tumor_type_classifier.keras"

MODEL_PATH = os.path.join(MODEL_DIR, MODEL_NAME)

IMAGE_SIZE = (224, 224)

BATCH_SIZE = 32

EPOCHS = 20

LEARNING_RATE = 0.0001

SEED = 42