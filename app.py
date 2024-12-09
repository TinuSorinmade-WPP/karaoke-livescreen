from flask import Flask, render_template, request, redirect, url_for
from karaoke import download_link, chat_gpt_fact, transcribe_to_json, split_track

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        artist_name = request.form.get('artist', '').strip()
        song_name = request.form.get('song', '').strip()

        if not artist_name or not song_name:
            return render_template('index.html', error="Both artist and song are required.")

        # Generate the fact and download the song
        downloaded_song_path = download_link(artist_name, song_name)
        fact = chat_gpt_fact(downloaded_song_path)

        # Redirect to fact page with parameters
        return redirect(url_for('fact', fact=fact, downloaded_song_path=downloaded_song_path))

    return render_template('index.html')

@app.route('/fact', methods=['GET', 'POST'])
def fact():
    # Get parameters from URL for GET requests
    fact = request.args.get('fact')
    downloaded_song_path = request.args.get('downloaded_song_path')

    if request.method == 'POST':
        # Get parameters from form for POST requests
        downloaded_song_path = request.form.get('downloaded_song_path')
        fact = request.form.get('fact')

        if not downloaded_song_path or not fact:
            return redirect(url_for('index'))

        try:
            # Process the song
            transcribed_lyrics = transcribe_to_json(downloaded_song_path)
            stemmed_track = split_track(downloaded_song_path)

            if not transcribed_lyrics or not stemmed_track:
                error = "Processing failed. Try again."
                return render_template('fact.html', 
                                       fact=fact, 
                                       downloaded_song_path=downloaded_song_path, 
                                       error=error)

            # Redirect to lyrics page with all necessary data
            return redirect(url_for('lyrics', 
                                    transcribed_lyrics=transcribed_lyrics,
                                    stemmed_track=stemmed_track))

        except Exception as e:
            return render_template('fact.html', 
                                   fact=fact, 
                                   downloaded_song_path=downloaded_song_path, 
                                   error=str(e))

    # For GET requests, if parameters are missing, redirect to index
    if not fact or not downloaded_song_path:
        return redirect(url_for('index'))

    return render_template('fact.html', fact=fact, downloaded_song_path=downloaded_song_path)

@app.route('/lyrics', methods=['GET'])
def lyrics():
    transcribed_lyrics = request.args.get('transcribed_lyrics')
    stemmed_track = request.args.get('stemmed_track')

    if not transcribed_lyrics or not stemmed_track:
        return redirect(url_for('index'))

    return render_template('lyrics.html', 
                           lyrics=transcribed_lyrics, 
                           stems=stemmed_track)

if __name__ == "__main__":
    app.run(debug=True)
