# Kokoro Text-to-Speech Application

A desktop application that converts text to speech using the Kokoro ONNX model. This application provides a user-friendly interface for generating speech from text with multiple voice options.

## Features

- Clean and intuitive graphical user interface
- Multiple voice options to choose from
- Real-time text-to-speech playback
- Save audio output as WAV files
- Upload and read text from files
- Stop/Play functionality for audio playback

## Prerequisites

- Python 3.x
- Windows OS (for batch scripts)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/NickWeder/KokoroUI.git
cd KokoroUI
```

2. Run the preparation script:
```bash
preparation.bat
```

This script will:
- Download the required `voices.json` file
- Set up a Python virtual environment
- Install necessary dependencies
- Download the Kokoro model from HuggingFace

## Running the Application

After installation, simply run:
```bash
run.bat
```

Or manually:
1. Activate the virtual environment:
```bash
.\.venv\Scripts\activate
```

2. Run the application:
```bash
python UserInterface.py
```

## Dependencies

- `kokoro_onnx`: For text-to-speech conversion
- `sounddevice`: For audio playback
- `soundfile`: For saving audio files
- `tkinter`: For the graphical user interface
- `huggingface_hub`: For downloading model files

## Usage

1. Select a voice from the dropdown menu
2. Enter text directly in the text box or upload a text file
3. Click "Play Voice" to hear the audio
4. Use "Stop Voice" to stop the playback
5. Click "Save Voice" to save the audio as a WAV file

## Project Structure

- `UserInterface.py`: Main GUI application
- `Backend.py`: Text-to-speech processing and audio handling
- `preparation.bat`: Setup and dependency installation
- `run.bat`: Application launcher
- `Model/`: Directory containing the Kokoro ONNX model
- `voices.json`: Available voice configurations

## License

Apache-2.0 license

## Acknowledgments

- [Kokoro ONNX](https://github.com/hexgrad/Kokoro) for the text-to-speech model
- [HuggingFace](https://huggingface.co/hexgrad/Kokoro-82M) for model hosting

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Submit a pull request with a clear description of your changes

## Issues

If you encounter any problems, please file an issue on the GitHub repository with:
- A clear description of the problem
- Steps to reproduce the issue
- Your system information
- Any relevant error messages

