from keras.datasets import mnist  # type: ignore
import keras
import time

(X_train, y_train), (X_test, y_test) = mnist.load_data()

# Define the model
model = keras.models.Sequential()

# Add the ConvPool layers
model.add(keras.Input((28, 28, 1)))
model.add(keras.layers.Conv2D(8, kernel_size=(4, 4), activation="relu", name="1st-Conv2D"))
model.add(keras.layers.MaxPool2D(name="1st-MaxPool"))
model.add(keras.layers.Conv2D(8, kernel_size=(2, 2), activation="relu", name="2nd-Conv2D"))
model.add(keras.layers.MaxPool2D(name="2nd-MaxPool"))

# Fully-connected layers
model.add(keras.layers.Flatten(name="Flatten"))
model.add(keras.layers.Dense(32, activation="relu", name="HiddenLayer"))
model.add(keras.layers.Dense(10, activation="softmax", name="OutputLayer"))

# Compile and train the model
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(X_train.reshape(-1, 28, 28, 1), y_train, epochs=5, batch_size=32, validation_split=0.2)

# Save the model
model.save("model/mnist_cnn.keras")
