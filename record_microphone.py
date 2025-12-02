import sounddevice as sd
import numpy as np
import wavio
from pydub import AudioSegment
import threading

SAMPLE_RATE = 44100  
CHANNELS = 1
FILENAME = "recording"

is_recording = False
frames = []
stream = None

def callback(indata, frames_count, time, status):
    """Called repeatedly during recording to store microphone data."""
    if is_recording:
        frames.append(indata.copy())

def start_recording():
    """Start recording audio from the microphone."""
    global is_recording, frames, stream
    frames = []
    is_recording = True
    print("🎤 Recording... Press ENTER to stop.")

    stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback)
    stream.start()

def stop_recording():
    """Stop recording and save the audio as WAV and MP3."""
    global is_recording, frames, stream
    if is_recording:
        is_recording = False
        stream.stop()
        stream.close()

        audio_data = np.concatenate(frames, axis=0)

        wavio.write(f"{FILENAME}.wav", audio_data, SAMPLE_RATE, sampwidth=2)
        print(f"✅ Saved {FILENAME}.wav")

        audio = AudioSegment.from_wav(f"{FILENAME}.wav")
        audio.export(f"{FILENAME}.mp3", format="mp3")
        print(f"🎧 Saved {FILENAME}.mp3")

if __name__ == "__main__":
    input("Press ENTER to start recording...")
    start_recording()
    input("Press ENTER to stop recording...")
    stop_recording()