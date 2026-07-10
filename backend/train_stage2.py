import os
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam

from dataset_loader_stage2 import train_data, validation_data
from config_stage2 import *
from utils import plot_history

os.makedirs(MODEL_DIR, exist_ok=True)

# Load MobileNetV2
base_model = MobileNetV2(

    weights="imagenet",

    include_top=False,

    input_shape=(224,224,3)

)

# Freeze base model
base_model.trainable=False

x = base_model.output

x = GlobalAveragePooling2D()(x)

x = Dropout(0.3)(x)

x = Dense(128,activation="relu")(x)

output = Dense(3, activation="softmax")(x)

model = Model(inputs=base_model.input,outputs=output)

model.compile(

    optimizer=Adam(learning_rate=LEARNING_RATE),

    loss="categorical_crossentropy",

    metrics=["accuracy"]

)

checkpoint = ModelCheckpoint(

    MODEL_PATH,

    monitor="val_accuracy",

    save_best_only=True,

    verbose=1

)

early = EarlyStopping(

    monitor="val_loss",

    patience=5,

    restore_best_weights=True

)

history = model.fit(

    train_data,

    validation_data=validation_data,

    epochs=EPOCHS,

    callbacks=[checkpoint,early]

)

loss,accuracy=model.evaluate(validation_data)

print()

print("="*40)

print("=" * 50)
print("Stage 2 (Tumor Type Classification)")
print(f"Validation Accuracy : {accuracy:.4f}")
print("=" * 50)

plot_history(history)

model.save(MODEL_PATH)

print("\nTumor Type Classifier Saved Successfully")
print("Saved Model :", MODEL_PATH)