import os
from PIL import Image

# Configuration
TARGET_SIZE = (224, 224)  # Change to (150, 150) if your model architecture expects that
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(BASE_DIR, r'C:\Users\Charishma\final project\custom_dataset')

print(f"Starting image normalization in: {dataset_path}")
print(f"Target dimensions: {TARGET_SIZE}\n")

if not os.path.exists(dataset_path):
    print(f"[ERROR] Could not find 'custom fruits' folder at {dataset_path}")
    exit()

# Counters for tracking progress
total_resized = 0
total_skipped = 0

# Loop through all 15 fruit folders
for fruit_folder in os.listdir(dataset_path):
    fruit_folder_path = os.path.join(dataset_path, fruit_folder)
    
    # Ensure it's a directory, not a random file
    if os.path.isdir(fruit_folder_path):
        print(f"Processing folder: {fruit_folder}...")
        
        for filename in os.listdir(fruit_folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(fruit_folder_path, filename)
                
                try:
                    # Open the image safely
                    with Image.open(img_path) as img:
                        # Check if it already matches the target size to save time
                        if img.size == TARGET_SIZE:
                            total_skipped += 1
                            continue
                        
                        # Convert to RGB (handles PNG transparency channels falling over during JPEG conversions)
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                            
                        # Resize using high-quality resampling (LANCZOS)
                        resized_img = img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
                        
                        # Overwrite the original file with the resized version
                        resized_img.save(img_path, 'JPEG', quality=95)
                        total_resized += 1
                        
                except Exception as e:
                    print(f"  [ERROR] Failed to resize {filename}: {e}")

print("\n" + "="*40)
print(" Image Normalization Complete!")
print(f" Total images resized: {total_resized}")
print(f" Total images already standard: {total_skipped}")
print("="*40)