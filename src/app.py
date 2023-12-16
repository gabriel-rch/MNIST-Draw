from flask import Flask
from flask import request
import tensorflow as tf
import numpy as np
from PIL import Image
import urllib

from model import load_model

app = Flask(__name__)
model = load_model("../data/model-weights.h5")

@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    # Get image from request
    image = request.get_json()["image"]

    # Decode image
    image_data = urllib.request.urlopen(image)

    # Convert to numpy array
    image = np.array(Image.open(image_data))

    # Shrink image to 28x28
    image = tf.image.resize(image, [28, 28], antialias=True, method="bilinear")

    # Remove alpha channel
    image = image[:,:,:3]

    # Convert to grayscale
    image = tf.image.rgb_to_grayscale(image)

    # Predict
    prediction = model.predict(tf.reshape(image, [1, 28, 28, 1]))

    # Create response
    response = {"label": np.argmax(prediction).item(), "confidence": np.max(prediction).item()}
    
    print(prediction)
    return response
