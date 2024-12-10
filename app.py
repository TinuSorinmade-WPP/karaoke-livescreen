from flask import Flask, render_template, request, redirect, url_for, send_file
from pathlib import Path
import os
from karaoke import *

# Initialising the Flask application
app = Flask(__name__)

# This is the main route of the application
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the artist and song name from the form
        artist_name = request.form.get('artist', '').strip()
        song_name = request.form.get('song', '').strip()

        # If either field is empty, reload the page with an error
        if not artist_name or not song_name:
            return render_template('index.html', error="Both artist and song are required.")

        # Try to download the song and generate a fact about it
        downloaded_song_path = download_link(artist_name, song_name)
        fact = chat_gpt_fact(downloaded_song_path)

        # Redirect to the page where the fact is displayed
        return redirect(url_for('fact', fact=fact, downloaded_song_path=downloaded_song_path))

    # If it's a GET request, just show the index page
    return render_template('index.html')

# Route to show the fact about the song
@app.route('/fact', methods=['GET', 'POST'])
def fact():
    fact = request.args.get('fact')
    downloaded_song_path = request.args.get('downloaded_song_path')

    if request.method == 'POST':
        # Handle form submission for further processing
        downloaded_song_path = request.form.get('downloaded_song_path')
        fact = request.form.get('fact')

        # Redirect back to the home page if data is missing
        if not downloaded_song_path or not fact:
            return redirect(url_for('index'))

        try:
            # Try to process the song
            transcribed_lyrics = transcribe_to_json(downloaded_song_path)
            vocals_path, instrumental_path = split_track(downloaded_song_path)

            # If anything goes wrong, show an error message
            if not transcribed_lyrics or not vocals_path or not instrumental_path:
                error = "Processing failed. Try again."
                return render_template(
                    'fact.html', 
                    fact=fact, 
                    downloaded_song_path=downloaded_song_path, 
                    error=error
                )

            # Redirect to the lyrics page if everything worked
            return redirect(url_for(
                'lyrics', 
                transcribed_lyrics=transcribed_lyrics,
                vocals_path=vocals_path,
                instrumental_path=instrumental_path
            ))

        except Exception as e:
            # Log the exception and show it on the page
            return render_template(
                'fact.html', fact=fact, downloaded_song_path=downloaded_song_path, error=str(e))

    # Redirect to the index page if no data is provided
    if not fact or not downloaded_song_path:
        return redirect(url_for('index'))

    # Show the fact page if everything is okay
    return render_template('fact.html', fact=fact, downloaded_song_path=downloaded_song_path)

# Route to display the song's lyrics
@app.route('/lyrics', methods=['GET'])
def lyrics():
    transcribed_lyrics = request.args.get('transcribed_lyrics')
    vocals_path = request.args.get('vocals_path')
    instrumental_path = request.args.get('instrumental_path')

    # Redirect to home if any data is missing
    if not all([transcribed_lyrics, vocals_path, instrumental_path]):
        return redirect(url_for('index'))

    try:
        # Try reading the transcribed lyrics from the JSON file
        song_data = read_json_file(transcribed_lyrics)
        
        # Ensure paths are absolute (not sure why we need this, but seems safer?)
        vocals_path = str(Path(vocals_path).absolute())
        instrumental_path = str(Path(instrumental_path).absolute())
        
        # Render the lyrics page with the song's data and audio paths
        return render_template(
            'lyrics.html', 
            song_data=song_data,
            vocals_path=f"/audio/{vocals_path}",
            instrumental_path=f"/audio/{instrumental_path}"
        )

    except Exception as e:
        # If something goes wrong, log it and show an error on the page
        print(f"Error: {e}")
        return render_template('lyrics.html', song_data=[], error=str(e))

# Route to serve audio files (for streaming or download)
@app.route('/audio/<path:filename>')
def serve_audio(filename):
    try:
        audio_path = Path(filename).resolve()
        
        # Check if the file actually exists
        if not audio_path.exists():
            return f"Audio file not found: {filename}", 404
            
        # Send the audio file back 
        return send_file(str(audio_path), mimetype='audio/mpeg')
    except Exception as e:
        # Handle any errors that might occur
        print(f"Error serving audio: {e}")
        return f"Error serving audio file: {str(e)}", 404

# Run the Flask app in debug mode
if __name__ == "__main__":
    app.run(debug=True)
