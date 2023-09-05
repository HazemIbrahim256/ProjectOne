// Function to toggle night mode
function toggleNightMode() {
    const body = document.body;
    const nightModeButton = document.getElementById('nightModeButton');

    // Toggle the night mode class on the body
    body.classList.toggle('night-mode');

    // Update the button text based on the current mode
    if (body.classList.contains('night-mode')) {
        // Set the button's HTML to the sun icon
        nightModeButton.innerHTML = '<i class="fas fa-sun"></i>';
    } else {
        // Set the button's HTML to the moon icon
        nightModeButton.innerHTML = '<i class="fas fa-moon"></i>';
    }
}

// Event listener for the button click
const nightModeButton = document.getElementById('nightModeButton');
nightModeButton.addEventListener('click', toggleNightMode);

// Check for initial mode (based on local storage or user preferences)
const storedMode = localStorage.getItem('nightMode');
if (storedMode === 'night') {
    toggleNightMode();
};

// HTML Elements
const startButton = document.getElementById("startButton");
const stopButton = document.getElementById("stopButton");
const pauseButton = document.getElementById("pauseButton");
const audioPlayer = document.getElementById("audioPlayer");
const transcriptTextArea = document.getElementById("transcript");
const sourceLanguageSelect = document.getElementById("sourceLanguage");
const targetLanguageSelect = document.getElementById("targetLanguage");
const translationTextArea = document.getElementById("translation");
const nerOutputText = document.getElementById("ner-output-text");

// Speech Recognition
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.continuous = true;
recognition.interimResults = true;

// State
let isRecording = false;
let isPaused = false ;

// Event Listeners
startButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
pauseButton.addEventListener("click", togglePauseRecording);

function togglePauseRecording() {
    if (isRecording) { // Check if it's currently recording
        if (!isPaused) {
            isPaused = true;
            recognition.stop(); // Pause recognition
            pauseButton.innerText = "Resume";
            pauseButton.classList.add("paused"); // Add the paused class for animation
        } else {
            isPaused = false;
            recognition.start(); // Resume recognition
            pauseButton.innerText = "Pause";
            pauseButton.classList.remove("paused"); // Remove the paused class for animation
        }
    }
}
// Start Recording Function
function startRecording() {
    if (!isRecording) {
        isRecording = true;
        pauseButton.disabled = false;
        startButton.disabled = true;
        stopButton.disabled = false;
        console.log("recording...")

        // Request microphone access
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then((stream) => {
                //audioPlayer.stream = stream;
                recognition.lang = sourceLanguageSelect.value; // Set the source language
                recognition.start();
            })
            .catch((error) => {
                console.error("Microphone access error:", error);
                isRecording = false;
                startButton.disabled = false;
                stopButton.disabled = true;
            });
    }
}

// Stop Recording Function
function stopRecording() {
    if (isRecording) {
        isRecording = false;
        recognition.stop();
        startButton.disabled = false;
        stopButton.disabled = true;
        console.log("stop recotding")
    }
}
sourceLanguageSelect.addEventListener("change", () => {
    recognition.lang = sourceLanguageSelect.value;
});

// Speech Recognition Result
recognition.onresult = (event) => {
    let transcription = "";
    let numSpaces = 1; // Initialize with 1 space for the first line

    for (const result of event.results) {
        if (result.isFinal) {
            const sentence = result[0].transcript;

            // Create a string with the desired number of spaces
            const spaces = ' '.repeat(numSpaces);

            // Add the spaces before the current sentence
            const indentedLine = spaces + sentence;

            // Add the indented line to the transcription
            transcription += indentedLine + '\n';

            // Increment the number of spaces for the next line
            numSpaces++;
        }
    }

    transcriptTextArea.textContent = transcription.trim();

    // Send the transcription to the backend for translation
    const targetLanguage = targetLanguageSelect.value;
    translate(transcription, targetLanguage);
};
function translate(text, target_language) {
    const backendURL = `http://localhost:8000/api/transcribe/${target_language}/`;
    fetch(backendURL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: text }),
    })
        .then((response) => response.json())
        .then((data) => {
            translationTextArea.textContent = data.translation;
            if ('ner_output' in data) {
                // Display NER output in the frontend
                nerOutputText.textContent = data.ner_output.join(', '); // Assumes data.ner_output is a list of NER entities
            } else {
                nerOutputText.textContent = "";
            }
        })
        .catch((error) => {
            console.error("Translation error:", error);
        });
}

//upload file 
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData();
    const fileInput = document.getElementById('audioUpload');
    const file = fileInput.files[0];

    if (file) {
        formData.append('audioFile', file);
        const sourceLanguageValue = document.getElementById('sourceLanguage').value;
        const targetLanguageValue = document.getElementById('targetLanguage').value;
        
        try {
            const response = await fetch(`http://localhost:8000/api/upload/${sourceLanguageValue}/to/${targetLanguageValue}`, {
                method: 'POST',
                headers: {
                    "Content-Type": "multipart/form-data",
                },
                body: formData,
            });

            if (response.ok) {
                // Handle a successful upload
                const responseData = await response.json();
                console.log('File uploaded successfully');
                transcriptTextArea.textContent = responseData.transcription;
                translationTextArea.textContent = responseData.translation;

                // Check if NER output exists in the response
                if ('ner_output' in responseData) {
                    // Display NER output in the frontend
                    nerOutputText.textContent = responseData.ner_output.join(', ');
                } else {
                    nerOutputText.textContent = "";
                }
            } else {
                console.error('File upload failed');
            }
        } catch (error) {
            console.error('Network error:', error);
        }
    }
});
