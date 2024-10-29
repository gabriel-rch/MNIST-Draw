import gradio as gr
from PIL.Image import Image, fromarray, Resampling
from model import load_model
import numpy as np


def predict(image):
    # Convert to grayscale
    gray = np.dot(np.array(image)[..., :3], [0.2989, 0.5870, 0.1140])

    # Reshape to batch
    batch = np.array(gray).reshape(1, 28, 28, 1)
    return model.predict(batch)[0]


def update(canvas):
    # Extract from canvas and clear it
    image = canvas["composite"]

    # Create blank background
    background = np.zeros(image.shape, dtype=np.uint8)
    background[..., -1].fill(255)  # Fill alpha channel

    # Add image to background
    image: Image = fromarray(np.add(image, background))

    # Scale down the image with anti-aliasing (as per MNIST)
    scaled_down = image.resize((28, 28), Resampling.LANCZOS)
    confidence = predict(scaled_down)

    print(confidence)

    return scaled_down.resize(image.size), np.argmax(confidence).item()


model = load_model("data/model-weights.h5")

with gr.Blocks() as demo:
    with gr.Row():
        # Default white brush
        brush = gr.Brush(default_size=20, colors=["white"], color_mode="fixed")
        
        # Canvas dimensions
        canvas_size = 400
        container_size = int(canvas_size + (0.2 * canvas_size))

        # Create the drawable area
        canvas = gr.Sketchpad(
            label="Canvas ✏️",
            type="numpy",
            canvas_size=(canvas_size, canvas_size),
            height=container_size,
            layers=False,
            transforms=[],
            brush=brush,
        )

        # Shows the image after MNISTization
        preview = gr.Image(label="MNISTized", width=container_size, height=container_size)

    with gr.Row():
        # Show the prediction
        result = gr.Label()

    # Update the preview and prediction on every stroke
    canvas.change(update, inputs=canvas, outputs=[preview, result], show_progress="hidden")

    demo.launch()
