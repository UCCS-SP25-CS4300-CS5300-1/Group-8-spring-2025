## 
## This script is for custom tests of images, the bulk test from CIFAR10 (10k images) is done in train.ipynb
## Feel free to add any images you want into /img and test them (even if they're not one of the 10 classes because that's fun to test too)
## Just make sure to add any new image path to the img_paths list
## 

import logging, os
logging.disable(logging.WARNING)
# Disable GPU since we're only doing testing of a pre-trained model
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

model = load_model('LeafQuestRepo/Group-8-spring-2025/EfficientNetB0/EfficientNetB0_CIFAR10.keras')
labels = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']


# Testing unseen images of one horse, truck, and ship each
img_paths = [
    'LeafQuestRepo/Group-8-spring-2025/EfficientNetB0/img/test1.jpg',
    'LeafQuestRepo/Group-8-spring-2025/EfficientNetB0/img/test2.jpg',
    'LeafQuestRepo/Group-8-spring-2025/EfficientNetB0/img/test3.jpg'
]

for img_path in img_paths:
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)

    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)[0]

    print(f"Image: {img_path} --> Predicted class: {labels[predicted_class]}")