import os
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# 1. Setup paths and dimensions
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(BASE_DIR, 'custom_dataset') 

IMG_SIZE = (224, 224) 
BATCH_SIZE = 32

print(f"Loading image dataset from: {dataset_path}")

# 2. Data Preparation & Validation Split (80/20)
# 2. Data Preparation & Validation Split (80/20)
# Added a validation split directly to the base configuration
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    validation_split=0.2 
)

# FIXED: Explicitly set seed and shuffle behaviors to protect class balance
train_generator = datagen.flow_from_directory(
    dataset_path,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    seed=42,
    shuffle=True
)

val_generator = datagen.flow_from_directory(
    dataset_path,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    seed=42,
    shuffle=True # <-- CHANGED TO TRUE to fix class calculation warp
)


num_classes = train_generator.num_classes
class_indices = train_generator.class_indices
labels = [k for k, v in sorted(class_indices.items(), key=lambda item: item[1])]

# Save class names for your dashboard interface
with open(os.path.join(BASE_DIR, 'labels.txt'), 'w') as f:
    for label in labels:
        f.write(f"{label}\n")
print(f"Saved {num_classes} classes to labels.txt")

# 3. Model Architecture (MobileNetV2 Transfer Learning)
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.3)(x)  
predictions = Dense(num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# 4. Save Callbacks
model_path = os.path.join(BASE_DIR, 'fruit_vision_model.h5')
callbacks = [
    ModelCheckpoint(model_path, monitor='val_loss', save_best_only=True, verbose=1),
    EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True, verbose=1)
]

# 5. Run Training
print("\nTraining Vision Model...")
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=10,
    callbacks=callbacks,
    verbose=1
)

print(f"\nVision Model saved as '{model_path}'")