from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import serial
import time

# --- CONFIGURATION ---
PORT = "COM6"  
BAUD = 115200

# Global variable to hold the serial connection
esp = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP LOGIC ---
    global esp
    print(f"🔌 Connecting to ESP32 on {PORT}...")
    try:
        # Open connection ONCE when the server starts
        esp = serial.Serial(PORT, BAUD, timeout=1)
        print("⏳ Waiting 3 seconds for ESP32 to boot...")
        time.sleep(3)
        print("✅ Backend connected to ESP32 successfully!")
    except serial.SerialException as e:
        print(f"❌ SERIAL ERROR: Could not connect to {PORT}. Is another program using it?")
        esp = None
        
    yield # The FastAPI server runs while paused here
    
    # --- SHUTDOWN LOGIC ---
    if esp and esp.is_open:
        esp.close()
        print("🛑 Serial connection closed.")

# Initialize app with the new lifespan manager
app = FastAPI(title="ESP32 Backend Test", lifespan=lifespan)

@app.post("/api/send-command/{command}")
def send_command(command: str):
    global esp
    
    # 1. Check if hardware is connected
    if not esp or not esp.is_open:
        raise HTTPException(status_code=500, detail="Backend is not connected to ESP32.")
    
    # 2. Validate command
    valid_commands = ["NORMAL", "GLIOMA", "MENINGIOMA", "PITUITARY", "INVALID"]
    command_upper = command.upper()
    
    if command_upper not in valid_commands:
        raise HTTPException(status_code=400, detail=f"Command '{command}' is not recognized.")

    # 3. Send command to hardware
    try:
        formatted_command = f"{command_upper}\n"
        esp.write(formatted_command.encode('utf-8'))
        esp.flush()
        print(f"📡 Backend successfully sent: {command_upper}")
        return {"status": "success", "command_sent": command_upper}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write to serial: {str(e)}")