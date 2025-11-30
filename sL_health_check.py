import subprocess
import platform
import sys
import re 
from datetime import datetime
from typing import Optional # The 'tuple' import was removed to fix the error

# --- Configuration ---
# Target a reliable, well-known IP address for a general internet health check.
TARGET_HOST = "8.8.8.8" 

def check_network_health(host: str) -> tuple[bool, Optional[int]]:
    """
    Executes a ping command and checks the return code to determine network health.
    Extracts and returns the average latency (ping time) in milliseconds.
    
    Args:
        host: The IP address or hostname to ping.
        
    Returns:
        A tuple: (is_healthy: bool, avg_latency_ms: int or None)
    """
    print(f"\n🌐 Initiating Network Vibe Check at {datetime.now().strftime('%H:%M:%S')}")
    print(f"📡 Pinging target host: {host}...")

    # Determine the correct ping command based on the operating system
    if platform.system().lower() == "windows":
        command = ["ping", "-n", "1", host]
    else:
        command = ["ping", "-c", "1", host]

    try:
        # Execute the command and wait for it to finish
        result = subprocess.run(
            command,              # The command and its arguments
            capture_output=True,  # Capture the output and errors
            text=True,            # Decode output as text
            check=True            # Raise an error only if the ping command itself fails
        )
        
        if result.returncode == 0:
            
            # Robust Regex: Allows for variable spacing and searches across multiple lines (re.DOTALL)
            match = re.search(r'Average\s*=\s*(\d+)ms', result.stdout, re.IGNORECASE | re.DOTALL)

            if match:
                avg_time = int(match.group(1)) # Extract the number of milliseconds
                return True, avg_time
            else:
                # If ping succeeded but the average time line wasn't found (e.g., non-English OS)
                return True, None
        else:
            return False, None

    except FileNotFoundError:
        print("🚨 Error: Ping command not found. Is your system's PATH set up correctly?")
        return False, None
    except subprocess.CalledProcessError:
        # This catches non-zero return codes (ping failed to reach host)
        return False, None
    except Exception as e:
        print(f"🚨 An unexpected error occurred: {e}")
        return False, None

# --- Main Execution ---
if __name__ == "__main__":
    # The function returns two values, which are unpacked here
    is_healthy, avg_latency_ms = check_network_health(TARGET_HOST)
    
    if is_healthy:
        # Check if we successfully extracted the latency data 
        if avg_latency_ms is not None:
            # Positive, data-driven report!
            print(f"\n✅ Network Health: Optimal! Latency: {avg_latency_ms}ms")
            
            # Set a custom Vibe Status based on performance (Tier 1 analysis)
            if avg_latency_ms < 50:
                 print(f"✨ Vibe Status: Blazing fast connectivity achieved. Ready for high-speed work.")
            else:
                 print(f"✨ Vibe Status: Stable connectivity achieved. Ready for work.")

        else:
            print("\n✅ Network Health: Optimal! (Latency data not found—may be non-standard ping output)")
            print(f"✨ Vibe Status: Seamless connectivity achieved. Ready for work.")
    else:
        print("\n⚠️ Network Warning: Host Unreachable.")
        print(f"🚨 Vibe Status: Investigate system or Wi-Fi setup immediately (Tier 1 Diagnostic Step).")