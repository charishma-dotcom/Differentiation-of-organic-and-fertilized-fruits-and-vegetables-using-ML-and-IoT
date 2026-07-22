import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam

# 1. SETUP
DATASET_DIR = 'fruit d/fruits-360_100x100/fruits-360/Training'
IMG_SIZE = (100, 100)
# Add 'Background' here after you run the capture script!
KEYWORDS = ['Apple', 'Banana', 'Mango', 'Orange', 'Pomegranate', 'Grape', 'Background']

# 2. STRONGER DATA AUGMENTATION
# This "fakes" different lighting and hand positions
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.7, 1.3], # Helps with your room lighting
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=32,
    classes=KEYWORDS,
    class_mode='categorical',
    subset='training'
)

# 3. IMPROVED MODEL ARCHITECTURE
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 3)),
    BatchNormalization(), # Stabilizes learning
    MaxPooling2D(2, 2),
    
    Conv2D(64, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(2, 2),
    
    Conv2D(128, (3, 3), activation='relu'), # Extra layer for detail
    MaxPooling2D(2, 2),
    
    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.5), # Forces the AI to stop "memorizing"
    Dense(len(KEYWORDS), activation='softmax')
])

model.compile(optimizer=Adam(learning_rate=0.0001), # Slower learning is more precise
              loss='categorical_crossentropy', 
              metrics=['accuracy'])

# 4. TRAIN
model.fit(train_generator, epochs=15) # Increased epochs for better learning
model.save('fruit_vision_model.h5')
print("New model saved! Try running main.py now.")