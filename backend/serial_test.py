import serial
import time

PORT = "COM6"      # Change if your COM port is different
BAUD = 115200

esp = serial.Serial(PORT, BAUD, timeout=1)

time.sleep(2)  # Wait for ESP32 reset

commands = ["INVALID", "NORMAL", "BENIGN", "MALIGNANT"]

for cmd in commands:
    print(f"Sending: {cmd}")
    esp.write((cmd + "\n").encode())
    time.sleep(3)

esp.close()
print("Test Complete")