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
