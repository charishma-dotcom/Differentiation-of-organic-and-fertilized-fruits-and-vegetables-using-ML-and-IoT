import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Configuration
n_total = 20000
n_per_class = n_total // 2

fruits = [
    'Apple', 'Banana', 'Orange', 'Ivy gourd', 'Carrot', 
    'Mango', 'Grapes', 'Guava', 'Sapota', 'Papaya', 
    'Onion', 'Garlic', 'Beetroot', 'Brinjal', 'Pomegranate'
]

sizes = ['medium', 'large', 'small']
colours = ['vibrant', 'dull', 'neutral', 'irregular']
shapes = ['oval', 'round', 'elongated', 'irregular']

data = []

# Generate balanced classes (10,000 Organic, 10,000 Fertilized)
for status in ['organic', 'fertilized']:
    for _ in range(n_per_class):
        item = np.random.choice(fruits)
        
        if status == 'organic':
            # Organic: Higher probability of small/medium sizes and dull/neutral colours
            size = np.random.choice(sizes, p=[0.5, 0.1, 0.4])
            colour = np.random.choice(colours, p=[0.1, 0.5, 0.3, 0.1])
            shape = np.random.choice(shapes, p=[0.3, 0.3, 0.2, 0.2])
        else:
            # Fertilized: Higher probability of large sizes and vibrant colours
            size = np.random.choice(sizes, p=[0.3, 0.6, 0.1])
            colour = np.random.choice(colours, p=[0.7, 0.1, 0.1, 0.1])
            shape = np.random.choice(shapes, p=[0.4, 0.4, 0.1, 0.1])
        
        data.append([item, size, colour, shape, status])

# Map to the exact column names from your image
columns = ['item name', 'size', 'colour', 'shape', 'status']
df = pd.DataFrame(data, columns=columns)

# Shuffle the rows so the classes are mixed randomly
df = df.sample(frac=1).reset_index(drop=True)

# Save directly to your project workspace
output_filename = 'fruit_authenticity_dataset.csv'
df.to_csv(output_filename, index=False)

print(f"Success! Dataset saved as '{output_filename}' with {len(df)} rows.")
print("\nClass distribution:")
print(df['status'].value_counts())