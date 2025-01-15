@echo off

:: Use PowerShell to download the file
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/voices.json' -OutFile 'voices.json'"

:: Check if the download was successful
if exist voices.json (
    echo File downloaded successfully.
) else (
    echo Download failed.
    exit /b 1
)

:: Set up Python virtual environment
python -m venv .venv

:: Activate the virtual environment
call .\.venv\Scripts\activate

:: Install necessary Python packages
pip install sounddevice kokoro_onnx
pip install -U "huggingface_hub[cli]"

:: Download the Kokoro model
huggingface-cli download hexgrad/Kokoro-82M kokoro-v0_19.onnx --local-dir Model

echo Setup complete!
