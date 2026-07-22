import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# --- 1. SETTINGS ---
DATASET_PATH = 'fruit d' 
IMG_SIZE = (100, 100) # Fruit-360 standard size
BATCH_SIZE = 64       
EPOCHS = 10

# --- 2. DATA LOADERS ---
datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_gen = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

val_gen = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# --- 3. ARCHITECTURE ---
model = Sequential([
    Conv2D(16, (5, 5), activation='relu', input_shape=(100, 100, 3)),
    MaxPooling2D(2, 2),
    
    Conv2D(32, (5, 5), activation='relu'),
    MaxPooling2D(2, 2),
    
    Conv2D(64, (5, 5), activation='relu'),
    MaxPooling2D(2, 2),
    
    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(train_gen.num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# --- 4. TRAINING ---
print(f"Training started for classes: {list(train_gen.class_indices.keys())}")
model.fit(train_gen, validation_data=val_gen, epochs=EPOCHS)

# --- 5. SAVE ---
model.save('fruit_vision_model.h5')
print("Success! 'fruit_vision_model.h5' has been created.")