# 🤖 Frank Vision Helmet - Raspberry Pi Zero W

A voice-controlled AI-powered vision assistant designed for Raspberry Pi Zero W. Frank provides real-time visual description, reads text from screens and papers, and can make voice calls—all controlled by simple voice commands.

**Designed for accessibility**: Perfect for users who are blind or visually impaired.

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🎯 Features

✨ **Voice-Controlled AI Assistant**
- Wake word detection ("Frank" or "Hello")
- Natural language responses using Google Gemini 2.0 Flash
- Real-time speech synthesis with gTTS

👁️ **Computer Vision**
- Describes scenes and objects in real-time
- Reads text from screens, papers, and documents
- Identifies colors, shapes, and spatial relationships
- Optimized for Raspberry Pi Zero W performance

📞 **Communication**
- Make voice calls via Twilio integration
- Customizable contact list
- Automated greeting messages

🔴 **Smart LED Status Indicators**
- 🟢 Green: Program running/processing
- 🔴 Red: Microphone/audio errors
- 🟡 Yellow: Camera/vision errors

📋 **Logging & Monitoring**
- Comprehensive system logs
- Easy debugging and troubleshooting
- Optional systemd service for autostart

---

## 📋 Hardware Requirements

| Component | Specs |
|-----------|-------|
| **Processor** | Raspberry Pi Zero W |
| **Camera** | Pi Camera v2 (or USB equivalent) |
| **Microphone** | USB microphone or audio interface |
| **Audio Output** | Speaker or headphones (3.5mm jack) |
| **LEDs** | 3× with 220Ω resistors (GPIO 17, 27, 22) |
| **Power** | 5V 2.5A+ (USB power adapter) |
| **Storage** | 8GB+ microSD card |

---

## 🚀 Quick Start

### 1. One-Line Installation

```bash
curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/frank-vision-helmet/main/setup.sh | bash
```

Or manual installation:

```bash
sudo apt-get update && sudo apt-get upgrade -y
git clone https://github.com/YOUR_USERNAME/frank-vision-helmet.git
cd frank-vision-helmet
bash setup.sh
```

### 2. Configure API Keys

Edit `frank_vision_helmet_pizero.py`:

```python
API_KEY = 'your-google-gemini-api-key'
TWILIO_ACCOUNT_SID = "your-twilio-account-sid"
TWILIO_AUTH_TOKEN = "your-twilio-auth-token"
```

### 3. Add Contacts

```python
CONTACTS = {
    "sriram": {
        "phone": "+918148624912",
        "greeting": "Hello Shriram, this is Frank."
    },
}
```

### 4. Test Hardware

```bash
source ~/frank_env/bin/activate
python3 test_leds.py        # Test LED connections
python3 test_camera.py      # Test camera
python3 test_microphone.py  # Test microphone
```

### 5. Run Frank

```bash
python3 frank_vision_helmet_pizero.py
```

---

## 💬 Usage Examples

### Wake Up Frank
```
"Frank, hello"
"Frank, are you there?"
```

### Vision Tasks
```
"Frank, what's in front of me?"
"Frank, read the text on the screen"
"Frank, describe what you see"
"Frank, what is on the paper?"
```

### Make Calls
```
"Frank, call Sriram"
"Frank, make a call to Shriram"
```

### General Chat
```
"Frank, what time is it?"
"Frank, what's the date?"
"Frank, tell me a joke"
```

### Stop
```
"Frank, stop"
"Frank, goodbye"
```

---

## 🔧 API Setup

### Google Gemini API (Free)

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Click "Get API Key"
3. Create a new API key
4. Copy to `frank_vision_helmet_pizero.py`

### Twilio Account (Paid - Trial Available)

