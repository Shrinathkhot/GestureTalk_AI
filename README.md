# GestureTalk AI
A Smart Sign Language Recognition System using Computer Vision and Deep Learning

---

## Project Overview
GestureTalk AI is a real-time sign language recognition system that converts hand gestures into text and speech. The system uses MediaPipe for hand detection and a MobileNetV2 deep learning model for gesture classification.

The goal of this project is to reduce the communication gap between hearing-impaired individuals and others by providing an efficient and intelligent solution.

---

## Features
- Real-time hand gesture recognition using webcam  
- Image and video-based prediction  
- Confidence-based filtering for improved accuracy  
- Smooth and stable predictions  
- Text generation from gestures  
- Speech output for detected text  

---

## Tech Stack
- Frontend: HTML, CSS, JavaScript  
- Backend: Flask (Python)  
- Machine Learning: TensorFlow, Keras  
- Computer Vision: OpenCV, MediaPipe  
- Model: MobileNetV2 (Transfer Learning)  

---

## Project Structure
GestureTalk_AI/
│── app.py
│── templates/
│── static/
│── data/
│── requirements.txt
│── README.md

---

## Installation and Setup

### Step 1: Clone the Repository

git clone https://github.com/YOUR-USERNAME/GestureTalk_AI.git

cd GestureTalk_AI

### Step 2: Create Virtual Environment

pip install -r requirements.txt

---

## How to Run the Project

python app.py

Open your browser and go to:

http://127.0.0.1:5000

---

## Usage

### Live Webcam Mode
- Click on "Live Webcam"  
- Click on "Translate"  
- Show hand gestures clearly  

### Upload Mode
- Upload an image or video  
- View predicted output  

---

## Model Details
- Pretrained Model: MobileNetV2  
- Input Size: 224 × 224  
- Optimizer: Adam  
- Loss Function: Categorical Crossentropy  
- Dataset: Custom hand gesture dataset  

---

## Limitations
- Accuracy depends on lighting conditions  
- Requires clear hand visibility  
- Similar gestures may reduce accuracy  

---

## Future Improvements
- Automatic word formation from letters  
- Improved accuracy using hand landmarks  
- Multi-hand detection  
- Mobile application deployment  

---

## Author
Shrinath Khot  
Aspiring Data Scientist and Data Analyst  

---

## Conclusion
GestureTalk AI demonstrates the practical use of Artificial Intelligence and Computer Vision in building assistive technologies. It provides an effective approach for real-time sign language recognition.

Next step

After pasting:

git add .
git commit -m "updated README professionally"
git push
