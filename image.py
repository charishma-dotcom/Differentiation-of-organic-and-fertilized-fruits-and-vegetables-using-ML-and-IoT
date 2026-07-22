import os
import cv2

folder_path = r'C:\Users\Charishma\final project\custom_dataset\Brinjal'
keep_count = 500

def get_blur_score(image_path):
    # Load image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return -1
    # Calculate the Laplacian variance (sharpness score)
    return cv2.Laplacian(img, cv2.CV_64F).var()

# 1. Gather all images and their scores
image_scores = []
valid_extensions = ('.png', '.jpg', '.jpeg')

print("Analyzing image quality...")
for filename in os.listdir(folder_path):
    if filename.lower().endswith(valid_extensions):
        path = os.path.join(folder_path, filename)
        score = get_blur_score(path)
        if score != -1:
            image_scores.append((filename, score))

# 2. Sort by score (highest quality first)
image_scores.sort(key=lambda x: x[1], reverse=True)

# 3. Identify images to keep and images to delete
to_keep = [img[0] for img in image_scores[:keep_count]]
to_delete = [img[0] for img in image_scores[keep_count:]]

# 4. Delete the "bad" ones
print(f"Keeping the top {len(to_keep)} sharpest images. Deleting {len(to_delete)} lower-quality images...")
for filename in to_delete:
    os.remove(os.path.join(folder_path, filename))

print("Cleanup complete!")