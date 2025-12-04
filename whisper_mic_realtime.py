import os
import queue
import threading
import sounddevice as sd
import numpy as np
import whisper

MODEL_NAME = "base"
SAMPLE_RATE = 16000
BLOCK_SECONDS = 5  # chunk length

print("Loading Whisper model:", MODEL_NAME)
model = whisper.load_model(MODEL_NAME)

audio_queue = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())

def transcriber():
    print("Transcriber thread started.")
    while True:
        data = audio_queue.get()
        if data is None:
            break
        audio = data.flatten().astype(np.float32)
        result = model.transcribe(audio, fp16=False)
        text = result.get("text", "").strip()
        if text:
            print("\n[Whisper]:", text)

t = threading.Thread(target=transcriber, daemon=True)
t.start()

print("Recording from default microphone. Press Ctrl+C to stop.")
with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=audio_callback):
    try:
        while True:
            sd.sleep(1000)
    except KeyboardInterrupt:
        print("Stopping...")
        audio_queue.put(None)
