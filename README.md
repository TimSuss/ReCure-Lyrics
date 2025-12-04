# **ReCure Teleprompter – Raspberry Pi Setup Guide**

## **Background**

I am in a tribute band to **The Cure**. This project takes raw text files containing our setlists and builds an HTML file with a **stage-ready teleprompter setlist** that includes cues, reminders, and sometimes full lyrics.
The HTML file is eventually converted into a PDF and used by a separate project — a **custom Raspberry Pi teleprompter system** with foot-switch controls.

This guide explains how to set up that Pi system and run everything automatically.

---

# **1. Requirements**

## Hardware

* Raspberry Pi Zero 2 W (recommended) or Pi 3–5
* MicroSD card (16+ GB)
* Two momentary switches (footswitch pedals)
* Two LEDs (optional diagnostics)
* TRS jack/wiring (if needed)
* Temporary monitor/keyboard/mouse for setup

## Software

* Raspberry Pi OS Desktop (Wayland)
* Python 3
* `gpiozero`
* `wtype` (Wayland keystroke injector)
* Netsurf browser (lightweight + fast on Pi Zero)

---

# **2. Flash Raspberry Pi OS**

Use **Raspberry Pi Imager**:

1. Choose **Raspberry Pi OS (32-bit) Desktop**
2. Configure:

   * Hostname, Wi-Fi, and SSH
   * User account (ex: `tim-r`)
3. Flash → insert into Pi → boot.

---

# **3. Clone This Repository**

```bash
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/YOUR-REPO/ReCure-Lyrics.git
```

Change repo URL as needed.

---

# **4. Install Required Packages**

```bash
sudo apt update
sudo apt install -y wtype python3-gpiozero netsurf-gtk git
```

---

# **5. Make Scripts Executable**

```bash
chmod +x ~/projects/ReCure-Lyrics/pedals.py
```

---

# **6. Install Systemd Services (User Mode)**

Copy the service files:

```bash
mkdir -p ~/.config/systemd/user
cp ~/projects/ReCure-Lyrics/systemd/*.service ~/.config/systemd/user/
```

Reload:

```bash
systemctl --user daemon-reload
```

Enable autostart:

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

# **7. Enable Lingering (Required for Auto-Start on Boot)**

```bash
sudo loginctl enable-linger tim-r
```

Replace the username if different.

---

# **8. Footswitch Wiring (GPIO)**

| Function | GPIO Pin | Type            |
| -------- | -------- | --------------- |
| Button A | 17       | Input (pull-up) |
| Button B | 27       | Input (pull-up) |
| LED A    | 22       | Output          |
| LED B    | 23       | Output          |
| Ground   | Any GND  | —               |

### TRS Jack Mapping (Typical)

* **Tip → Button A → GPIO17**
* **Ring → Button B → GPIO27**
* **Sleeve → Ground**

Internal pull-ups remove the need for resistors.

---

# **9. Pedal Behavior (Updated / Cleaned)**

✔ **Button A (Tap)** → PAGE UP
✔ **Button B (Tap)** → PAGE DOWN
✔ **Both Buttons (Short press together)** → TAB (refocus browser)
✔ **Hold A for 5 seconds** → Toggle diagnostic mode

### Diagnostic Mode

* LEDs mirror button presses
* Toggles ON/OFF by holding **A for 5 seconds**
* No scroll actions performed

**Slow scroll and jump-to-top have been removed.**

---

# **10. Teleprompter Auto-Load Behavior**

The teleprompter systemd service runs:

```bash
LATEST=$(ls -t ~/projects/ReCure-Lyrics/output/*.html | head -n 1)
```

This means:

* Whatever **newest HTML file** appears inside
  `~/projects/ReCure-Lyrics/output/`
  will automatically open fullscreen in Netsurf on boot.

Just regenerate your setlist → copy into `output/` → reboot (or restart service).

---

# **11. Managing the Services**

### Check logs

```bash
journalctl --user -u teleprompter.service -n 50 --no-pager
journalctl --user -u pedals.service -n 50 --no-pager
```

### Restart

```bash
systemctl --user restart teleprompter.service
systemctl --user restart pedals.service
```

### Stop

```bash
systemctl --user stop teleprompter.service
```

---

# **12. Troubleshooting**

### ❌ Pedals don’t work

Probably a Python crash:

```bash
journalctl --user -u pedals.service
```

### ❌ Teleprompter doesn’t load at boot

Run lingering again:

```bash
sudo loginctl enable-linger tim-r
```

### ❌ Browser isn’t fullscreen

Open Netsurf manually → maximize → close.
Labwc remembers the size.

### ❌ Clicking breaks keyboard control

Press both pedals → sends TAB → browser regains focus.

---

# **13. Updating After Git Pull**

```bash
cd ~/projects/ReCure-Lyrics
git pull
chmod +x pedals.py
systemctl --user restart pedals.service
systemctl --user restart teleprompter.service
```

---
