// Get DOM elements
const lyricsContainer = document.getElementById('lyrics');
const vocalsAudio = document.getElementById('vocals');
const instrumentalAudio = document.getElementById('instrumental');

// Debug logging for audio elements
console.log("Vocals audio source:", vocalsAudio.src);
console.log("Instrumental audio source:", instrumentalAudio.src);

// Initialize variables
let currentIndex = 0;
let startTime = null;
let intervalId = null;

// Set initial volumes
vocalsAudio.volume = 0.2;  // 20% volume for vocals
instrumentalAudio.volume = 1.0;  // 100% volume for instrumental

// Function to start displaying lyrics and playing audio
function startLyrics() {
if (!intervalId) {
    console.log("Starting playback...");
    // Reset and start audio playback
    vocalsAudio.currentTime = 0;
    instrumentalAudio.currentTime = 0;
    
    Promise.all([
        vocalsAudio.play().catch(e => {
            console.error("Error playing vocals:", e);
            console.log("Vocals src:", vocalsAudio.src);
        }),
        instrumentalAudio.play().catch(e => {
            console.error("Error playing instrumental:", e);
            console.log("Instrumental src:", instrumentalAudio.src);
        })
    ]).then(() => {
        console.log("Audio playback started successfully");
        startTime = Date.now() / 1000;
        currentIndex = 0;
        intervalId = setInterval(displayLyrics, 100);
        lyricsContainer.textContent = "Starting...";
    }).catch(error => {
        console.error("Error playing audio:", error);
        lyricsContainer.textContent = "Error playing audio";
    });
}
}

// Function to reset lyrics and audio
function resetLyrics() {
if (intervalId) {
    clearInterval(intervalId);
    intervalId = null;
}
// Stop and reset audio
vocalsAudio.pause();
instrumentalAudio.pause();
vocalsAudio.currentTime = 0;
instrumentalAudio.currentTime = 0;

currentIndex = 0;
lyricsContainer.textContent = "Click Start to begin...";
}

// Function to display lyrics
function displayLyrics() {
const currentTime = (Date.now() / 1000) - startTime;

if (currentIndex < songData.length) {
    const currentSegment = songData[currentIndex];
    
    if (currentTime >= currentSegment.start && currentTime <= currentSegment.end) {
        lyricsContainer.textContent = currentSegment.text;
    } else if (currentTime > currentSegment.end) {
        currentIndex++;
        if (currentIndex >= songData.length) {
            clearInterval(intervalId);
            intervalId = null;
            lyricsContainer.textContent = "End of lyrics";
            vocalsAudio.pause();
            instrumentalAudio.pause();
        }
    }
}
}

// Add audio loading event listeners
vocalsAudio.addEventListener('loadeddata', () => {
console.log("Vocals loaded successfully");
});

instrumentalAudio.addEventListener('loadeddata', () => {
console.log("Instrumental loaded successfully");
});

// Add error listeners
vocalsAudio.addEventListener('error', (e) => {
console.error("Vocals error:", e);
});

instrumentalAudio.addEventListener('error', (e) => {
console.error("Instrumental error:", e);
});

// Error handling for when no lyrics are available
if (!songData || songData.length === 0) {
lyricsContainer.textContent = "No lyrics available";
}