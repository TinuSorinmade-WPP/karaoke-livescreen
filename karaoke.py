##############################
# Import Relevant Libraries  #
##############################

import webbrowser  # To open web pages in the default browser
import json  # To parse JSON data (if needed for API interactions or responses)
# For interacting with the operating system (file management and system commands)
import os  # Provides functions to interact with the operating system (e.g., file paths, directories)
import subprocess  # For running system commands (e.g., executing external programs)
# YOUTUBE VIDEO SEARCH 
from youtube_search import YoutubeSearch  # To search YouTube for videos based on a query and retrieve results (Video ID)
# For downloading YouTube audio and handling download progress
import pytubefix
from pytubefix import YouTube  # To download YouTube videos (specifically audio) using pytubefix
from pytubefix.cli import on_progress  # To handle the progress callback during video downloads
# AUDIO SEPERATION
import demucs  # To separate audio tracks into different stems (e.g., vocals, instrumental)
import torch
# LYRIC TRANSCRIPTION
import whisper
# PLAYING THE MUSIC 
import time
import pygame # For the Music Playack 
import flask_socketio
from flask_socketio import SocketIO
# Importing ChatGPT elements
from openai import AzureOpenAI
# Parsing the Chatgpt response
import urllib.parse
from flask import Flask, render_template, redirect, url_for

##########################################
# Download the Youtube Video Information #
##########################################

def download_link(artist, track):
    # Retrieve the song title and artist information from the 'get_song_artist' function
    song_artist = artist
    song_title = track  # Get the song and artist information to search on YouTube
    title= f"{artist}+{track}"
    # Use YoutubeSearch to search for the song on YouTube, limiting the results to 1
    results = YoutubeSearch(title, max_results=1).to_dict()  # Get the top result as a dictionary
    # Loop through the search results to extract the YouTube video link
    for v in results:
        # Construct the full YouTube URL using the video ID from the search results
        link = 'https://www.youtube.com/watch?v=' + v['id']
    # Ensure the 'Audio_Downloads' directory exists to store the downloaded audio files
    if not os.path.exists('Audio_Downloads'):
        os.makedirs('Audio_Downloads')  # Create the 'Audio_Downloads' folder if it doesn't exist
    # Call the youtube_link function to get the YouTube URL for the video
    # Initialise the YouTube object and set up the on-progress callback for download tracking
    yt = YouTube(link, on_progress_callback=on_progress)
    # Get the audio stream from the YouTube video
    ys = yt.streams.get_audio_only()  # Extract only the audio from the video
    # Download the audio to the 'Audio_Downloads' directory and get the full file path
    audio_path = ys.download(output_path='Audio_Downloads')  # Downloads and returns the full audio file path
    # Rename the downloaded file to have a '.mp3' extension instead of the default format
    base, ext = os.path.splitext(audio_path)  # Split the file into base name and extension
    new_file = base + '.mp3'  # Change the file extension to '.mp3'
    # Rename the audio file to the new .mp3 format
    os.rename(audio_path, new_file)  # Rename the file to the new format
    # Return the full path to the renamed audio file
    return new_file  # The renamed .mp3 file path is returned 


######################################
# Get Lyrics and Timings of the song #
######################################

def transcribe_to_json(audiofile_path: str, num_passes: int = 1) -> str:
    audio_path_file_name = audiofile_path.replace('\\',',' )
    audio_path_file_name_ending = audio_path_file_name.split(",")[-1]
    output_filename = f"{audio_path_file_name_ending} - Lyrical Timing.json"
    try:
        json_path = os.path.join(  # The file will be saved in the 'subtitles' directory with the same base name as the audio file
            os.getcwd(),  # Use the current working directory
            "Lyrical Timings",  # Fixed directory for output
            output_filename # Custom or default file name
        )
        print("Output JSON path:", json_path)

        # Create the directory if it doesn't already exist
        if not os.path.exists(os.path.dirname(json_path)):
            os.makedirs(os.path.dirname(json_path))

        # Load the Whisper model for transcription
        # Determine if a CUDA-enabled GPU is available; otherwise, use the CPU
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model = whisper.load_model("large-v2").to(device)

        last_result = None  # Initialise a variable to store the final transcription result
        for i in range(num_passes):
            # Perform transcription multiple times if specified (useful for improving accuracy)
            print(f"Transcription pass {i + 1} of {num_passes}...")
            current_result = model.transcribe(
                audiofile_path,  # Path to the audio file to be transcribed
                verbose=True,    # Display detailed output during transcription
                language="en",   # Specify the language for transcription
                word_timestamps=True  # Include timestamps for each word in the transcription
            )
            last_result = current_result  # Update the last result with the current transcription

        # Check if any transcription result was obtained
        if last_result is None:
            raise ValueError("No transcription results obtained.")

        # Process transcription data into a list of segments
        # Each segment includes the start time, end time, and text
        karaoke_data = []
        for segment in last_result['segments']:
            karaoke_data.append({
                "start": segment['start'],  # Start time of the segment in seconds
                "end": segment['end'],      # End time of the segment in seconds
                "text": segment['text']     # Transcribed text for the segment
            })
        
        print("Processed transcription data:", karaoke_data)

        # Save the processed transcription data to a JSON file
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(karaoke_data, json_file, indent=4)  # Write JSON data with indentation for readability
            print("Transcription saved successfully.")  # Confirm successful save

        return json_path  # Return the path to the saved JSON file

    except Exception as e:
        # Handle any errors that occur during the process
        print(f"Error transcribing audio to JSON: {e}")
        return ""  # Return an empty string in case of an error

