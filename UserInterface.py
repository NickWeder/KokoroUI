import tkinter as tk
from tkinter import messagebox, filedialog
import sounddevice as sd
import soundfile as sf
from kokoro_onnx import Kokoro
import asyncio
import threading

# Initialize Kokoro
kokoro = Kokoro("Model/kokoro-v0_19.onnx", "voices.json")

# Main application window
root = tk.Tk()
root.geometry("600x600")
root.title("Kokoro")
root.config(bg="#f7f7f7")

# Form frame for layout
formFrame = tk.Frame(root, padx=30, pady=30, bg="#f7f7f7")
formFrame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Modern fonts and colors
font_header = ("Segoe UI", 14, "bold")
font_label = ("Segoe UI", 12)
font_button = ("Segoe UI", 12, "bold")
bg_color = "#4A90E2"
button_color = "#50E3C2"
hover_color = "#3A80B8"
text_color = "#333333"

# Label for the dropdown
voice_label = tk.Label(formFrame, text="Select a Voice:", font=font_label, bg="#f7f7f7", fg=text_color)
voice_label.pack(anchor="w", pady=10)

# Dropdown menu for voices
voices = list(kokoro.get_voices())  # Convert dict_keys to list
selected_voice = tk.StringVar(value=voices[0])  # Default value

voice_dropdown = tk.OptionMenu(formFrame, selected_voice, *voices)
voice_dropdown.config(width=30, font=font_label, bg="white", fg=text_color, relief="solid", borderwidth=1)
voice_dropdown.pack(anchor="w", fill=tk.X, pady=5)

# Input field for custom text
text_label = tk.Label(formFrame, text="Enter Text to Play:", font=font_label, bg="#f7f7f7", fg=text_color)
text_label.pack(anchor="w", pady=10)

text_input = tk.Entry(formFrame, width=50, font=("Segoe UI", 12), relief="solid", borderwidth=1)
text_input.pack(anchor="w", fill=tk.X, pady=5)

# Label for file upload option
file_label = tk.Label(formFrame, text="Or Upload a .txt File to Play:", font=font_label, bg="#f7f7f7", fg=text_color)
file_label.pack(anchor="w", pady=10)

# Function to open file dialog and load content
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                file_content = file.read().strip()
                text_input.delete(0, tk.END)  # Clear any previous input
                text_input.insert(0, file_content)  # Insert file content into text input
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read the file: {e}")

upload_button = tk.Button(formFrame, text="Upload File", command=upload_file, font=font_button, bg=button_color, fg="white", relief="flat")
upload_button.pack(anchor="w", pady=10, fill=tk.X)

# Label to display loading message
loading_label = tk.Label(formFrame, text="", font=("Segoe UI", 12), bg="#f7f7f7", fg=text_color)
loading_label.pack(anchor="w", pady=10)

# Track if the audio is playing
is_playing = False
stop_event = threading.Event()
current_thread = None

# Async function to play the selected voice with custom text or file content
async def async_play_voice():
    global is_playing
    voice = selected_voice.get()
    text = text_input.get().strip()
    
    if not text:
        messagebox.showerror("Error", "Please enter some text or upload a file to play.")
        return
    
    loading_label.config(text="Loading... Please wait.", fg="#ff6f00")
    root.update_idletasks()
    
    try:
        stream = kokoro.create_stream(
            text=text,
            voice=voice,
            speed=1.0,
            lang="en-us",
        )
        
        stop_event.clear()  # Reset the stop event
        count = 0
        async for samples, sample_rate in stream:
            if stop_event.is_set():
                break
            count += 1
            print(f"Playing audio stream ({count})...")
            sd.play(samples, sample_rate)
            sd.wait()
            
        loading_label.config(text="")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        loading_label.config(text="")
    finally:
        is_playing = False
        root.after(0, lambda: play_button.config(text="Play Voice", bg=bg_color))


# Wrapper to run the async function in a separate event loop
def play_voice():
    global is_playing, current_thread
    if is_playing:
        stop_voice()
    else:
        def run_in_thread():
            asyncio.run(async_play_voice())
        
        current_thread = threading.Thread(target=run_in_thread, daemon=True)
        current_thread.start()
        is_playing = True
        play_button.config(text="Stop Voice", bg="#E74C3C")

# Stop the audio stream and reset button
def stop_voice():
    global is_playing, current_thread
    loading_label.config(text="")
    stop_event.set()  # Signal the async loop to stop
    sd.stop()  # Stop any currently playing audio
    is_playing = False
    play_button.config(text="Play Voice", bg=bg_color)
    
    # Wait for the thread to finish if it exists
    if current_thread and current_thread.is_alive():
        current_thread.join(timeout=1.0)

play_button = tk.Button(formFrame, text="Play Voice", command=play_voice, font=font_button, bg=bg_color, fg="white", relief="flat")
play_button.pack(anchor="w", pady=20, fill=tk.X)

# Function to save the generated voice to a .wav file
def save_voice():
    voice = selected_voice.get()
    text = text_input.get().strip()  # Get text from input field
    if not text:
        messagebox.showerror("Error", "Please enter some text or upload a file to save.")
        return
    
    try:
        samples, sample_rate = kokoro.create(text, voice=voice, speed=1.0, lang="en-us")
        
        # Ask the user how they want to name the file
        save_path = filedialog.asksaveasfilename(
            defaultextension=".wav", 
            filetypes=[("WAV files", "*.wav")],
            initialfile="audio.wav"  # Default name for the file
        )
        
        if save_path:
            sf.write(save_path, samples, sample_rate)  # Save the audio to a file
            messagebox.showinfo("Success", f"Audio saved as {save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save audio: {e}")

# Save voice button
save_button = tk.Button(formFrame, text="Save Voice", command=save_voice, font=font_button, bg="#FFD700", fg="white", relief="flat")
save_button.pack(anchor="w", pady=10, fill=tk.X)

# Styling (optional) to ensure buttons have a hover effect
def on_enter(event, button):
    button.config(bg=hover_color)

def on_leave(event, button):
    button.config(bg=bg_color)

# Bind hover effect for buttons
play_button.bind("<Enter>", lambda e: on_enter(e, play_button))
play_button.bind("<Leave>", lambda e: on_leave(e, play_button))
upload_button.bind("<Enter>", lambda e: on_enter(e, upload_button))
upload_button.bind("<Leave>", lambda e: on_leave(e, upload_button))
save_button.bind("<Enter>", lambda e: on_enter(e, save_button))
save_button.bind("<Leave>", lambda e: on_leave(e, save_button))

# Run the application
root.mainloop()
