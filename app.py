import os
import cv2
import numpy as np
import mediapipe as mp
from flask import Flask, request, jsonify, render_template, Response
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from werkzeug.utils import secure_filename

# ---------------- CONFIG ---------------- #

DATA_DIR = "data/"
IMG_SIZE = 224
MODEL_PATH = "modelnet_model.h5"
UPLOAD_FOLDER = "uploads"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

LABELS = sorted(os.listdir(DATA_DIR))

# ---------------- MEDIAPIPE ---------------- #

mp_hands = mp.solutions.hands

hands_detector = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,   # 🔥 increased
    min_tracking_confidence=0.7     # 🔥 increased
)

# ---------------- MODEL ---------------- #

def build_model():

    base_model = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )

    for layer in base_model.layers:
        layer.trainable = False

    x = base_model.output
    x = Flatten()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.5)(x)
    output = Dense(len(LABELS), activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=output)

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model


def train_model():

    datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2,
        rotation_range=20,
        zoom_range=0.2,
        horizontal_flip=True,
        brightness_range=[0.5, 1.5]
    )

    train_gen = datagen.flow_from_directory(
        DATA_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=32,
        class_mode='categorical',
        subset='training'
    )

    val_gen = datagen.flow_from_directory(
        DATA_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=32,
        class_mode='categorical',
        subset='validation'
    )

    model = build_model()

    model.fit(
        train_gen,
        epochs=40,   # 🔥 increased
        validation_data=val_gen
    )

    model.save(MODEL_PATH)

    return model


# Load or train
if os.path.exists(MODEL_PATH):
    model = load_model(MODEL_PATH)
    print("✅ Model loaded")
else:
    print("⚡ Training model...")
    model = train_model()


# ---------------- PREPROCESS ---------------- #

def preprocess_frame(frame):

    img = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)

    return img


# ---------------- PREDICTION ---------------- #

def predict_frame(frame):

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands_detector.process(img_rgb)

    if not results.multi_hand_landmarks:
        return frame, "No Hand Detected", 0.0

    h, w, _ = frame.shape

    for hand_landmarks in results.multi_hand_landmarks:

        x_coords = [lm.x * w for lm in hand_landmarks.landmark]
        y_coords = [lm.y * h for lm in hand_landmarks.landmark]

        padding = 40  # 🔥 improved crop

        x_min = max(0, int(min(x_coords)) - padding)
        x_max = min(w, int(max(x_coords)) + padding)
        y_min = max(0, int(min(y_coords)) - padding)
        y_max = min(h, int(max(y_coords)) + padding)

        cropped = frame[y_min:y_max, x_min:x_max]

        if cropped.size == 0:
            return frame, "No Hand Detected", 0.0

        processed = preprocess_frame(cropped)

        preds = model.predict(processed, verbose=0)

        class_index = np.argmax(preds)
        confidence = float(np.max(preds))
        label = LABELS[class_index]

        # Draw box
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0,255,0), 2)
        cv2.putText(frame, f"{label} ({confidence:.2f})",
                    (x_min, y_min-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0,255,0), 2)

        return frame, label, confidence

    return frame, "No Hand Detected", 0.0


# ---------------- ROUTES ---------------- #

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict_image", methods=["POST"])
def predict_image():

    file = request.files["file"]

    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    _, label, conf = predict_frame(img)

    return jsonify({
        "prediction": label,
        "confidence": conf
    })


@app.route("/predict_video", methods=["POST"])
def predict_video():

    file = request.files["file"]

    filename = secure_filename(file.filename)
    video_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(video_path)

    cap = cv2.VideoCapture(video_path)
    sequence = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        _, label, _ = predict_frame(frame)

        if label != "No Hand Detected":
            sequence.append(label)

    cap.release()

    return jsonify({"prediction": " ".join(sequence)})


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(debug=True)