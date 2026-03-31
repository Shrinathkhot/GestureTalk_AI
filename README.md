# GestureTalk AI
A Smart Sign Language Recognition System Using Computer Vision

---

## Project Description
GestureTalk AI is an AI-powered web application that detects sign language hand gestures and converts them into text in real time using Computer Vision and Deep Learning.

The system helps reduce the communication gap between hearing-impaired individuals and others by providing an intelligent and interactive solution.

---

## Features
- Real-time hand gesture recognition  
- Image upload for gesture prediction  
- Video upload for gesture detection  
- Live webcam gesture recognition  
- Displays detected text output  
- Shows prediction confidence score  
- Converts gestures into sentences  
- Optional Text-to-Speech functionality  

---

## Technologies Used

| Technology | Purpose |
|-----------|--------|
| Python | Backend development |
| Flask | Web application framework |
| TensorFlow / Keras | Deep learning model |
| OpenCV | Image processing |
| MediaPipe | Hand detection |
| NumPy | Numerical computations |
| HTML | Webpage structure |
| CSS | User interface design |
| JavaScript | Frontend interaction |
| Docker | Containerized deployment |

---

## System Architecture

User Input (Image / Video / Webcam)  
↓  
Hand Detection (MediaPipe)  
↓  
Image Preprocessing  
↓  
CNN Deep Learning Model  
↓  
Gesture Classification  
↓  
Text Output  
↓  
Speech Output (Optional)  

---

## Project Structure


GestureTalk_AI/
│
├── app.py
├── README.md
│
├── static/
│ ├── script.js
│ └── style.css
│
├── templates/
│ └── index.html
│
├── data/
│
└── uploads/


---

## Dataset
The dataset is not included in this repository due to file size limitations.

After downloading the dataset, place it inside the project folder as shown below:


GestureTalk_AI/
│
├── data/
│ ├── A/
│ ├── B/
│ ├── C/
│ └── ...


Each folder represents a gesture class used for training.

---

## Model File (modelnet_model.h5)
The trained model file is not included in this repository.

When the application runs:
- If the model file exists → it will be loaded  
- If it does not exist → the system will train a new model automatically  

The trained model will be saved as:

modelnet_model.h5


---

## Installation and Setup

### Step 1: Clone the Repository

git clone https://github.com/YOUR_USERNAME/GestureTalk_AI.git

cd GestureTalk_AI


### Step 2: Create Virtual Environment

python -m venv venv


### Step 3: Activate Virtual Environment

Windows:

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate


### Step 4: Install Dependencies

pip install -r requirements.txt


---

## Run the Application

python app.py


Open your browser and go to:

http://127.0.0.1:5000


---

## Usage

### Upload Mode
Upload an image or video containing sign language gestures.

### Live Webcam Mode
Use your webcam to perform gestures and receive real-time predictions.

The system will detect gestures and convert them into text.

---

## Future Improvements
- Support for full sign language vocabulary  
- Improved model accuracy with larger datasets  
- Mobile application integration  
- Real-time sentence prediction using NLP  
- Multilingual speech output  

---

## Author
Shrinath Khot  
B.Tech Computer Engineering  
Aspiring Data Scientist  

---

## Conclusion
GestureTalk AI demonstrates the application of Artificial Intelligence and Computer Vision in building assistive technologies. It provides an effective approach for real-time sign language recognition.
