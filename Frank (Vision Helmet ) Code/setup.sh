#!/bin/bash

# Frank Vision Helmet - Installation Script for Raspberry Pi Zero W
# Run this script to automatically set up Frank

set -e  # Exit on error

echo "=========================================="
echo "Frank Vision Helmet - Setup Script"
echo "Raspberry Pi Zero W Edition"
echo "=========================================="
echo ""

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/device-tree/model 2>/dev/null; then
    echo "⚠ Warning: This script is designed for Raspberry Pi"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Step 1: System Update
echo "Step 1: Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y
echo "✓ System updated"
echo ""

# Step 2: Install system dependencies
echo "Step 2: Installing system dependencies..."
echo "  Installing Python tools..."
sudo apt-get install -y python3-pip python3-dev python3-venv

echo "  Installing audio libraries..."
sudo apt-get install -y alsa-utils portaudio19-dev

echo "  Installing camera support..."
sudo apt-get install -y libatlas-base-dev libjasper-dev libtiff5 libjasper1 libharfbuzz0b libwebp6

echo "  Installing OpenCV dependencies..."
sudo apt-get install -y libopenjp2-7 libtiff5 libjasper1 libharfbuzz0b libwebp6

echo "  Installing utilities..."
sudo apt-get install -y git wget curl libssl-dev
echo "✓ System dependencies installed"
echo ""

# Step 3: Create virtual environment
echo "Step 3: Creating Python virtual environment..."
if [ ! -d "$HOME/frank_env" ]; then
    python3 -m venv ~/frank_env
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Step 4: Activate virtual environment and install Python packages
echo "Step 4: Installing Python packages..."
source ~/frank_env/bin/activate
pip install --upgrade pip setuptools wheel

echo "  Installing core packages..."
pip install RPi.GPIO
pip install opencv-python
pip install SpeechRecognition
pip install pyaudio
pip install gTTS
pip install twilio
pip install google-generativeai
pip install Pillow
echo "✓ Python packages installed"
echo ""

# Step 5: Clone repository (optional)
read -p "Do you want to clone the Frank repository? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Step 5: Cloning repository..."
    read -p "Enter your GitHub username: " github_user
    git clone https://github.com/$github_user/frank-vision-helmet.git ~/frank-vision-helmet
    cd ~/frank-vision-helmet
    echo "✓ Repository cloned"
else
    echo "Step 5: Skipping repository clone"
    mkdir -p ~/frank-vision-helmet
    cd ~/frank-vision-helmet
fi
echo ""

# Step 6: Create systemd service (optional)
read -p "Do you want to set up autostart service? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Step 6: Setting up systemd service..."
    
    # Copy main script if not already present
    if [ ! -f "frank_vision_helmet_pizero.py" ]; then
        echo "Note: Please add frank_vision_helmet_pizero.py to this directory"
    fi
    
    # Create service file
    sudo tee /etc/systemd/system/frank.service > /dev/null << EOF
[Unit]
Description=Frank Vision Helmet Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=$HOME/frank-vision-helmet
ExecStart=$HOME/frank_env/bin/python3 $HOME/frank-vision-helmet/frank_vision_helmet_pizero.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
    
    sudo systemctl daemon-reload
    sudo systemctl enable frank
    echo "✓ Systemd service created"
    echo "  Start Frank: sudo systemctl start frank"
    echo "  Stop Frank: sudo systemctl stop frank"
    echo "  View logs: journalctl -u frank -f"
else
    echo "Step 6: Skipping systemd service setup"
fi
echo ""

# Step 7: Camera enablement reminder
echo "Step 7: Camera enablement"
echo "  Make sure to enable the camera:"
echo "  1. Run: sudo raspi-config"
echo "  2. Go to: Interface Options → Camera → Enable"
echo "  3. Reboot: sudo reboot"
echo ""

# Step 8: Configuration reminder
echo "Step 8: Configuration reminder"
echo "  Before running Frank, you need to:"
echo ""
echo "  1. Add API credentials to frank_vision_helmet_pizero.py:"
echo "     - Google Gemini API key (from aistudio.google.com)"
echo "     - Twilio Account SID and Auth Token"
echo ""
echo "  2. Edit the CONTACTS dictionary with your phone numbers"
echo ""
echo "  3. Test components:"
echo "     source ~/frank_env/bin/activate"
echo "     python3 test_leds.py"
echo "     python3 test_camera.py"
echo "     python3 test_microphone.py"
echo ""
echo "  4. Run Frank:"
echo "     python3 frank_vision_helmet_pizero.py"
echo ""

# Final message
echo "=========================================="
echo "✓ Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Edit frank_vision_helmet_pizero.py with your API keys"
echo "  2. Run the test scripts to verify hardware"
echo "  3. Start Frank with: python3 frank_vision_helmet_pizero.py"
echo ""
echo "For more information, see FRANK_SETUP_GUIDE.md"
echo ""
