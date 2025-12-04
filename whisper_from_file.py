import os
import whisper

AUDIO_DIR = r"D:\DevTools\AI\audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

print("Put your audio file (wav/mp3/m4a) into:", AUDIO_DIR)
filename = input("File name (with extension): ").strip()
path = os.path.join(AUDIO_DIR, filename)

if not os.path.exists(path):
    print("File not found:", path)
    exit(1)

print("Loading Whisper model 'base' (CPU)...")
model = whisper.load_model("base")
result = model.transcribe(path)

print("\n=== TRANSCRIPT ===\n")
print(result["text"])