#################################################
# Split the Tracks into vocals and instrumental #
#################################################

def split_track(audiofile_path):
    # Ensure FFmpeg is installed and accessible on the system by checking its version
    os.system("ffmpeg -version")
    # The original audio file path
    song_path = audiofile_path
    # Replace the file extension from 'm4a' to 'mp3' to convert the downloaded file format
    path = song_path.replace('m4a', 'mp3')
    # Extract the file name from the file path (after the last backslash)
    file_title = os.path.basename(path).replace('.mp3', '')
    # Mian output
    output ="output"
    # Define the output directory for Demucs by combining "output" and "htdemucs"
    output_dir = os.path.join("output", "htdemucs")
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    # Construct the Demucs command to isolate vocals and instrumental stems
    command = f"demucs --mp3 --two-stems=vocals -o {output} \"{song_path}\""
    # Execute the Demucs command to process the audio and generate the separated stems
    os.system(command)
    # Get Current working directory
    wd = os.getcwd()
    # Get the paths of the output files generated by Demucs
    vocals_file = os.path.join(wd,output_dir, file_title, "vocals.mp3")
    instrumental_file = os.path.join(wd,output_dir, file_title, "no_vocals.mp3")
    # Return the original audio file path and the paths of the output files
    return vocals_file, instrumental_file



#######################################################
# Generate Random Facts about the artist and the song #
#######################################################
# Function to generate a music fact about the song from the audio file path
def chat_gpt_fact(audiofile_path): 

    # Initialise the AzureOpenAI client with API key, endpoint, and version details
    client = AzureOpenAI(
        api_key = os.getenv("AZURE_KEY"),  # Get the Azure API key from environment variables
        azure_endpoint = os.getenv("AZURE_ENDPOINT"),  # Get the Azure endpoint from environment variables
        api_version = "2023-10-01-preview"  # Set the specific API version
    )
    # Replace backslashes in the file path with commas for easier parsing
    new_path = audiofile_path.replace("\\", ',')
    # Extract the song title by splitting the modified path and taking the last element
    chatgpt_song_title = new_path.split(",")[-1]
    
    # Define the messages to send to the GPT model
    messages = [
        {"role": "system", "content": f"Generate a music fact about this song or any of the artists who made this song: {chatgpt_song_title}. Make sure there is a '/' between each fact and that the output is maximum 50 words!"},  # System message with context
        {"role": "user", "content": f"Please generate a fact about this song or any of the artists who made this song: {chatgpt_song_title}"}  # User's request for a music fact
    ]
    # Make the API call to Azure OpenAI to generate the completion (fact about the song)
    response = client.chat.completions.create(
        model="GPT-4",  # Use the GPT-4 model for generating the response
        messages=messages  # Provide the messages for the model
    )
    # Extract the generated fact from the response, specifically from the first choice's 'message' field
    music_fact = response.choices[0].message.content
    # Clean the fact by removing unnecessary newline characters (if any) to make it more readable
    encoded_fact = music_fact.replace("\n\n", "")    
    # Return the cleaned-up music fact (URL-encoded if necessary, but here it's just a string)
    return encoded_fact  # Return the final music fact


######################
# Read the JSON 1 file #
######################

def read_json_file(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"JSON file not found: {file_path}")
    try:
        # Open and load the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Validate the data structure
        if not isinstance(data, list):
            raise ValueError("JSON data must be a list")
        
        # Validate that each item contains the required fields
        for item in data:
            if not all(key in item for key in ['start', 'end', 'text']):
                raise ValueError("Each item must have 'start', 'end', and 'text' fields")
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")
    except Exception as e:
        raise Exception(f"Error reading JSON file: {e}")
    

######################
# Read the JSON file #
######################
def read_the_file(json_path): 
    # Assuming `transcribed_lyrics` contains the path to the JSON file.
    json_file_path = json_path
    # Read the JSON file.
    with open(json_file_path, 'r', encoding='utf-8') as file:
        lyrics_data = json.load(file)
    # Display the content of the JSON file.
    print(lyrics_data)