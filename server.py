import time
import random
import threading
import datetime
from typing import List, Optional

from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field

# Before running, you must install the required libraries.
# Open your terminal or command prompt in this directory and run:
# pip install -r requirements.txt

try:
    from pynput.mouse import Controller, Button
except ImportError:
    print("pynput library not found.")
    print("Please install dependencies by running: pip install -r requirements.txt")
    exit()

# --- Application Setup ---
app = FastAPI()
mouse = Controller()

# --- State Management ---
# Using a class to hold state is cleaner than global variables
class AppState:
    def __init__(self):
        self.is_clicking = False
        self.click_log: List[str] = []
        self.click_thread: Optional[threading.Thread] = None
        self.interval_mode = "fixed"
        self.min_interval = 1.0
        self.max_interval = 1.0

state = AppState()

# --- Pydantic Models for API Data ---
class StartRequest(BaseModel):
    mode: str = Field("fixed", description="'fixed' or 'random'")
    min_interval: float = Field(1.0, description="Minimum click interval in seconds")
    max_interval: float = Field(1.0, description="Maximum click interval in seconds (used in random mode)")

class StatusResponse(BaseModel):
    is_clicking: bool
    log_count: int
    mode: str
    min_interval: float
    max_interval: float

# --- Core Clicker Logic ---
def clicker_worker():
    """This function runs in a separate thread and performs the clicks."""
    while state.is_clicking:
        # Perform the click
        mouse.click(Button.left, 1)
        
        # Log the click with a timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        state.click_log.append(timestamp)
        print(f"Clicked at {timestamp}")

        # Determine sleep time based on mode
        if state.interval_mode == "random":
            sleep_duration = random.uniform(state.min_interval, state.max_interval)
        else: # fixed
            sleep_duration = state.min_interval
        
        time.sleep(sleep_duration)
    print("Clicker thread stopped.")

# --- API Endpoints ---
@app.get("/", response_class=HTMLResponse)
async def get_root():
    """Serves the main web interface."""
    return FileResponse('index.html')

@app.post("/api/start")
async def start_clicking(request: StartRequest, background_tasks: BackgroundTasks):
    """Starts the auto-clicker."""
    if state.is_clicking:
        return {"status": "error", "message": "Clicker is already running."}

    # Update state from the request
    state.interval_mode = request.mode
    state.min_interval = request.min_interval
    state.max_interval = request.max_interval
    
    # Start the clicker
    state.is_clicking = True
    state.click_thread = threading.Thread(target=clicker_worker, daemon=True)
    state.click_thread.start()
    
    print(f"Starting clicker. Mode: {request.mode}, Min: {request.min_interval}, Max: {request.max_interval}")
    return {"status": "success", "message": "Clicker started."}

@app.post("/api/stop")
async def stop_clicking():
    """Stops the auto-clicker."""
    if not state.is_clicking:
        return {"status": "error", "message": "Clicker is not running."}
    
    state.is_clicking = False
    # The thread is a daemon, so we don't strictly need to join it,
    # but it's good practice if you want to ensure cleanup.
    # For simplicity, we'll let it exit on its own.
    print("Stopping clicker.")
    return {"status": "success", "message": "Clicker stopped."}

@app.get("/api/status", response_model=StatusResponse)
async def get_status():
    """Gets the current status and configuration of the clicker."""
    return StatusResponse(
        is_clicking=state.is_clicking,
        log_count=len(state.click_log),
        mode=state.interval_mode,
        min_interval=state.min_interval,
        max_interval=state.max_interval
    )

@app.get("/api/log")
async def get_log():
    """Gets the list of click timestamps."""
    return {"log": state.click_log}

@app.post("/api/test_click")
async def test_click():
    """Performs a single test click."""
    print("Performing a test click.")
    mouse.click(Button.left, 1)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    state.click_log.append(f"{timestamp} (Test)")
    return {"status": "success", "message": "Test click performed."}

@app.delete("/api/log")
async def clear_log():
    """Clears the click log."""
    state.click_log.clear()
    print("Click log cleared.")
    return {"status": "success", "message": "Log cleared."}

# --- Main Entry Point ---
if __name__ == "__main__":
    import uvicorn
    print("--- Welcome to ClickForge Server ---")
    print("Starting server...")
    print("To access the user interface, open your web browser and go to:")
    print("http://127.0.0.1:8000")
    print("\nTo access from your phone or another device on the same network,")
    print("you will need to use your computer's local IP address.")
    print("Example: http://192.168.1.10:8000")
    print("------------------------------------")
    # Host on 0.0.0.0 to make it accessible from other devices on the network
    uvicorn.run(app, host="0.0.0.0", port=8000)
