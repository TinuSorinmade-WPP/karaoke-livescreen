class GifTV {
    constructor() {
        // Initialise essential DOM elements by retrieving them using their IDs
        this.gifVideo = document.getElementById('loading-screen'); // The loading GIF element that is initially displayed
        this.karokeForm = document.getElementById('main-tv-screen'); // The karaoke form that will be displayed after the GIF
        this.pixels = document.getElementById('tv_pixels'); // The pixelated overlay on the TV screen

        // Define the static URLs for the GIF and the sound that will be played during the experience
        this.staticGIF = 'https://res.cloudinary.com/cyborgspaceviking/image/upload/v1571155222/giphy_n0r827.gif';
        this.staticSound = 'https://freesound.org/data/previews/41/41029_410502-lq.mp3';
    }
        
    // To play sound
    playSound(volume) {
        try {
            // Create a new Audio object with the defined sound URL
            const sound = new Audio(this.staticSound);
            sound.volume = volume; // Set the volume of the sound
            sound.play().catch(err => console.log('Error playing sound:', err)); // Play the sound and catch any potential errors
        } catch (err) {
            console.log('Sound error:', err); // Log any error that occurs during sound playback
        }
    }
    
    // To handle form submission
    handleFormSubmit() {
        // Play the sound at a lower volume when the form is submitted
        this.playSound(0.3);
    }
    
    // To initialise the GifTV experience
    init() {
        // Set the initial display state of the GIF and karaoke form
        this.gifVideo.style.display = 'block'; // Show the GIF initially
        this.karokeForm.style.display = 'none'; // Hide the karaoke form initially
    
        // After 3 seconds, switch from the GIF video to the karaoke form
        setTimeout(() => {
            this.gifVideo.style.display = 'none'; // Hide the GIF video
            this.karokeForm.style.display = 'flex'; // Show the karaoke form
            this.playSound(0.2); // Play the sound at a lower volume when switching to the karaoke form
        }, 3000);
    
        // Add an event listener to the karaoke form for when it is submitted
        if (this.karokeForm) {
            this.karokeForm.addEventListener('submit', () => this.handleFormSubmit());
        }
    }
}

// Initialise the TV class when the DOM content is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    const gifTV = new GifTV(); // Create a new instance of GifTV
    gifTV.init(); // Initialise the GifTV experience
});
