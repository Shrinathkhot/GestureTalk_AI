let useWebcam = false;
let sentence = "";
let lastLetter = "";
let lastAddedTime = 0;
let stableCount = 0;
let lastStableLetter = "";

// Elements
const uploadTab = document.getElementById("uploadTab");
const liveTab = document.getElementById("liveTab");
const uploadSection = document.getElementById("uploadSection");
const liveSection = document.getElementById("liveSection");

const dropZone = document.getElementById("dropZone");
const mediaUpload = document.getElementById("mediaUpload");

const preview = document.getElementById("preview");
const webcam = document.getElementById("webcam");

const predictBtn = document.getElementById("predictBtn");
const loader = document.getElementById("loader");

const resultBox = document.getElementById("result");
const confidenceBox = document.getElementById("confidence");
const historyList = document.getElementById("historyList");

// ---------------- TAB SWITCH ---------------- //

uploadTab.onclick = () => {
    useWebcam = false;
    uploadSection.classList.remove("hidden");
    liveSection.classList.add("hidden");
    uploadTab.classList.add("active");
    liveTab.classList.remove("active");
};

liveTab.onclick = () => {
    useWebcam = true;
    uploadSection.classList.add("hidden");
    liveSection.classList.remove("hidden");
    liveTab.classList.add("active");
    uploadTab.classList.remove("active");
    startWebcam();
};

// ---------------- FILE UPLOAD ---------------- //

dropZone.onclick = () => mediaUpload.click();

mediaUpload.onchange = function () {
    handleMedia(this.files[0]);
};

function handleMedia(file) {
    if (!file) return;

    preview.innerHTML = "";
    let url = URL.createObjectURL(file);

    if (file.type.startsWith("image")) {
        let img = document.createElement("img");
        img.src = url;
        preview.appendChild(img);
    } else if (file.type.startsWith("video")) {
        let video = document.createElement("video");
        video.src = url;
        video.controls = true;
        preview.appendChild(video);
    }
}

// ---------------- WEBCAM ---------------- //

async function startWebcam() {
    let stream = await navigator.mediaDevices.getUserMedia({ video: true });
    webcam.srcObject = stream;
}

// ---------------- PREDICT BUTTON ---------------- //

predictBtn.onclick = async () => {

    loader.classList.remove("hidden");

    if (useWebcam) {
        startLivePrediction();
        loader.classList.add("hidden");
        return;
    }

    const file = mediaUpload.files[0];

    if (!file) {
        alert("Upload a file first");
        loader.classList.add("hidden");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    let endpoint = file.type.startsWith("image") ? "/predict_image" : "/predict_video";

    const response = await fetch(endpoint, {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    updatePrediction(data.prediction, data.confidence);

    loader.classList.add("hidden");
};

// ---------------- CORE LOGIC (FINAL 🔥) ---------------- //

function updatePrediction(text, confidence) {

    // ✅ 1. Confidence filter (40%)
    if (confidence && confidence < 0.4) return;

    // Ignore no hand
    if (text === "No Hand Detected") return;

    let currentTime = Date.now();

    // ✅ 2. Stability check (same letter 2 times)
    if (text === lastStableLetter) {
        stableCount++;
    } else {
        stableCount = 1;
        lastStableLetter = text;
    }

    if (stableCount < 2) return;

    // ✅ 3. Throttle (prevent spam)
    if (currentTime - lastAddedTime < 600) return;

    lastAddedTime = currentTime;

    // ✅ 4. Add letter (controlled repeat)
    sentence += text;
    lastLetter = text;

    addHistory(text);

    resultBox.innerText = sentence;

    if (confidence) {
        confidenceBox.innerText = "Confidence: " + (confidence * 100).toFixed(2) + "%";
    }
}

// ---------------- HISTORY ---------------- //

function addHistory(letter) {
    let li = document.createElement("li");
    li.innerText = letter;
    historyList.appendChild(li);
}

// ---------------- LIVE PREDICTION ---------------- //

function startLivePrediction() {

    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");

    setInterval(async () => {

        if (!useWebcam) return;

        canvas.width = webcam.videoWidth;
        canvas.height = webcam.videoHeight;

        ctx.drawImage(webcam, 0, 0);

        const blob = await new Promise(resolve =>
            canvas.toBlob(resolve, "image/jpeg")
        );

        const formData = new FormData();
        formData.append("file", blob, "frame.jpg");

        const response = await fetch("/predict_image", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        updatePrediction(result.prediction, result.confidence);

    }, 400); // 🔥 faster + smooth
}

// ---------------- SPEAK ---------------- //

function speakText() {
    const speech = new SpeechSynthesisUtterance(sentence);
    speech.lang = "en-US";
    window.speechSynthesis.speak(speech);
}

// ---------------- RESET ---------------- //

function resetText() {
    sentence = "";
    lastLetter = "";
    stableCount = 0;
    lastStableLetter = "";

    resultBox.innerText = "---";
    historyList.innerHTML = "";
    confidenceBox.innerText = "Confidence: --";
}