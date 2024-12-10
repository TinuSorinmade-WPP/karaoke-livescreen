# Web Karaoke Application

## Description

A web-based karaoke application that allows users to search for songs, split them into vocal and instrumental tracks, display synchronised lyrics, and provide an interactive karaoke experience. The application uses AI-powered audio separation and speech-to-text technology to create a complete karaoke system.

## Features

- Song search and download functionality
- AI-powered track separation (vocals and instrumental)
- Synchronised lyrics display
- Adjustable volume controls for vocals and instrumental tracks
- Interactive TV-style interface
- Song fact generation using ChatGPT (open AI) API
- Real-time lyrics synchronisation

## Technical Stack

- **Backend**: Python/Flask
- **Frontend**: HTML, CSS, JavaScript
- **Audio Processing**:
  - Demucs (for track separation)
  - FFmpeg (for audio conversion)
- **AI Integration**:
  - OpenAI's ChatGPT (for fact generation)
  - Speech-to-text (for lyrics transcription)

## Prerequisites

```bash
# Required Python packages
Flask
demucs
ffmpeg-python
openai
# (other dependencies as specified in requirements.txt)
```

## Installation

1. Clone the repository

```bash
git clone [repository-url]
cd web-karaoke
```

2. Create a virtual environment and Install dependencies

```bash
mkdir [Name of the File]
cd file
virtualenv venv 
venv\scripts\activate
pip install -r requirements.txt
```

3. Set up environment variables (for Open-AI)

```bash
set AZURE_KEY={Your Azure Key} 
echo %AZURE_KEY% # to check it saved properly
set AZURE_ENDPOINT={Your Azure Endpoint}
echo %AZURE_ENDPOINT% # to check it saved properly
```



## Key Components

- **Song Processing**: Uses Demucs to separate vocals from instrumental tracks

  

- **Lyrics Synchronisation**: Matches transcribed lyrics with audio timing

  

- **Audio Control**: Independent volume control for vocals and instrumental tracks!

  

- **Interactive Interface**: Retro TV-style design with start/reset controls - as well as a fun fact to keep the user engaged whilst the karaoke set up is underway!

## Features in Detail

1. **Song Search & Download**

- User inputs artist and song name
- System downloads the song and generates an interesting fact

2. **Track Separation**

- Splits original song into vocal and instrumental tracks
- Processes audio files for optimal karaoke experience

3. **Lyrics Display**

- Shows synchronised lyrics
- Highlights current line being sung
- Adjustable audio mixing