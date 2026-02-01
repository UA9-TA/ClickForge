# ClickForge 🖱️✨

ClickForge is a powerful, remotely-controlled auto-clicker built with Python and a web-based frontend. It allows you to configure and run an auto-clicker on a host machine and control it from any device with a web browser, such as your phone.

![ClickForge UI](https://i.imgur.com/your-screenshot-url.png)
*(Note: You can replace the image link above after you take a screenshot of the running application!)*

---

## Features

- **Multiple Clicking Modes:**
    - **Fixed Interval:** Clicks at a consistent, user-defined rate.
    - **Custom Random Interval:** Clicks at random intervals between a user-defined minimum and maximum.
    - **Simple Random Interval:** A no-fuss mode that clicks at random intervals between 5 and 59 seconds.
- **Remote Control UI:**
    - A sleek, mobile-friendly web interface to control the clicker.
    - Start, stop, and configure the clicker from your phone or any browser.
    - "Add to Home Screen" support for an app-like experience on mobile.
- **Live Feedback & Logging:**
    - Real-time status indicator with a "pulsing" animation when active.
    - A "Test Click" button that flashes with a random color for immediate feedback.
    - A live log that displays the timestamp of every click.
- **Cross-Platform:** The core application can run on Windows, macOS, and Linux (system permissions required).

## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn, Pynput
- **Frontend:** HTML, CSS, vanilla JavaScript

---

## Installation

**1. Clone the Repository**

First, get the project files onto your local machine. If you're using git, you can clone the repository:
```bash
git clone https://github.com/your-username/ClickForge.git
cd ClickForge
```

**2. Install Dependencies**

This project uses Python. Make sure you have Python 3.7+ installed.

Install all the required Python libraries using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

**3. Grant System Permissions (Crucial for macOS)**

Auto-clickers need permission to control your mouse. You will need to grant accessibility permissions to your terminal or code editor.

- **On macOS:**
    1. Go to **System Settings > Privacy & Security > Accessibility**.
    2. Click the `+` button and add your Terminal application (e.g., `Terminal.app`, `iTerm.app`).
    3. Make sure the toggle next to your terminal is **on**.
    4. **Important:** You may need to restart your terminal application after making this change.

---

## Usage

**1. Run the Server**

Navigate to the project directory in your terminal and run the server:
```bash
python3 server.py
```
The server will start, and you will see instructions in your terminal on how to connect.

**2. Access the Web UI**

- **On the same computer:** Open your web browser and go to `http://127.0.0.1:8000`.
- **From another device (like your phone):**
    1. Make sure your device is on the **same Wi-Fi network** as the computer running the server.
    2. Find your computer's Local IP Address (e.g., on macOS, go to **System Settings > Network**).
    3. Open the browser on your phone and navigate to `http://<YOUR-COMPUTER-IP-ADDRESS>:8000`. For example: `http://192.168.1.105:8000`.

**3. Use ClickForge!**

You can now use the web interface to configure, start, stop, and test the auto-clicker.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

*(It is recommended to add a file named `LICENSE` with the text of the MIT License.)*
