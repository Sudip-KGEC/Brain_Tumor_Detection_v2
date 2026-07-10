import cv2
import numpy as np

# Assuming IMAGE_SIZE is 224 based on your previous predict.py
IMAGE_SIZE = (224, 224) 

def preprocess_image_from_bytes(image_bytes: bytes):
    """
    Decodes an image directly from memory (FastAPI UploadFile bytes)
    and preprocesses it for the Keras models.
    """
    # Convert bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    
    # Decode image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if image is None:
        raise Exception("Invalid image format or corrupted file.")

    # Convert BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Resize to match model input
    image = cv2.resize(image, IMAGE_SIZE)

    # Normalize pixel values
    image = image.astype("float32") / 255.0

    # Expand dimensions (batch size of 1)
    image = np.expand_dims(image, axis=0)

    return image