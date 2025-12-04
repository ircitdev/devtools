import os
import whisper
import soundfile as sf
import subprocess
import uuid

INPUT_DIR = r"D:\DevTools\voice\input"
OUTPUT_DIR = r"D:\DevTools\voice\output"
TEMP_DIR = r"D:\DevTools\voice\temp"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Whisper model
print("Loading Whisper base model...")
model = whisper.load_model("base")

def convert_to_wav(input_path):
    """Converts any media file to WAV 16kHz mono for Whisper."""
    output_path = os.path.join(TEMP_DIR, str(uuid.uuid4()) + ".wav")
    cmd = [
        "ffmpeg", "-i", input_path,
        "-ar", "16000", "-ac", "1",
        "-y", output_path
    ]
    try:
        subprocess.run(cmd, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        return output_path
    except:
        return None


def transcribe_file(file_path):
    """Transcribe a single audio file."""
    print(f"\nProcessing: {file_path}")

    wav = convert_to_wav(file_path)
    if not wav:
        print("Error converting file, skipping.")
        return

    result = model.transcribe(wav)
    text = result.get("text", "").strip()

    base = os.path.basename(file_path)
    name, _ = os.path.splitext(base)
    out_path = os.path.join(OUTPUT_DIR, f"{name}.txt")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Saved transcript: {out_path}")


def process_all():
    files = os.listdir(INPUT_DIR)
    if not files:
        print("No files found.")
        return

    for f in files:
        fpath = os.path.join(INPUT_DIR, f)
        if not os.path.isfile(fpath):
            continue

        # Skip non-audio formats by extension
        if not f.lower().endswith((".wav", ".mp3", ".m4a", ".aac", ".ogg", ".flac", ".mp4", ".mov", ".webm")):
            print(f"Skipping (unknown format): {f}")
            continue

        # Skip if transcript already exists
        name = os.path.splitext(f)[0] + ".txt"
        if os.path.exists(os.path.join(OUTPUT_DIR, name)):
            print(f"Already processed: {f}")
            continue

        transcribe_file(fpath)


if __name__ == "__main__":
    print("Batch Whisper Processor Started")
    process_all()
    print("\nDone.")
