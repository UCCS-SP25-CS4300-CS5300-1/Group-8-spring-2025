##
# Model Testing File
##

import warnings
import os
import glob

import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

warnings.filterwarnings("ignore", category=UserWarning, module='tensorflow')
warnings.filterwarnings("ignore", category=DeprecationWarning, module='tensorflow')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'



# Constants
IMG_PATH = "img"
MODEL_PATH = os.path.join("models", "LeafQuest_FinalModel.keras")
IMG_SIZE = (224, 224)

# Create & load label mapping
class_labels = {}
with open("class_labels.txt", "r") as f:
    for line in f:
        index, label = line.strip().split(", ")
        class_labels[int(index)] = label

image_paths = glob.glob(os.path.join(IMG_PATH, "*"))

# Load model
for img_path in image_paths:
    img = image.load_img(img_path, target_size=IMG_SIZE)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.resnet.preprocess_input(img_array)

model = tf.keras.models.load_model(MODEL_PATH)

for img_path in image_paths:
    img = image.load_img(img_path, target_size=IMG_SIZE)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.resnet.preprocess_input(img_array)

    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    predicted_class_name = class_labels.get(predicted_class_index, "Unknown")
    confidence = np.max(predictions) * 100  # Convert to percentage

    print(f"Image: {os.path.basename(img_path)} | Predicted Class: {predicted_class_name} (Index: {predicted_class_index}) | Confidence: {confidence:.2f}%")
