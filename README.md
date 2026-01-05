# 🔐 Advanced Image Steganography with Noise Resilience Analysis

## 📱 **Live Demo**
[![Streamlit App Status](https://img.shields.io/badge/Live_Demo-Working-00D9FF?style=flat&logo=streamlit)](https://steganography-noise.streamlit.app/)

## 👨‍🎓 **Student Details**
**Sudarshan Das**  
**BSc Physics** (4-Credit Final Year Project)  
**CENTRAL UNIVERSITY OF KERALA**  
**Academic Year: 2025-2026**

---

## 🎯 **Project Overview**

This **4-credit BSc Physics elective project** demonstrates **Computational Physics** concepts applied to **Information Security**. The system implements:

- **LSB Steganography** (3 bits/pixel RGB encoding)
- **AES-256 Encryption** (SHA256 key derivation + CBC mode)
- **Gaussian Noise Channel Simulation** (Physics-based analysis)
- **PSNR/BER Performance Metrics** (Signal processing)

**Purpose**: Hide sensitive data (messages/images) inside innocent images with quantifiable noise resilience for secure transmission.

---

## ✨ **Key Features**

### ✅ **Core Steganography**
| Feature | Description |
|---------|-------------|
| **Message Encoding** | AES-encrypted text → LSB embedding |
| **Image Encoding** | Hide full images (4-LSB encoding) |
| **Message Decoding** | Extract + decrypt with key |
| **Image Decoding** | Recover secret images |

### 🔬 **Physics Enhancements (4 Credits)**
| Analysis | Metrics |
|----------|---------|
| **Live Noise Demo** | Real-time Gaussian noise (σ slider) |
| **PSNR Calculation** | `10log(255²/MSE)` |
| **BER Testing** | Bit Error Rate vs noise |
| **Experiment Data** | `noise_results.csv` + graphs |

---

## 📊 **Physics Experiment Results**

**Test Setup**: 512×512 PNG → LSB embed → Gaussian noise → BER/PSNR

| Noise (σ) | PSNR (dB) | BER (%) | Visual Quality |
|-----------|-----------|---------|----------------|
| 0.000     | ∞         | 0.00    | Perfect |
| 0.005     | 42.1      | 0.23    | Excellent |
| 0.010     | 36.4      | 2.10    | Very Good |
| 0.020     | 30.2      | 12.40   | Good |
| 0.050     | 24.1      | 45.60   | Poor |

**Key Finding**: LSB maintains **PSNR > 30dB** up to σ=0.02 (acceptable quality)

---

## 🛠 **Technical Stack**

```python
Frontend: Streamlit 1.52.2
Backend: Python 3.13.9 (Streamlit Cloud)
Core Libraries:
├── Pillow 12.1.0     # Image processing
├── NumPy 1.26.4      # Noise generation
├── PyCryptodome 3.21.0 # AES-256 encryption
└── Matplotlib 3.10.8 # Experiment graphs
Deployment: Streamlit Cloud

🚀 Live Demo Features
Encode Message: Image + Text + Key → Download stego PNG

Decode Message: Stego PNG + Key → Extract original text

Noise Analysis: Upload stego → σ slider → Live PSNR calculation

Image Stego: Hide one image inside another
🔧 Quick Start (Local)
bash
git clone https://github.com/Sudarshan-cuk/advanced-image-steganography.git
cd advanced-image-steganography
pip install -r requirements.txt
streamlit run app.py
requirements.txt
text
streamlit
pillow
pycryptodome
numpy<2.0
matplotlib
📈 Algorithm Breakdown
LSB Encoding (3 bits/pixel)
python
# RGB pixel (r,g,b) → embed 3 secret bits
r' = (r & 0xF8) | secret_bit  # 5 MSBs + 1 secret bit
g' = (g & 0xF8) | secret_bit[2]  
b' = (b & 0xF8) | secret_bit[3]
PSNR Formula
PSNR=10log10(MAX2MSE)PSNR=10log 10 ( MSEMAX*MAX = 255 (8-bit images), MSE = mean squared error

🎓 Academic Value (4 Credits)
Computational Physics: Gaussian noise channel simulation

Signal Processing: PSNR/MSE quantitative analysis

Error Analysis: BER characterization vs noise levels

Security: AES+LSB hybrid cryptosystem

Deployment: Production web application📂 Project Deliverables
text
✅ Source Code: app.py + noise analysis modules
✅ Live Demo: https://steganography-noise.streamlit.app/
✅ Experiment Results: noise_results.csv
✅ Graphs: noise_analysis.png (PSNR vs BER)
✅ Documentation: This README
✅ Deployment: Streamlit Cloud (24/7)
✅ GitHub: Professional repo structure
📝 Report Sections Covered
Introduction: Steganography vs Cryptography

Theory: LSB algorithm + AES + Noise models

Methodology: Encoding/decoding flowcharts

Results: PSNR/BER tables + graphs

Discussion: Noise resilience analysis

Conclusion: Physics + Security applications

🔗 Links
Live App: https://steganography-noise.streamlit.app/ ,
[ALTERNATIVE](https://advanced-image-steganography.onrender.com/)

GitHub: https://github.com/Sudarshan-cuk/advanced-image-steganography

Experiment Data: noise_results.csv

Graphs: noise_analysis.png

📄 License
MIT License - Free for academic use.

Sudarshan | BSc Physics | CUKERALA 2025-26
4-Credit Physics Project 🎓
