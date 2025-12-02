## **Background** ## 
I am in a tribute banch to The Cure. This takes raw text files containing our setlists and builds an html file with a stage ready setlist that includes all of my cues and reminders and sometimes full lyrics. The html will be converted to a pdf and leveraged for another project--a custom teleprompter for the stage.

Here you go — a clean, **Markdown onboarding guide** that you can drop directly into your repo (e.g., `SETUP.md`).
This explains how a fresh user can set up the Pi, install the services, and run the teleprompter + pedals system.

---

# **ReCure Teleprompter – Raspberry Pi Setup Guide**

This document explains how to set up a Raspberry Pi (Zero 2 W or newer) to run the **HTML teleprompter** and **footswitch pedal controller**.

The Pi will:

* Boot into the Raspberry Pi OS desktop
* Automatically load the **newest** HTML file from
  `~/projects/ReCure-Lyrics/output/`
* Launch the browser in fullscreen
* Listen to two footswitch pedals for scrolling, diagnostics, etc.

---

# **1. Requirements**

## Hardware

* Raspberry Pi Zero 2 W (recommended) or any Pi 3–5
* MicroSD card (16+ GB)
* Two momentary footswitch buttons
* Two LEDs (optional, for diagnostics)
* Wires or TRS jack
* Monitor + keyboard/mouse (for first setup)

## Software

* Raspberry Pi OS Desktop (Wayland version, default as of 2023+)
* Git
* Python 3
* `wtype` (Wayland-safe keystroke injector)

---

# **2. Flash Raspberry Pi OS**

Use the **Raspberry Pi Imager** on Windows/macOS/Linux:

1. Choose **Raspberry Pi OS (32-bit) – Desktop**
2. Enable:

   * SSH
   * Wi-Fi
   * User: `tim-r` (or your preferred user)
3. Flash the SD card
4. Boot the Pi

---

# **3. Clone the Repository**

After booting and connecting to the network:

```bash
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/YOUR-REPO/ReCure-Lyrics.git
```

*(Change the repo URL to match your actual repo.)*

---

# **4. Fix Windows Line Endings (important)**

If the repo was edited on a Windows machine, run:

```bash
cd ~/projects/ReCure-Lyrics
sed -i 's/\r$//' pedals.py
sed -i 's/\r$//' systemd/*.service
```

---

# **5. Install Required Packages**

```bash
sudo apt update
sudo apt install wtype python3-gpiozero git
```

Your browser (Netsurf) may already be installed. If not:

```bash
sudo apt install netsurf-gtk
```

---

# **6. Make the Pedal Script Executable**

```bash
chmod +x ~/projects/ReCure-Lyrics/pedals.py
```

---

# **7. Install User-Level Systemd Services**

User services live in:

```
~/.config/systemd/user/
```

Create the directory if needed:

```bash
mkdir -p ~/.config/systemd/user
```

Copy service files:

```bash
cp ~/projects/ReCure-Lyrics/systemd/teleprompter.service ~/.config/systemd/user/
cp ~/projects/ReCure-Lyrics/systemd/pedals.service ~/.config/systemd/user/
```

Reload:

```bash
systemctl --user daemon-reload
```

Enable both on login:

```bash
systemctl --user enable teleprompter.service
systemctl --user enable pedals.service
```

Start:

```bash
systemctl --user start teleprompter.service
systemctl --user start pedals.service
```

---

# **8. Enable Lingering (required for auto-start)**

```bash
sudo loginctl enable-linger tim-r
```

Replace `tim-r` with your username if different.

---

# **9. Footswitch Wiring (GPIO)**

| Function | GPIO Pin | Type            |
| -------- | -------- | --------------- |
| Button A | 17       | Input (pull-up) |
| Button B | 27       | Input (pull-up) |
| LED A    | 22       | Output          |
| LED B    | 23       | Output          |
| Ground   | Any GND  | Ground          |

You may use a TRS jack:

* **Tip** → Button A → GPIO17
* **Ring** → Button B → GPIO27
* **Sleeve** → Ground

No resistors needed (internal pull-ups used).

---

# **10. How the Pedals Work**

### **Button A**

* Tap → Page Down
* Hold 5 seconds → Enter/Exit Diagnostic Mode

### **Button B**

* Tap → Slow scroll (Down Arrow)

### **Both buttons pressed briefly**

* Send TAB key (brings browser back into focus)

### **Diagnostic Mode**

* LEDs mirror button presses
* Exits when A is held 5 seconds again

---

# **11. Autoloading the Latest HTML File**

The teleprompter service runs this logic:

```bash
LATEST=$(ls -t ~/projects/ReCure-Lyrics/output/*.html | head -n 1)
```

On boot, the newest HTML file is automatically opened in the browser.

You can generate new files from your workflow and simply place them in:

```
~/projects/ReCure-Lyrics/output/
```

---

# **12. Managing the Services**

### Check logs:

```bash
journalctl --user -u teleprompter.service -n 50 --no-pager
journalctl --user -u pedals.service -n 50 --no-pager
```

### Restart a service:

```bash
systemctl --user restart teleprompter.service
systemctl --user restart pedals.service
```

### Stop a service:

```bash
systemctl --user stop teleprompter.service
```

---

# **13. Common Troubleshooting**

### ❌ Script doesn’t run at boot

Run:

```bash
sudo loginctl enable-linger tim-r
```

### ❌ Python script crashes

```bash
journalctl --user -u pedals.service
```

### ❌ Wrong browser window size

Open Netsurf manually → maximize it → close it.
Labwc remembers window geometry.

### ❌ Keys stop working after clicking

Press both buttons briefly → sends TAB → focus restored.

---

# **14. Updating the Pi After Git Pull**

Whenever you pull new code:

```bash
cd ~/projects/ReCure-Lyrics
git pull
sed -i 's/\r$//' pedals.py
chmod +x pedals.py
systemctl --user restart pedals.service
systemctl --user restart teleprompter.service
```

---

# **You’re Done!**

Your Pi will now:

✔ Boot straight into the teleprompter
✔ Load the latest lyrics HTML
✔ Run pedal control automatically
✔ Support diagnostic LED feedback
✔ Stay Wayland-safe using wtype

If you want, I can generate:

* A PDF version of this guide
* A bash "first-run setup" script to automate everything
* The wiring diagram
* Or a clean architecture diagram of the whole system.


