"""
Frank Vision Helmet - Raspberry Pi Zero W Edition
A voice-controlled AI assistant with vision capabilities for Pi Zero W
Features: Wake word detection, vision processing, voice synthesis, LED status indicators, Twilio calls
"""

import cv2
import speech_recognition as sr
from gtts import gTTS
import os
import RPi.GPIO as GPIO
import datetime
import time
from twilio.rest import Client
import logging
from pathlib import Path

try:
    from google import genai
    import PIL.Image
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

# ---------- LOGGING SETUP ----------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/pi/frank_helmet.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ---------- GPIO LED SETUP (Pi Zero W) ----------
# GPIO Pin assignments for LEDs
LED_PROGRAM = 17      # Green LED - Program Status
LED_MIC_ERROR = 27    # Red LED - Microphone Error
LED_VIDEO_ERROR = 22  # Yellow LED - Video/Vision Error

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Initialize LED pins as output
for led_pin in [LED_PROGRAM, LED_MIC_ERROR, LED_VIDEO_ERROR]:
    GPIO.setup(led_pin, GPIO.OUT)
    GPIO.output(led_pin, GPIO.LOW)

logger.info("GPIO LEDs initialized successfully")

def led_on(pin):
    """Turn on an LED"""
    try:
        GPIO.output(pin, GPIO.HIGH)
    except Exception as e:
        logger.error(f"Error turning on LED {pin}: {e}")

def led_off(pin):
    """Turn off an LED"""
    try:
        GPIO.output(pin, GPIO.LOW)
    except Exception as e:
        logger.error(f"Error turning off LED {pin}: {e}")

def blink_led(pin, times=3, interval=0.3):
    """Blink LED multiple times"""
    try:
        for _ in range(times):
            led_on(pin)
            time.sleep(interval)
            led_off(pin)
            time.sleep(interval)
    except Exception as e:
        logger.error(f"Error blinking LED {pin}: {e}")

# ---------- SETUP KEYS & CLIENTS ----------
# 🔴 REPLACE WITH YOUR ACTUAL KEYS
API_KEY ='Your Google Gemini API Key'  # Google Gemini API
TWILIO_ACCOUNT_SID = "Your Twilio Account SID"
TWILIO_AUTH_TOKEN = "Your Twilio Auth Token"
TWILIO_PHONE_NUMBER = "Your Twilio Phone Number"  # Your Twilio trial number

# Initialize Gemini Client
if GENAI_AVAILABLE:
    try:
        genai_client = genai.Client(api_key=API_KEY)
        MODEL_ID = "gemini-2.0-flash"
        logger.info("Google Genai client initialized")
        led_on(LED_PROGRAM)  # Turn on program LED on startup
    except Exception as e:
        logger.error(f"Failed to initialize Genai client: {e}")
        blink_led(LED_VIDEO_ERROR, times=5)
        GENAI_AVAILABLE = False

# Initialize Twilio Client
try:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    logger.info("Twilio client initialized")
except Exception as e:
    logger.error(f"Failed to initialize Twilio client: {e}")
    blink_led(LED_VIDEO_ERROR, times=3)

# ---------- CONTACTS DATABASE ----------
CONTACTS = {
    "sriram": {
        "phone": "+918148624912",
        "greeting": "Hello Shriram, this is Frank calling you."
    },
    "shriram": {
        "phone": "+918148624912",
        "greeting": "Hello Shriram, this is Frank calling you."
    },
    # Add more contacts here
}

# ---------- SPEAK USING gTTS ----------
def speak(text, save_path="frank.mp3"):
    """Convert text to speech and play it"""
    print(f"Frank: {text}")
    logger.info(f"Speaking: {text}")
    
    try:
        # Generate speech
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(save_path)
        
        # Play on Pi Zero W (using alsa or pulseaudio)
        if os.name != "nt":  # Not Windows
            # Try multiple approaches for Pi audio
            play_commands = [
                f"aplay {save_path} 2>/dev/null",  # ALSA (most common on Pi)
                f"mpg123 {save_path} 2>/dev/null",  # MPG123
                f"mpv {save_path} 2>/dev/null",    # MPV (if installed)
            ]
            
            success = False
            for cmd in play_commands:
                result = os.system(cmd)
                if result == 0:
                    success = True
                    break
            
            if not success:
                logger.warning("Could not play audio with any player")
        else:
            os.system(f"start {save_path}")
            
    except Exception as e:
        logger.error(f"Speech Error: {e}")
        blink_led(LED_VIDEO_ERROR, times=2)

