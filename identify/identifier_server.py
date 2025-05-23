import os
import warnings
import requests

import gevent
import numpy as np
import tensorflow as tf
from bottle import Bottle, request
from gevent import monkey
from tensorflow.keras.preprocessing import image


# Initialize global variables and constants
MODEL_PATH = os.path.join("models", f'LeafQuest_IdentifyModel_v{os.getenv("IDENTIFY_MODEL_VER", "1")}.keras')
IMG_SIZE = (224, 224)
model = tf.keras.models.load_model(MODEL_PATH, compile=False)
model.compile()

monkey.patch_all()
app = Bottle()

UPLOAD_DIR = "./uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

class_labels = {}
with open("class_labels.txt", "r") as f:
    for line in f:
        index, label = line.strip().split(", ")
        class_labels[int(index)] = label


def determine_identity(req_id, file_path):
    """Spawned as greenlet which Identifies the given image."""
    img = image.load_img(path=file_path, target_size=IMG_SIZE)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.resnet.preprocess_input(img_array)

    predictions = model.predict(img_array, verbose=0)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    predicted_class_name = class_labels.get(predicted_class_index, "Unknown")
    confidence = np.max(predictions) * 100  # Convert to percentage

    # Delete the temp file
    os.remove(file_path)

    print(predicted_class_name, confidence)

    # send response back to server
    requests.post(os.environ.get("MAIN_SERVER_HOST") + "/identify/return/",
                  json={
                      "req_id": req_id,
                      "prediction": predicted_class_name,
                      "confidence": str(confidence)
                  })


@app.post('/identify')
def identify():
    try:
        """Receives an image from the requestor"""
        upload = request.files.get('image')

        if not upload:
            return {"status": "error", "message": "No file uploaded"}

        name, ext = os.path.splitext(upload.filename)
        if ext.lower() not in ('.png', '.jpg', '.jpeg', '.gif'):
            return {"status": "error", "message": "Unsupported file type"}

        # get req_id
        req_id = request.forms.get("req_id")
        if req_id is None:
            return {"status": "error", "message": "No request id"}

        # Store the file temporarily (keras preprocessing only accepts file paths, not file streams)
        save_path = os.path.join(UPLOAD_DIR, upload.filename)
        upload.save(save_path)

        gevent.spawn(determine_identity, req_id, save_path)

        return {"status": "received"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def main():
    print("Starting identifier server...")

    app.run(
        host='0.0.0.0',
        port=8080,
        server='gevent',
    )


if __name__ == '__main__':
    main()
