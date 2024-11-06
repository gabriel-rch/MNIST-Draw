from PIL.Image import Image, fromarray, Resampling
import matplotlib.pyplot as plt
import gradio as gr
import numpy as np
import keras


def predict(image):
    # Convert to grayscale
    gray = np.dot(np.array(image)[..., :3], [0.2989, 0.5870, 0.1140])

    # Reshape to batch
    batch = np.array(gray).reshape(1, 28, 28, 1)
    return model.predict(batch)[0]


def plot_confidence(confidence):
    # Plot the confidence
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.bar(np.arange(10), confidence, color="#DF6A19")

    # Set the x and y-axis ticks
    ax.set_xticks(np.arange(10))
    ax.set_yticks([])
    ax.set_ylim(0, 1)

    # Hide the ticks and make the labels white
    ax.tick_params(left=False, bottom=False)
    ax.tick_params(axis='both', which='major', labelsize=12, labelcolor='white')

    # Hide the frame, x and y axis
    ax.set_frame_on(False)

    # Make the background invisible
    fig.patch.set_alpha(0)

    return fig


def update(canvas):
    # Extract from canvas and clear it
    image = canvas["composite"]

    # Create blank background
    background = np.zeros(image.shape, dtype=np.uint8)
    background[..., -1].fill(255)  # Fill alpha channel

    # Add image to background
    image: Image = fromarray(np.add(image, background))
    image_size = image.size

    # Scale down the image with anti-aliasing (as per MNIST)
    scaled_down = image.resize((28, 28), Resampling.LANCZOS)
    confidence = predict(scaled_down)

    return scaled_down.resize(image_size), plot_confidence(confidence)


model = keras.models.load_model("model/mnist_cnn.keras")

with gr.Blocks(theme="default") as demo:
    with gr.Row():
        # Default white brush
        brush = gr.Brush(default_size=18, colors=["white"], color_mode="fixed")

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
        plot = gr.Plot(label="Prediction")

    # Update the preview and prediction on every stroke
    canvas.change(update, inputs=canvas, outputs=[preview, plot], show_progress=False)

    demo.launch()