# ---------- CAMERA CAPTURE ----------
def capture_image(output_path="vision.jpg"):
    """Capture image from camera"""
    led_on(LED_PROGRAM)
    
    try:
        cap = cv2.VideoCapture(0)
        
        # Pi Zero W camera settings for better performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        cap.set(cv2.CAP_PROP_FPS, 15)
        
        time.sleep(1)  # Allow camera to warm up
        
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            # Compress image for faster processing
            cv2.imwrite(output_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            logger.info(f"Image captured: {output_path}")
            return output_path
        else:
            logger.error("Failed to capture image")
            blink_led(LED_VIDEO_ERROR, times=3)
            return None
            
    except Exception as e:
        logger.error(f"Camera capture error: {e}")
        blink_led(LED_VIDEO_ERROR, times=5)
        return None

# ---------- SPEECH RECOGNITION ----------
def listen_for_wake_word(timeout=5):
    """Listen for user input with wake word detection"""
    led_on(LED_PROGRAM)
    
    try:
        r = sr.Recognizer()
        r.dynamic_energy_threshold = True
        
        with sr.Microphone() as source:
            # Adjust for ambient noise
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("🎤 Listening...")
            logger.info("Listening for input")
            
            try:
                # Listen with timeout
                audio = r.listen(source, timeout=timeout, phrase_time_limit=4)
                
                # Recognize speech
                text = r.recognize_google(audio).lower()
                logger.info(f"Recognized: {text}")
                return text
                
            except sr.UnknownValueError:
                logger.warning("Could not understand audio")
                return ""
            except sr.RequestError as e:
                logger.error(f"Speech recognition service error: {e}")
                blink_led(LED_MIC_ERROR, times=3)
                return ""
            except sr.Timeout:
                logger.info("Listening timeout")
                return ""
                
    except Exception as e:
        logger.error(f"Microphone error: {e}")
        blink_led(LED_MIC_ERROR, times=5)
        return ""

# ---------- VISION PROCESSING ----------
def process_vision(user_input):
    """Process image with Gemini Vision"""
    if not GENAI_AVAILABLE:
        speak("Vision system is not available. Please check your API key.")
        blink_led(LED_VIDEO_ERROR, times=3)
        return
    
    try:
        speak("One moment, I am looking.")
        led_on(LED_PROGRAM)
        
        # Capture image
        img_path = capture_image()
        if not img_path or not os.path.exists(img_path):
            speak("I could not access the camera.")
            blink_led(LED_VIDEO_ERROR, times=4)
            return
        
        # Open image
        img = PIL.Image.open(img_path)
        
        # Create prompt
        prompt = (
            f"User said: '{user_input}'. "
            "User name: Chinu. "
            f"Today: '{datetime.datetime.now().strftime('%A, %B %d, %Y')}'. "
            "Please describe what you see in this image. "
            "If there's text on paper or screens, read it out clearly. "
            "Keep your response short and clear, suitable for someone with visual impairment."
        )
        
        logger.info("Processing image with Gemini Vision")
        
        # Call Gemini Vision API
        response = genai_client.models.generate_content(
            model=MODEL_ID,
            contents=[prompt, img]
        )
        
        speak(response.text)
        led_off(LED_PROGRAM)
        
    except FileNotFoundError as e:
        logger.error(f"Image file not found: {e}")
        speak("Image file not found.")
        blink_led(LED_VIDEO_ERROR, times=4)
    except Exception as e:
        logger.error(f"Vision processing error: {e}")
        speak("I am having trouble with my vision system.")
        blink_led(LED_VIDEO_ERROR, times=5)

# ---------- MAKE A CALL ----------
def make_call(contact_name):
    """Make a call via Twilio"""
    contact_name = contact_name.lower().strip()
    
    if contact_name not in CONTACTS:
        speak(f"Sorry, I don't have {contact_name} in my contacts.")
        logger.warning(f"Contact not found: {contact_name}")
        return
    
    contact = CONTACTS[contact_name]
    
    try:
        logger.info(f"Initiating call to {contact_name}")
        
        call = twilio_client.calls.create(
            twiml=f"<Response><Say>{contact['greeting']}</Say></Response>",
            to=contact['phone'],
            from_=TWILIO_PHONE_NUMBER
        )
        
        logger.info(f"Call initiated: {call.sid}")
        speak(f"OK, calling {contact_name} now.")
        blink_led(LED_PROGRAM, times=2)
        
    except Exception as e:
        logger.error(f"Call error: {e}")
        speak(f"Sorry, I could not make the call to {contact_name}.")
        blink_led(LED_MIC_ERROR, times=3)

# ---------- GENERAL CHAT ----------
def process_chat(user_input):
    """Process general chat requests"""
    if not GENAI_AVAILABLE:
        speak("I'm not configured properly. Please check your API key.")
        return
    
    try:
        led_on(LED_PROGRAM)
        
        prompt = (
            f"User said: '{user_input}'. "
            "User name: Chinu. "
            f"Time: '{datetime.datetime.now().strftime('%I:%M %p')}'. "
            f"Date: '{datetime.datetime.now().strftime('%A, %B %d, %Y')}'. "
            "Please respond in a friendly manner. Keep your response short and clear. "
            "Make it suitable for someone with visual impairment."
        )
        
        logger.info(f"Processing chat: {user_input}")
        
        response = genai_client.models.generate_content(
            model=MODEL_ID,
            contents=[prompt]
        )
        
        speak(response.text)
        led_off(LED_PROGRAM)
        
    except Exception as e:
        logger.error(f"Chat processing error: {e}")
        speak("I am having trouble processing your request.")
        blink_led(LED_VIDEO_ERROR, times=3)

# ---------- MAIN LOOP ----------
def main():
    """Main program loop"""
    try:
        # Startup sequence
        blink_led(LED_PROGRAM, times=2, interval=0.2)
        speak("Frank is online.")
        
        logger.info("=== Frank Vision Helmet Started ===")
        
        while True:
            try:
                # Listen for input
                user_input = listen_for_wake_word()
                
                if not user_input:
                    continue
                
                # Check for wake word
                if "frank" in user_input or "hello" in user_input:
                    logger.info(f"Wake word detected: {user_input}")
                    blink_led(LED_PROGRAM, times=1)
                    
                    # ===== VISION TASK =====
                    if any(keyword in user_input for keyword in 
                           ["in front of me", "read", "what is on the paper", 
                            "what is on the screen", "in front", "see", "look", "what do you see"]):
                        process_vision(user_input)
                    
                    # ===== MAKE A CALL =====
                    elif "make a call" in user_input or "call" in user_input:
                        # Extract contact name
                        for contact in CONTACTS.keys():
                            if contact in user_input:
                                make_call(contact)
                                break
                        else:
                            speak("Sorry, I need a contact name to make a call.")
                    
                    # ===== GENERAL CHAT =====
                    else:
                        process_chat(user_input)
                
                # Stop command
                elif "stop" in user_input or "goodbye" in user_input:
                    speak("Goodbye.")
                    logger.info("Stop command received")
                    break
                    
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received")
                break
            except Exception as e:
                logger.error(f"Loop error: {e}")
                blink_led(LED_VIDEO_ERROR, times=2)
                time.sleep(1)
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        blink_led(LED_VIDEO_ERROR, times=10)
    
    finally:
        # Cleanup
        logger.info("Shutting down Frank Vision Helmet")
        speak("Goodbye.")
        
        # Turn off all LEDs
        for led_pin in [LED_PROGRAM, LED_MIC_ERROR, LED_VIDEO_ERROR]:
            led_off(led_pin)
        
        # Cleanup GPIO
        GPIO.cleanup()
        logger.info("GPIO cleaned up")

if __name__ == "__main__":
    main()
