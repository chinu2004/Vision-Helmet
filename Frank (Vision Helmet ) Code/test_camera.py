"""
Frank Vision Helmet - Camera Test Script
Diagnose camera functionality before running main program
"""

import cv2
import sys
import time

def test_camera():
    """Test camera capture"""
    print("="*50)
    print("Frank Vision Helmet - Camera Test")
    print("="*50)
    
    try:
        print("\n1. Initializing camera...")
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("✗ Failed to open camera")
            print("\nTroubleshooting:")
            print("  1. Check if camera is enabled: sudo raspi-config")
            print("     → Interface Options → Camera → Enable")
            print("  2. Reboot: sudo reboot")
            print("  3. Check connections (ribbon cable)")
            print("  4. Test with: raspistill -o test.jpg")
            return False
        
        print("✓ Camera opened successfully")
        
        # Set camera properties for Pi Zero W
        print("\n2. Configuring camera for Pi Zero W...")
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        cap.set(cv2.CAP_PROP_FPS, 15)
        
        print(f"  Frame width: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}")
        print(f"  Frame height: {cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
        print(f"  FPS: {cap.get(cv2.CAP_PROP_FPS)}")
        print("✓ Camera configured")
        
        # Warm up camera
        print("\n3. Warming up camera...")
        for i in range(10):
            ret, frame = cap.read()
            if ret:
                print(f"  Frame {i+1}/10: {frame.shape}")
            time.sleep(0.1)
        print("✓ Camera warmed up")
        
        # Capture test image
        print("\n4. Capturing test image...")
        time.sleep(1)
        ret, frame = cap.read()
        
        if ret:
            cv2.imwrite("camera_test.jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            print(f"✓ Image captured: camera_test.jpg")
            print(f"  Resolution: {frame.shape}")
            print(f"  File size: {frame.nbytes / 1024:.1f} KB")
        else:
            print("✗ Failed to capture image")
            return False
        
        # Release camera
        cap.release()
        print("\n5. Releasing camera...")
        print("✓ Camera released")
        
        print("\n" + "="*50)
        print("✓ Camera test PASSED!")
        print("="*50)
        print("\nYou can now run: python3 frank_vision_helmet_pizero.py")
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nTroubleshooting:")
        print("  1. Check if OpenCV is installed correctly:")
        print("     pip install opencv-python")
        print("  2. Check if camera is enabled in raspi-config")
        print("  3. Check camera ribbon cable connection")
        cap.release()
        return False

if __name__ == "__main__":
    success = test_camera()
    sys.exit(0 if success else 1)
