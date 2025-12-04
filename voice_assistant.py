import os
import sounddevice as sd
import numpy as np
import whisper
import pyttsx3
from llama_cpp import Llama

MODEL_PATH = r"D:\DevTools\AI\models\llama3-8b-instruct.Q4_K_M.gguf"
SAMPLE_RATE = 16000
RECORD_SECONDS = 6

if not os.path.exists(MODEL_PATH):
    print("LLM model not found:", MODEL_PATH)
    exit(1)

print("Loading Whisper (base)...")
whisper_model = whisper.load_model("base")

print("Loading LLaMA model...")
llm = Llama(model_path=MODEL_PATH, n_ctx=4096, n_threads=6)

print("Init TTS engine...")
tts = pyttsx3.init()
tts.setProperty("rate", 170)

def record_audio(seconds=RECORD_SECONDS):
    print(f"Recording {seconds} seconds...")
    audio = sd.rec(int(seconds * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="float32")
    sd.wait()
    return audio.flatten()

def transcribe_audio(audio):
    print("Transcribing...")
    result = whisper_model.transcribe(audio, fp16=False)
    return result.get("text", "").strip()

def ask_llm(prompt):
    print("Asking LLaMA...")
    out = llm(prompt, max_tokens=200, stop=["User:", "You:", "\n\n"])
    return out["choices"][0]["text"].strip()

def speak(text):
    print("AI:", text)
    tts.say(text)
    tts.runAndWait()

print("Voice assistant ready. Say something, or press Ctrl+C to exit.")

try:
    while True:
        audio = record_audio()
        text = transcribe_audio(audio)
        if not text:
            print("No speech detected.")
            continue
        print("You:", text)
        if text.lower() in ("exit", "выход", "стоп"):
            speak("Goodbye.")
            break
        answer = ask_llm(text)
        speak(answer)
except KeyboardInterrupt:
    print("Stopping voice assistant.")