1. Sign up at [Twilio.com](https://www.twilio.com/)
2. Get Account SID and Auth Token from Dashboard
3. Get a Twilio phone number
4. Add credits for calls
5. Copy credentials to script

---

## 📁 Project Structure

```
frank-vision-helmet/
├── frank_vision_helmet_pizero.py    # Main application
├── frank_helmet.log                 # Auto-generated logs
├── requirements.txt                 # Python dependencies
├── setup.sh                         # Installation script
├── FRANK_SETUP_GUIDE.md            # Detailed setup guide
├── README.md                        # This file
└── tests/
    ├── test_leds.py                # LED functionality test
    ├── test_camera.py              # Camera test
    └── test_microphone.py          # Microphone test
```

---

## 🔌 GPIO Pinout

```
Raspberry Pi Zero W GPIO Layout:
(Using BCM numbering)

GPIO 17 (Pin 11) ──→ Green LED (Program Status)
GPIO 27 (Pin 13) ──→ Red LED (Microphone Error)
GPIO 22 (Pin 15) ──→ Yellow LED (Vision Error)

Each LED should connect through a 220Ω resistor to Ground (Pin 6, 9, 14, etc.)
```

 
---

## 🛠️ Troubleshooting

### Camera Issues
```bash
# Enable camera in raspi-config
sudo raspi-config
# Interface Options → Camera → Enable

# Test camera
raspistill -o test.jpg
python3 test_camera.py
```

### Microphone Issues
```bash
# List audio devices
arecord -l
aplay -l

# Test microphone
arecord -D default test.wav
aplay test.wav

# Check levels
alsamixer
```

### API Connection Issues
```bash
# Test internet
ping google.com

# Test APIs
python3 -c "from google import genai; print('Gemini OK')"
python3 -c "from twilio.rest import Client; print('Twilio OK')"
```

### View Logs
```bash
# Application logs
tail -f /home/pi/frank_helmet.log

# System service logs (if running as service)
journalctl -u frank -f
```

---

## ⚡ Performance Optimization

The code is already optimized for Raspberry Pi Zero W:

- ✅ Low-resolution camera (320x240)
- ✅ Reduced frame rate (15 FPS)
- ✅ Compressed JPEG output
- ✅ Efficient GPIO operations
- ✅ Minimal memory footprint

### Additional Tips
- Disable WiFi when not needed
- Close unnecessary processes
- Increase GPU memory: `raspi-config` → Performance Options
- Use headless mode if no display needed

---

## 🔐 Security Notes

⚠️ **IMPORTANT:**
- Never commit API keys to GitHub
- Use `.gitignore` to exclude credentials
- Restrict file permissions: `chmod 600 frank_vision_helmet_pizero.py`
- Store credentials in environment variables for production use

---

## 🚀 Running as Autostart Service

### Automatic Setup (during installation)
```bash
bash setup.sh  # Follow prompts
```

### Manual Setup
```bash
sudo nano /etc/systemd/system/frank.service
```

Add the contents shown in the setup guide, then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable frank
sudo systemctl start frank
journalctl -u frank -f  # View logs
```

---

## 📊 LED Status Guide

| LED | State | Meaning |
|-----|-------|---------|
| 🟢 Green | Solid | Program running |
| 🟢 Green | Blinking (1x) | Wake word detected |
| 🟢 Green | Blinking (2x) | Processing task |
| 🔴 Red | Blinking | Microphone/audio error |
| 🟡 Yellow | Blinking | Camera/vision error |

---

## 📚 Documentation

- **[FRANK_SETUP_GUIDE.md](FRANK_SETUP_GUIDE.md)** - Comprehensive setup guide
- **[frank_vision_helmet_pizero.py](frank_vision_helmet_pizero.py)** - Fully commented source code

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

Created for **Chinu** - An accessibility-focused AI vision project

---

## 🙏 Acknowledgments

- Google Gemini 2.0 Flash for powerful AI
- Twilio for voice communication
- OpenCV for computer vision
- The Raspberry Pi community

---

## 📞 Support & Issues

Found a bug or have a suggestion?

1. **Check existing issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/frank-vision-helmet/issues)
2. **Check logs**: `tail -f /home/pi/frank_helmet.log`
3. **Read troubleshooting**: See [FRANK_SETUP_GUIDE.md](FRANK_SETUP_GUIDE.md)
4. **Open new issue**: Include error logs and hardware details

---

## 🎓 Learning Resources

- [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)
- [OpenCV Tutorials](https://docs.opencv.org/master/d9/df8/tutorial_root.html)
- [Google Gemini API Guide](https://ai.google.dev/)
- [Twilio Voice Documentation](https://www.twilio.com/docs/voice)

---

## 🌟 Give a Star!

If this project helps you, please give it a ⭐ on GitHub!

---

**Made with ❤️ for accessibility**
