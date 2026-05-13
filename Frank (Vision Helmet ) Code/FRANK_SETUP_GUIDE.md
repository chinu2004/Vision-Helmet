# Frank Vision Helmet - Raspberry Pi Zero W

A voice-controlled AI assistant with computer vision capabilities designed specifically for Raspberry Pi Zero W. Features real-time vision processing, speech synthesis, and smart home integration.

## 🎯 Features

- **Wake Word Detection**: Responds to "Frank" or "Hello"
- **AI Vision Processing**: Reads text, describes scenes, and answers visual questions
- **Voice Synthesis**: Natural speech responses using gTTS
- **Voice Control**: Make calls, ask questions, and more
- **LED Status Indicators**:
  - 🟢 Green LED: Program status
  - 🔴 Red LED: Microphone/audio errors
  - 🟡 Yellow LED: Camera/vision errors
- **Twilio Integration**: Make voice calls to saved contacts
- **Logging**: Comprehensive logging for debugging

## 📋 Hardware Requirements

- **Raspberry Pi Zero W** (WiFi version)
- **Pi Camera Module v2** (or compatible USB camera)
- **3 x LEDs** with resistors:
  - Green LED (GPIO 17)
  - Red LED (GPIO 27)
  - Yellow LED (GPIO 22)
- **Microphone/USB audio interface**
- **Speaker or audio output**
- **Power supply** (5V, 2.5A or higher)
- **MicroSD card** (8GB minimum)

## 🔧 GPIO Pinout

```
GPIO 17 (Pin 11) → Green LED (Program Status)
GPIO 27 (Pin 13) → Red LED (Microphone Error)
GPIO 22 (Pin 15) → Yellow LED (Camera/Vision Error)

Each LED should be connected with a 220Ω resistor to ground.
```

## 📦 Installation

### 1. Update Raspberry Pi OS

```bash
sudo apt-get update
sudo apt-get upgrade
```

### 2. Install System Dependencies

```bash
# Python development tools
sudo apt-get install python3-pip python3-dev python3-venv

# Audio libraries
sudo apt-get install alsa-utils portaudio19-dev

# Camera support
sudo apt-get install libatlas-base-dev libjasper-dev libtiff5 libjasper1 libharfbuzz0b libwebp6 libtiff5

# OpenCV dependencies
sudo apt-get install libopenjp2-7 libtiff5 libjasper1 libharfbuzz0b libwebp6

# Other utilities
sudo apt-get install git wget curl libssl-dev
```

### 3. Create Python Virtual Environment

```bash
python3 -m venv ~/frank_env
source ~/frank_env/bin/activate
```

### 4. Install Python Packages

```bash
pip install --upgrade pip setuptools wheel

# Core packages
pip install RPi.GPIO
pip install opencv-python
pip install SpeechRecognition
pip install pyaudio
pip install gTTS
pip install twilio
pip install google-generativeai
pip install Pillow
```

### 5. Setup Audio (IMPORTANT for Pi Zero W)

Test your audio setup:

```bash
# List available audio devices
arecord -l
aplay -l

# Record a test audio
arecord -D default -f cd test.wav -d 5

# Play it back
aplay test.wav
```

If using USB audio interface, update `~/.asoundrc`:

```bash
pcm.!default {
    type asym
    playback.pcm "playback"
    capture.pcm "capture"
}

pcm.playback {
    type plug
    slave.pcm "hw:1,0"
}

pcm.capture {
    type plug
    slave.pcm "hw:1,0"
}
```

### 6. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/frank-vision-helmet.git
cd frank-vision-helmet
```

### 7. Configure API Keys

Edit `frank_vision_helmet_pizero.py` and add your credentials:

```python
# Line ~70-72
API_KEY = 'YOUR_GOOGLE_GEMINI_API_KEY'
TWILIO_ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
```

### 8. Add Contacts

Edit the `CONTACTS` dictionary in the script:

```python
CONTACTS = {
    "sriram": {
        "phone": "+918148624912",
        "greeting": "Hello Shriram, this is Frank calling you."
    },
    "your_name": {
        "phone": "+91XXXXXXXXXX",
        "greeting": "Hello, this is Frank calling you."
    },
}
```

## 🚀 Running Frank

### Manual Run

```bash
source ~/frank_env/bin/activate
python3 frank_vision_helmet_pizero.py
```

### Run as Service (Autostart)

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/frank.service
```

