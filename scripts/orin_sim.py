import serial
import time
import sys
import random

# CONFIGURATION
# e.g COM3
SERIAL_PORT = 'COM3' 
BAUD_RATE = 115200

def log_system(subsystem, status):
    timestamp = time.strftime("%H:%M:%S.000", time.localtime())
    print(f"[{timestamp}] [ORIN_CORE] {subsystem:<15} : \033[92m{status}\033[0m")

def log_error(message):
    timestamp = time.strftime("%H:%M:%S.000", time.localtime())
    print(f"[{timestamp}] [KERNEL_PANIC] \033[91m{message}\033[0m")

try:
    # Open connection to the USB-TTL adapter
    # We use the RTS pin to physically simulate the electrical heartbeat pulse
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
    print("\n--- INITIALIZING AUTONOMOUS DRIVING STACK ---\n")
    time.sleep(1)

    # PHASE 1: NORMAL OPERATION
    # Simulating a healthy 10ms control loop
    start_time = time.time()
    packet_count = 0
    
    while time.time() - start_time < 10: # Run normally for 10 seconds
        
        # 1. Toggle the Heartbeat (RTS Pin High/Low)
        # This sends a voltage pulse to STM32 PA0
        ser.setRTS(True)
        time.sleep(0.005) # 5ms High
        ser.setRTS(False)
        time.sleep(0.005) # 5ms Low (Total 10ms period)

        # 2. Print "Fake" ROS Logs to look cool on screen
        if packet_count % 50 == 0: # Every 500ms update console
            choices = ["Path Planner", "Lidar Processing", "Object Detection", "Velocity Control"]
            log_system(random.choice(choices), "NOMINAL")
        
        packet_count += 1

    # PHASE 2: THE CRASH
    # Simulating a Segmentation Fault / Freeze
    print("\n" + "="*40)
    log_error("CRITICAL: SEGMENTATION FAULT (core dumped)")
    log_error("Process ID 4022 terminated unexpectedy")
    log_error("HEARTBEAT STOPPED.")
    print("="*40 + "\n")

    # We stop toggling RTS. The line stays LOW.
    # The STM32 Window Watchdog is now ticking down...
    # T-Minus 20ms to Emergency Braking.
    
    ser.setRTS(False) 
    
    # Keep script alive just to hold the line low
    while True:
        time.sleep(1)

except serial.SerialException:
    print(f"Error: Could not open {SERIAL_PORT}. Check your USB adapter.")
except KeyboardInterrupt:
    print("\nSimulation aborted.")
