import os
DATASET_DIR = r"C:\LeafQuest_Dataset"

# Get class folders and map each class string to an integer label
class_names = sorted([d for d in os.listdir(DATASET_DIR) if os.path.isdir(os.path.join(DATASET_DIR, d))])
class_to_index = {name: idx for idx, name in enumerate(class_names)}

# Write to a text file
with open("class_labels.txt", "w") as f:
    for class_name, index in class_to_index.items():
        f.write(f"{index}, {class_name}\n")