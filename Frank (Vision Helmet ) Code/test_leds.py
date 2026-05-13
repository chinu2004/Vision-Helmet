"""
Frank Vision Helmet - LED Test Script
Test your 3 LEDs before running the main program
Run this script to verify GPIO connections
"""

import RPi.GPIO as GPIO
import time
import sys

# LED Pin Configuration
LED_PROGRAM = 17      # Green LED - Program Status
LED_MIC_ERROR = 27    # Red LED - Microphone Error
LED_VIDEO_ERROR = 22  # Yellow LED - Video/Vision Error

LED_INFO = {
    LED_PROGRAM: "Green LED (Program Status)",
    LED_MIC_ERROR: "Red LED (Microphone Error)",
    LED_VIDEO_ERROR: "Yellow LED (Video/Vision Error)"
}

def setup_gpio():
    """Initialize GPIO"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    for pin in [LED_PROGRAM, LED_MIC_ERROR, LED_VIDEO_ERROR]:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    
    print("✓ GPIO initialized")

def test_led(pin, name):
    """Test a single LED"""
    print(f"\nTesting {name} (GPIO {pin})...")
    
    try:
        # Turn on
        GPIO.output(pin, GPIO.HIGH)
        print(f"  ✓ LED turned ON")
        time.sleep(1)
        
        # Blink 3 times
        for i in range(3):
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.3)
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.3)
        
        # Turn off
        GPIO.output(pin, GPIO.LOW)
        print(f"  ✓ LED blinked 3 times")
        print(f"  ✓ LED turned OFF")
        print(f"  ✓ {name} is working!")
        return True
        
    except Exception as e:
        print(f"  ✗ Error testing {name}: {e}")
        return False

def test_all_leds():
    """Test all LEDs together"""
    print("\n" + "="*50)
    print("Testing ALL LEDs simultaneously...")
    print("="*50)
    
    try:
        for pin in [LED_PROGRAM, LED_MIC_ERROR, LED_VIDEO_ERROR]:
            GPIO.output(pin, GPIO.HIGH)
        
        print("✓ All LEDs are ON")
        time.sleep(2)
        
        for pin in [LED_PROGRAM, LED_MIC_ERROR, LED_VIDEO_ERROR]:
            GPIO.output(pin, GPIO.LOW)
        
        print("✓ All LEDs are OFF")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Main test routine"""
    print("="*50)
    print("Frank Vision Helmet - LED Test Script")
    print("="*50)
    
    try:
        # Setup
        setup_gpio()
        
        # Test individual LEDs
        results = {}
        for pin, name in LED_INFO.items():
            results[pin] = test_led(pin, name)
            time.sleep(0.5)
        
        # Test all together
        test_all_leds()
        
        # Summary
        print("\n" + "="*50)
        print("TEST SUMMARY")
        print("="*50)
        
        all_passed = True
        for pin, name in LED_INFO.items():
            status = "✓ PASS" if results[pin] else "✗ FAIL"
            print(f"{status}: {name}")
            if not results[pin]:
                all_passed = False
        
        print("="*50)
        
        if all_passed:
            print("\n✓ All LEDs are working correctly!")
            print("You can now run: python3 frank_vision_helmet_pizero.py")
            return 0
        else:
            print("\n✗ Some LEDs failed. Check your connections:")
            print("  GPIO 17 (Pin 11) → Green LED")
            print("  GPIO 27 (Pin 13) → Red LED")
            print("  GPIO 22 (Pin 15) → Yellow LED")
            print("\nEach LED needs a 220Ω resistor to ground.")
            return 1
    
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        return 1
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        return 1
    finally:
        GPIO.cleanup()
        print("\n✓ GPIO cleaned up")

if __name__ == "__main__":
    sys.exit(main())
