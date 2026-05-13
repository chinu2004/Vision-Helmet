"""
Frank Vision Helmet - Microphone Test Script
Test microphone and speech recognition before running main program
"""

import speech_recognition as sr
import sys

def test_microphone():
    """Test microphone input"""
    print("="*50)
    print("Frank Vision Helmet - Microphone Test")
    print("="*50)
    
    try:
        print("\n1. Initializing speech recognizer...")
        r = sr.Recognizer()
        print("✓ Recognizer initialized")
        
        print("\n2. Listing available microphones...")
        mics = sr.Microphone.list_microphone_indexes()
        if not mics:
            print("✗ No microphones detected")
            print("\nTroubleshooting:")
            print("  1. Check USB microphone/audio interface connection")
            print("  2. Run: arecord -l")
            print("  3. Check audio configuration: alsamixer")
            return False
        
        for i in mics:
            try:
                mic_name = sr.Microphone.list_working_microphones()[i]
                print(f"  Microphone {i}: {mic_name}")
            except:
                print(f"  Microphone {i}: Available")
        
        print("✓ Microphones detected")
        
        print("\n3. Testing microphone input...")
        with sr.Microphone() as source:
            print("  Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            print(f"  Energy threshold: {r.energy_threshold}")
            print("  Dynamic energy threshold: ON")
            
            print("\n  🎤 Listening for 5 seconds...")
            print("  Please speak something...")
            
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=4)
                print(f"✓ Audio captured: {len(audio.get_wav_data())} bytes")
                
            except sr.Timeout:
                print("✗ Timeout - no audio detected")
                print("\nTroubleshooting:")
                print("  1. Check microphone volume: alsamixer")
                print("  2. Test with: arecord -D default test.wav")
                print("  3. Check microphone connection")
                return False
        
        print("\n4. Testing speech recognition...")
        try:
            print("  Recognizing audio...")
            text = r.recognize_google(audio)
            print(f"✓ Recognized text: '{text}'")
            
        except sr.UnknownValueError:
            print("⚠ Audio was captured but not recognized")
            print("  (This is normal if you didn't speak clearly)")
            print("✓ Microphone and audio capture working")
            return True
            
        except sr.RequestError as e:
            print(f"✗ Speech recognition service error: {e}")
            print("\nTroubleshooting:")
            print("  1. Check internet connection: ping google.com")
            print("  2. Check if Google Speech API is available")
            return False
        
        print("\n" + "="*50)
        print("✓ Microphone test PASSED!")
        print("="*50)
        print("\nYou can now run: python3 frank_vision_helmet_pizero.py")
        return True
        
    except ImportError:
        print("✗ speech_recognition module not installed")
        print("  Install with: pip install SpeechRecognition")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nTroubleshooting:")
        print("  1. Install dependencies:")
        print("     pip install SpeechRecognition pyaudio")
        print("  2. Check audio system: aplay -l")
        print("  3. Test microphone: arecord test.wav")
        return False

if __name__ == "__main__":
    success = test_microphone()
    sys.exit(0 if success else 1)
