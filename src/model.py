import keras

def load_model(weights: str) -> keras.Sequential:

    # Define the model
    model = keras.models.Sequential()

    # Add the ConvPool layers
    model.add(keras.Input((28, 28, 1)))
    model.add(keras.layers.Conv2D(32, kernel_size=(5, 5), activation='relu', name='1st-Conv2D'))
    model.add(keras.layers.MaxPool2D(name='1st-MaxPool'))
    model.add(keras.layers.Conv2D(32, kernel_size=(5, 5), activation='relu', name='2nd-Conv2D'))
    model.add(keras.layers.MaxPool2D(name='2nd-MaxPool'))

    # Fully-connected layers
    model.add(keras.layers.Flatten(name='Flatten'))
    model.add(keras.layers.Dense(32, activation='relu', name='HiddenLayer'))
    model.add(keras.layers.Dense(10, activation='softmax', name='OutputLayer'))

    # load weights into new model
    model.load_weights(weights)
    return model