# 🗣️ Chatterbox TTS Setup

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Yonatankinfe/chatterbox-tts/blob/main/chatterbox_colab.ipynb)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A streamlined, battle-tested setup for [Chatterbox TTS](https://github.com/resemble-ai/chatterbox) — the expressive, voice-cloning text-to-speech model by Resemble AI. This repository provides **two foolproof ways** to get Chatterbox running:

- ☁️ **Google Colab Notebook** – Zero local setup, runs entirely in the cloud with GPU acceleration.
- 💻 **Local Python Script** – For users who want to run Chatterbox on their own machine.

Both methods include:
- Automatic dependency resolution (solves the tricky `torch.fx` / `torchao` conflicts).
- Voice cloning from a short reference audio file.
- Adjustable expressiveness (`exaggeration`, `cfg_weight`).
- Automatic text chunking for long passages.
- Audio playback and waveform visualization.

---
## 🚀 Quick Start

### ☁️ Option 1: Google Colab (Recommended)

Click the badge above or [open this link](https://colab.research.google.com/github/Yonatankinfe/chatterbox-tts/blob/main/chatterbox_colab.ipynb).  
Run the cells **in order** – the notebook will install everything, download the model, and generate speech.  
Upload a voice sample to your Google Drive for cloning (optional).

### 💻 Option 2: Local Setup
```bash
git clone https://github.com/Yonatankinfe/chatterbox-tts.git
cd chatterbox-tts
python local_chatterbox.py
```

### The script will:

+ Create a virtual environment (optional).
+ Install exact dependencies.
+ Download the model.
+ Generate a sample TTS output.

###⚠️ System Requirements (Local)

+ Python 3.10 or 3.11 (3.12 may work but is untested).
+ CUDA‑compatible GPU recommended (CPU fallback works, slowly).
+ ~6 GB free disk space for model weights.
### 📦 Dependencies 
```bash
torch==2.5.0
torchaudio==2.5.0
transformers==4.46.3
diffusers==0.29.0
protobuf==3.20.3
chatterbox-tts (latest, --no-deps)
resemble-perth
s3tokenizer
conformer
librosa==0.11.0
```
### 📁 Repository Structure
```bash
chatterbox-tts/
├── README.md                 # You are here
├── chatterbox_colab.ipynb    # Google Colab notebook (end‑to‑end)
└── local_chatterbox.py       # Single‑script local setup + demo
```
### 🎛️ Configuration Options
Both the notebook and local script expose key parameters:
<img width="751" height="341" alt="Image" src="https://github.com/user-attachments/assets/318a8599-2257-4e67-b2f6-2e5380c0855c" />
### 🎭 Presets
The code includes several speaking‑style presets:
```bash
"neutral", "calm", "expressive", "dramatic", "storytelling", "audiobook", "fast_speaker"
```
Example
```bash
config.get_preset("storytelling")  # Returns dict with exaggeration=0.8, cfg_weight=0.4
```
### ⚠️ Known Limitations

+ Voice Samples: Must be WAV format, 10-30 seconds, clean audio
+ Long Texts: Very long passages (>2000 words) may require multiple runs
+ GPU Memory: 6GB+ VRAM recommended for optimal performance
+ Python Version: Tested on 3.10/3.11; 3.12 untested

### 🙏 Acknowledgments
+ Resemble AI for creating and open-sourcing Chatterbox
+ The PyTorch team for the incredible deep learning framework
+ All early testers who helped identify edge cases
