import streamlit as st
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
import numpy as np
import cv2
from keras.applications import DenseNet121
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense
from keras.optimizers import Adam

# Load the saved model
new_width = 64
new_height = 64
base_model = DenseNet121(weights='imagenet', include_top=False, input_shape=(new_width, new_height, 3))

# Freeze the layers of the pre-trained model
for layer in base_model.layers:
    layer.trainable = False

# Recreate your model by adding the DenseNet121 base model and additional layers
loaded_model = Sequential([
    base_model,
    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(128, activation='relu'),
    Dense(5, activation='softmax')
])

# Compile the loaded model with RMSprop optimizer
loaded_model.compile(optimizer=Adam(lr=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

# Load the saved weights into the model
loaded_model.load_weights('saved_model_weights.h5')

# Streamlit app
st.title("Satellite Image Classification AI Model")

# Add any additional UI elements or instructions as needed
st.sidebar.markdown("## Instructions:")
st.sidebar.markdown("1. Upload an image.")
st.sidebar.markdown("2. Click the 'Predict' button.")

# Image upload
uploaded_file = st.file_uploader("Choose an image...", type="jpg")

classes = ['agriculture clear primary road',
 'clear primary water',
 'cloudy',
 'haze primary',
 'partly_cloudy primary']

def preprocess_image(image):
    # Resize the image to match the model's expected input size
    image = cv2.resize(image, (64, 64))
    # print(image.shape)
    image = image/255
    image = image.reshape((-1,64,64,3))

    return image

# Function to make predictions
def make_prediction(image):
    preprocessed_image = preprocess_image(image)
    prediction = loaded_model.predict(preprocessed_image)
    print("predictions: ", prediction)
    rounded_prediction = np.round(prediction, 3)
    print("rounded: ", rounded_prediction)
    
    return classes[np.argmax(rounded_prediction)]

if uploaded_file is not None:
    image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
    st.image(image, channels="BGR", caption="Uploaded Image", use_column_width=True)
    prediction_button = st.button("Get Prediction")

    if prediction_button:
        prediction = make_prediction(image)
        st.write("Prediction:", prediction)
        


