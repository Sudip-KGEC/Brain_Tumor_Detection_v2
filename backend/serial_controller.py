import serial
import time

class ESP32Controller:
    def __init__(self, port="COM6", baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.serial_conn = None

    def send_command(self, command: str):
        print(f"\n🔌 Opening temporary connection to {self.port}...")
        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
            
            # 1. PREVENT FREEZE: Force Windows to let the ESP32 boot normally
            self.serial_conn.setDTR(False)
            self.serial_conn.setRTS(False)
            
            print("⏳ Waiting 3 seconds for ESP32 to boot...")
            time.sleep(3)
            
            # 2. THE WAKE-UP CALL: Tap the mic to clear the ESP32's throat
            self.serial_conn.write(b'\n')
            self.serial_conn.flush()
            time.sleep(0.2) # Wait a fraction of a second for it to snap to attention
            
            # 3. Send the REAL command
            formatted_command = f"{command.upper()}\n"
            self.serial_conn.write(formatted_command.encode('utf-8'))
            self.serial_conn.flush()
            print(f"📡 [HARDWARE] Successfully pushed '{command.upper()}' to ESP32")
            
            # 4. Listen for the ESP32's reply
            time.sleep(2)
            if self.serial_conn.in_waiting > 0:
                esp_reply = self.serial_conn.read(self.serial_conn.in_waiting).decode('utf-8', errors='ignore').strip()
                print(f"🎤 [ESP32 SAYS]:\n{esp_reply}")
            else:
                print("🔇 [ESP32 SAYS]: (Dead silence... it didn't respond)")
                
            return True
            
        except Exception as e:
            print(f"❌ Error communicating with ESP32: {e}")
            return False
        finally:
            # 5. ALWAYS close the door behind us
            if self.serial_conn and self.serial_conn.is_open:
                self.serial_conn.close()
                print("🛑 Serial connection closed safely.\n")

hardware = ESP32Controller(port="COM6")