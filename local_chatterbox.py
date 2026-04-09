#!/usr/bin/env python3
"""
Chatterbox TTS – Local Setup & Demo

Run this script to:
1. Install required dependencies (with a confirmation prompt).
2. Load the Chatterbox model.
3. Generate a sample TTS output using your own text.

Usage:
    python local_chatterbox.py
"""

import subprocess
import sys
import os
from pathlib import Path

# ----------------------------------------------------------------------
# 1. Dependency Installation (optional, can skip if already set up)
# ----------------------------------------------------------------------
def run_command(command, description=""):
    print(f"\n🔧 {description if description else command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"⚠️  Command failed: {command}\n{result.stderr}")
        return False
    print(f"✅ Success")
    return True

def install_dependencies():
    print("=" * 60)
    print("📦 Installing Chatterbox TTS Dependencies")
    print("=" * 60)

    # Upgrade pip
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip")

    # Clean previous installations
    run_command(
        f"{sys.executable} -m pip uninstall -y torch torchvision torchaudio transformers chatterbox-tts accelerate huggingface-hub diffusers torchao perth resemble-perth",
        "Cleaning old packages"
    )

    # PyTorch 2.5.0 (full build)
    run_command(
        f"{sys.executable} -m pip install torch==2.5.0 torchaudio==2.5.0",
        "Installing PyTorch 2.5.0"
    )

    # Chatterbox dependencies
    run_command(f"{sys.executable} -m pip install transformers==4.46.3", "Transformers")
    run_command(f"{sys.executable} -m pip install diffusers==0.29.0", "Diffusers")
    run_command(f"{sys.executable} -m pip install huggingface_hub>=0.23.0", "HuggingFace Hub")
    run_command(f"{sys.executable} -m pip install accelerate>=0.25.0", "Accelerate")

    # Audio and other libs
    run_command(
        f"{sys.executable} -m pip install 'numpy>=1.24.0,<1.26.0' librosa==0.11.0 safetensors soundfile scipy",
        "Audio processing libraries"
    )

    # Resemble-perth watermarker
    run_command(f"{sys.executable} -m pip install resemble-perth", "Resemble Perth")

    # Tokenizers
    run_command(f"{sys.executable} -m pip install s3tokenizer conformer", "S3Tokenizer & Conformer")

    # Chatterbox itself (no deps)
    run_command(f"{sys.executable} -m pip install chatterbox-tts --no-deps", "Chatterbox TTS")

    # Protobuf fix
    run_command(f"{sys.executable} -m pip uninstall -y protobuf", "Uninstall protobuf")
    run_command(f"{sys.executable} -m pip install protobuf==3.20.3", "Install protobuf 3.20.3")

    print("\n✅ All dependencies installed.\n")

# ----------------------------------------------------------------------
# 2. Model Loading
# ----------------------------------------------------------------------
def load_chatterbox_model():
    import torch
    from chatterbox.tts import ChatterboxTTS

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🚀 Loading Chatterbox model on {device}...")
    try:
        model = ChatterboxTTS.from_pretrained(device=device)
        print("✅ Model loaded successfully.")
    except Exception as e:
        print(f"⚠️  GPU load failed ({e}), falling back to CPU...")
        model = ChatterboxTTS.from_pretrained(device="cpu")
        print("✅ Model loaded on CPU.")
    return model

# ----------------------------------------------------------------------
# 3. Configuration & Utilities
# ----------------------------------------------------------------------
class ChatterboxConfig:
    def __init__(self):
        self.exaggeration = 0.75
        self.cfg_weight = 0.3
        self.max_chunk_words = 40
        self.voice_sample_path = None   # Set to a .wav file path for cloning

    def get_preset(self, preset_name):
        presets = {
            "neutral": {"exaggeration": 0.5, "cfg_weight": 0.5},
            "calm": {"exaggeration": 0.3, "cfg_weight": 0.6},
            "expressive": {"exaggeration": 0.7, "cfg_weight": 0.4},
            "dramatic": {"exaggeration": 1.0, "cfg_weight": 0.3},
            "storytelling": {"exaggeration": 0.8, "cfg_weight": 0.4},
            "audiobook": {"exaggeration": 0.4, "cfg_weight": 0.6},
            "fast_speaker": {"exaggeration": 0.6, "cfg_weight": 0.3},
        }
        return presets.get(preset_name, presets["storytelling"])

def split_into_chunks(text, max_words=100):
    sentences = text.strip().replace('\n', ' ').split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    chunks = []
    current_chunk = ""
    current_word_count = 0
    for sentence in sentences:
        sentence_words = sentence.split()
        if current_word_count + len(sentence_words) > max_words and current_chunk:
            chunks.append(current_chunk.strip() + ".")
            current_chunk = sentence
            current_word_count = len(sentence_words)
        else:
            if current_chunk:
                current_chunk += ". " + sentence
            else:
                current_chunk = sentence
            current_word_count += len(sentence_words)
    if current_chunk:
        chunks.append(current_chunk.strip() + ".")
    return chunks

def generate_speech(text, config, model, output_filename="output.wav"):
    import torch
    import torchaudio

    print("\n🎙️ Generating speech...")
    chunks = split_into_chunks(text, config.max_chunk_words)
    wav_tensors = []

    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}/{len(chunks)}: {chunk[:40]}...")
        gen_params = {
            "text": chunk,
            "exaggeration": config.exaggeration,
            "cfg_weight": config.cfg_weight
        }
        if config.voice_sample_path and os.path.exists(config.voice_sample_path):
            gen_params["audio_prompt_path"] = config.voice_sample_path
        try:
            wav = model.generate(**gen_params)
            wav_tensors.append(wav)
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except Exception as e:
            print(f"❌ Error generating chunk {i+1}: {e}")
            continue

    if not wav_tensors:
        print("❌ No audio generated.")
        return None

    full_audio = torch.cat(wav_tensors, dim=1)
    torchaudio.save(output_filename, full_audio, model.sr)
    print(f"✅ Audio saved to: {output_filename}")
    return output_filename

# ----------------------------------------------------------------------
# 4. Main Execution
# ----------------------------------------------------------------------
def main():
    # Ask if user wants to install dependencies
    if "--no-install" not in sys.argv:
        resp = input("Install dependencies now? (y/n): ").strip().lower()
        if resp == 'y':
            install_dependencies()
        else:
            print("Skipping installation. Assuming dependencies are already present.")

    # Imports after possible installation
    try:
        from chatterbox.tts import ChatterboxTTS
    except ImportError:
        print("❌ Chatterbox not found. Please run the script again and choose 'y' to install.")
        sys.exit(1)

    # Load model
    model = load_chatterbox_model()

    # Configuration
    config = ChatterboxConfig()
    # (Optional) Set voice cloning path
    # config.voice_sample_path = "/path/to/voice_sample.wav"

    # Sample text
    sample_text = """
    Welcome to Chatterbox Text-to-Speech running locally on your machine.
    You can adjust the exaggeration and guidance weight to change the speaking style.
    For voice cloning, provide a short WAV file with the voice_sample_path variable.
    Enjoy experimenting!
    """

    print("\n📝 Text to synthesize:")
    print("-" * 40)
    print(sample_text.strip())
    print("-" * 40)

    output_file = generate_speech(sample_text, config, model, "chatterbox_local_output.wav")
    if output_file:
        print(f"\n🎉 Done! Listen to '{output_file}'.")

if __name__ == "__main__":
    main()
