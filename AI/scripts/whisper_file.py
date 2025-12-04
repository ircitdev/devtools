import sys
import whisper

if len(sys.argv) < 2:
    print("Usage: whisper_file.py <path_to_wav>")
    sys.exit(1)

audio_path = sys.argv[1]

print(f"Loading Whisper base model...")
model = whisper.load_model("base")

print(f"Transcribing: {audio_path}")
result = model.transcribe(audio_path)

print("\n=== TEXT ===\n")
print(result["text"])
print("\n============\n")
