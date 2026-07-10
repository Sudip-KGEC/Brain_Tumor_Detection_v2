from tensorflow.keras.preprocessing.image import ImageDataGenerator

gen = ImageDataGenerator()

print("Stage 0")
data = gen.flow_from_directory("backend/dataset/stage0")
print(data.class_indices)

print("\nStage 1")
data = gen.flow_from_directory("backend/dataset/stage1")
print(data.class_indices)

print("\nStage 2")
data = gen.flow_from_directory("backend/dataset/stage2")
print(data.class_indices)