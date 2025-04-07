##
## This script is a one time preprocess before training, but it can be re-run to fit different models.
## It is currently fit to ResNet50 (IMAGE_SIZE)
## The output is a tfrecord file to use with tensorflow
##

import tensorflow as tf
import os
import glob

# Update these paths as needed
DATASET_DIR = r"C:\LeafQuest_Dataset" 
TFRECORD_FILENAME = "resnet50_dataset.tfrecord"
IMAGE_SIZE = (224, 224)

# Get the class folders and create mappings to integer labels
class_names = sorted([d for d in os.listdir(DATASET_DIR) if os.path.isdir(os.path.join(DATASET_DIR, d))])
class_to_index = {name: idx for idx, name in enumerate(class_names)}
print("Found classes:", class_to_index)

# Helper functions for TFRecord serialization
def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def serialize_example(image_bytes, label):
    feature = {
        'image': _bytes_feature(image_bytes),
        'label': _int64_feature(label),
    }
    example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
    return example_proto.SerializeToString()

def process_image(image_path):
    image_raw = tf.io.read_file(image_path)
    img = tf.image.decode_image(image_raw, channels=3)
    img = tf.image.resize(img, IMAGE_SIZE)
    img = tf.cast(img, tf.uint8)
    encoded_img = tf.io.encode_jpeg(img)
    return encoded_img.numpy()

# Create .tfrecord file
with tf.io.TFRecordWriter(TFRECORD_FILENAME) as writer:
    for class_name in class_names:
        class_dir = os.path.join(DATASET_DIR, class_name)
        image_paths = glob.glob(os.path.join(class_dir, "*"))
        label = class_to_index[class_name]
        print(f"Processing class '{class_name}' with label {label}: {len(image_paths)} images")
        for image_path in image_paths:
            try:
                image_bytes = process_image(image_path)
                example = serialize_example(image_bytes, label)
                writer.write(example)
            except Exception as e:
                print(f"Error processing {image_path}: {e}")

print(f"Saved as {TFRECORD_FILENAME}")