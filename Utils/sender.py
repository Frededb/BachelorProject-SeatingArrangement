import os
import time

SIGNAL_FILE = "start_signal.flag"

def main():
    print("Preparing to send start signal...")
    
    # Create the signal file
    with open(SIGNAL_FILE, "w") as f:
        f.write("start")
        
    print(f"Signal sent! (Created {SIGNAL_FILE})")
    print("Workers should now be starting.")
    
    # Wait a moment to ensure all workers detect it, then clean up
    time.sleep(2)
    try:
        if os.path.exists(SIGNAL_FILE):
            os.remove(SIGNAL_FILE)
            print("Cleaned up signal file.")
    except Exception as e:
        print(f"Failed to clean up: {e}")

if __name__ == "__main__":
    main()
