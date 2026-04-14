import sys
import time
import subprocess
import os

SIGNAL_FILE = "start_signal.flag"

def main():
    if len(sys.argv) < 2:
        print("Usage: python worker.py <seed>")
        sys.exit(1)
    
    seed = sys.argv[1]
    print(f"Worker initialized with seed {seed}.")
    print(f"Waiting for signal from sender.py (watching for '{SIGNAL_FILE}')...")
    
    # Optional cleanup on startup in case a stale flag file was left behind
    if os.path.exists(SIGNAL_FILE):
        try:
            os.remove(SIGNAL_FILE)
        except OSError:
            pass

    while True:
        # Wait for the signal file to be created
        while not os.path.exists(SIGNAL_FILE):
            time.sleep(0.1) # Fast polling
            
        print(f"\nSignal received! Starting test.py with seed {seed}...\n" + "-"*40)
        
        # Run the test.py script, passing "input100People" as the first arg and the seed as the second
        # Assumes test.py has been modified to accept the seed as sys.argv[2]
        subprocess.run(["pypy3", "test.py", "input100PeopleMoreRandom", seed])
        time.sleep(2)

if __name__ == "__main__":
    main()