Add the following content:

```ini
[Unit]
Description=Frank Vision Helmet Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/frank-vision-helmet
ExecStart=/home/pi/frank_env/bin/python3 /home/pi/frank-vision-helmet/frank_vision_helmet_pizero.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable frank
sudo systemctl start frank

# Monitor logs
journalctl -u frank -f
```

## 📝 Usage Commands

### Wake Frank Up
```
"Frank, hello"
"Frank, what's the time?"
```

### Vision Tasks
```
"Frank, what's in front of me?"
"Frank, read the text on the screen"
"Frank, what is on the paper?"
"Frank, describe what you see"
```

### Make Calls
```
"Frank, make a call to Sriram"
"Frank, call Shriram"
```

### General Chat
```
"Frank, what's the weather like?"
"Frank, tell me a joke"
"Frank, what time is it?"
```

### Stop
```
"Frank, stop"
"Frank, goodbye"
```

## 🔧 Getting API Keys

### Google Gemini API
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Click "Get API Key"
3. Create new API key
4. Copy and paste into the script

### Twilio
1. Sign up at [Twilio](https://www.twilio.com/)
2. Get your Account SID and Auth Token
3. Get a Twilio phone number
4. Add credit for calls
5. Copy credentials into the script

## 📊 LED Status Indicators

| LED | Status | Meaning |
|-----|--------|---------|
| 🟢 Green | ON | Program running |
| 🟢 Green | Blinking | Processing task |
| 🔴 Red | Blinking | Microphone/Audio error |
| 🟡 Yellow | Blinking | Camera/Vision error |

## 🐛 Troubleshooting

### Camera Not Working
```bash
# Enable camera
sudo raspi-config
# Interface Options → Camera → Enable

# Test camera
raspistill -o test.jpg

# Check if camera is detected
vcgencmd get_camera
```

### Microphone Not Detected
```bash
# List audio devices
arecord -l

# Test microphone
arecord -D default -f cd test.wav -d 5
aplay test.wav
```

### Speech Recognition Issues
```bash
# Check internet connection
ping google.com

# Test speech recognition module
python3 -c "import speech_recognition as sr; print(sr.__version__)"
```

### API Connection Issues
```bash
# Test Gemini API
python3 -c "from google import genai; print('Genai module OK')"

# Test Twilio
python3 -c "from twilio.rest import Client; print('Twilio module OK')"
```

### Check Logs
```bash
# View application logs
tail -f /home/pi/frank_helmet.log

# View systemd service logs
journalctl -u frank -f
```

## ⚡ Performance Tips for Pi Zero W

- Use resolution 320x240 for camera (already optimized in code)
- Enable GPU memory split in `raspi-config` (GPU Memory: 128MB)
- Close unnecessary processes
- Use headless mode if GUI not needed
- Consider disabling WiFi when not in use (drains battery)

## 📚 Project Structure

```
frank-vision-helmet/
├── frank_vision_helmet_pizero.py  # Main application
├── frank_helmet.log               # Application logs
├── README.md                       # This file
├── requirements.txt               # Python dependencies
├── setup.sh                       # Installation script
└── examples/
    ├── test_camera.py            # Camera test script
    ├── test_microphone.py         # Microphone test script
    └── test_leds.py              # LED test script
```

## 🛠️ Development & Debugging

### Test Individual Components

```bash
# Test LEDs
python3 test_leds.py

# Test Camera
python3 test_camera.py

# Test Microphone
python3 test_microphone.py

# Test API connection
python3 -c "from google import genai; client = genai.Client(api_key='YOUR_KEY'); print('Connected!')"
```

## 📄 License

MIT License - Feel free to use and modify

## 👤 Author

Created for Chinu - A vision assistance project using AI

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs (`frank_helmet.log`)
3. Open a GitHub issue with error details and logs

## 🔐 Security Notes

- **Never commit API keys** to GitHub
- Use environment variables for sensitive data
- Restrict file permissions: `chmod 600 frank_vision_helmet_pizero.py`
- Regularly update dependencies: `pip install --upgrade -r requirements.txt`

## 🚦 Next Steps

1. Test individual components before running the full application
2. Configure API keys from Google and Twilio
3. Add your own contacts to the CONTACTS dictionary
4. Test locally before setting up as a service
5. Monitor logs to ensure smooth operation

---

**Happy coding! 🚀 Frank is ready to see and assist!**
