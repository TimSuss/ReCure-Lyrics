

# 🎸 **ReCure Teleprompter – Raspberry Pi + Footswitch System**

A custom teleprompter + pedal controller designed for a live tribute band performing the music of **The Cure**.
This system converts raw text setlists into styled PDFs, displays them on a Raspberry Pi teleprompter with a two-page book view, and allows hands-free page-turning via a dual footswitch pedal.

---

# 📌 **Background**

This project takes raw text files containing our **setlists** and builds a stage-ready **PDF teleprompter file** that includes cues, reminders, and sometimes full lyrics.
The PDF is displayed on a **custom Raspberry Pi Zero 2 W teleprompter** in a two-page side-by-side view (like an open book) with dark mode styling and hands-free footswitch control for page-turning.

---

# 🖥️ **System Overview**

The Raspberry Pi:

* Boots directly into the desktop
* Automatically opens the most recent generated PDF setlist
* Displays it fullscreen in Zathura PDF viewer with two-page spread mode (dark background)
* Accepts input from a dual footswitch
* Allows page-turning (each press turns to the next two-page spread), TAB focus recovery, and diagnostic mode

User-level `systemd` services ensure everything starts automatically on boot.

---

# 🛠️ **Hardware Requirements**

### **Raspberry Pi**

* Raspberry Pi Zero 2 W (recommended)
* Pi 3/4/5 also supported

### **Electrical**

* Dual momentary footswitch (TRS)
* 1 × TRS panel-mount jack (stereo)
* 3 wires (Tip, Ring, Sleeve)
* Optional: 2 LEDs (for diagnostic mode)

### **Display**

* Any HDMI monitor or teleprompter screen

---

# 🎚️ **Footswitch TRS Wiring (Corrected)**

Your pedal must provide **two completely isolated switches**.

Correct wiring:

```
TIP   → Switch A → GPIO17
RING  → Switch B → GPIO27
SLEEVE → Ground
```

⚠️ **Tip ↔ Ring MUST NOT show continuity when idle.**
If they short, both buttons fire — this was the root cause of earlier issues.

---

# 🔧 **Software Setup (Pi)**

### 1. Install Raspberry Pi OS

Use the official Raspberry Pi Imager and select **Raspberry Pi OS (32-bit) Desktop**.

Enable:

* SSH
* Wi-Fi
* Username (e.g., `tim-r`)

---

### 2. Clone the Repo

```bash
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/YOUR-REPO/ReCure-Lyrics.git
```

---

### 3. Install Required Packages

```bash
sudo apt update
sudo apt install -y wtype python3-gpiozero zathura git python3-pip
pip3 install weasyprint
```

**Package Details:**
- `wtype`: Sends keypresses to applications (for pedal control)
- `python3-gpiozero`: GPIO control library for footswitch
- `zathura`: Lightweight PDF viewer (replaces Netsurf)
- `weasyprint`: Python library for converting HTML to PDF
- `git`: Version control

---

### 4. Copy & Enable Systemd Services

```bash
mkdir -p ~/.config/systemd/user
cp ~/projects/ReCure-Lyrics/systemd/*.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now teleprompter.service pedals.service
```

Enable lingering so services survive logout:

```bash
sudo loginctl enable-linger $USER
```

---

# 🎛️ **Pedal Behavior**

### **Tap A → Page Up**

Turns to the previous two-page spread (like flipping a book backward).

### **Tap B → Page Down**

Turns to the next two-page spread (the right page becomes the left page, new content appears on the right).

### **Hold A → then Tap B → TAB**

Zathura occasionally loses focus; this restores it.

### **Hold A for 5 seconds → Diagnostic Mode**

* LEDs blink
* Pedal scrolling disabled
* Press A for 5 seconds again to exit
* On exit, both services restart:

```
teleprompter.service
pedals.service
```

---

# 📖 **PDF Page-Turning Logic**

The system uses Zathura's two-page spread mode (activated with the `d` key on startup).

**How it works:**
1. PDF is generated with automatic pagination (songs flow across multiple pages as needed)
2. Zathura displays pages in two-page spread mode (like an open book)
3. Each pedal press sends a single `Page_Down` or `Page_Up` keypress
4. The display shifts by one two-page spread (right page becomes left page)

**Visual Example:**
```
Initial view:     After Page Down:
┌─────┬─────┐    ┌─────┬─────┐
│ P1  │ P2  │ →  │ P2  │ P3  │
└─────┴─────┘    └─────┴─────┘
```

This creates a natural "book-turning" experience optimized for live performance.

---

# 🔁 **Automatic Updating (Post-Merge Hook)**

To ensure the Pi always runs the latest code, add this hook:

```
~/projects/ReCure-Lyrics/.git/hooks/post-merge
```

```bash
#!/bin/bash

PROJECT_DIR="$HOME/projects/ReCure-Lyrics"
SERVICE_DIR="$HOME/.config/systemd/user"

echo "Running ReCure Teleprompter auto-update..."

# Fix Windows CRLF line endings
find "$PROJECT_DIR" -type f -name "*.py" -exec sed -i 's/\r$//' {} \;
find "$PROJECT_DIR/systemd" -type f -name "*.service" -exec sed -i 's/\r$//' {} \;

# Ensure executables
chmod +x "$PROJECT_DIR/pedals.py" 2>/dev/null || true
chmod +x "$PROJECT_DIR"/*.sh 2>/dev/null || true

# Update systemd files
mkdir -p "$SERVICE_DIR"
cp "$PROJECT_DIR/systemd/"*.service "$SERVICE_DIR"

# Reload and restart services
systemctl --user daemon-reload
systemctl --user restart teleprompter.service pedals.service

echo "ReCure Teleprompter auto-update complete!"
```

Make executable:

```bash
chmod +x ~/projects/ReCure-Lyrics/.git/hooks/post-merge
```

### Result:

Whenever you run:

```bash
git pull
```

everything updates automatically.

---

# 🪟 **Windows Development Workflow**

Windows → edit files normally → push → Pi pulls → everything updates.

Highly recommended: create a `.gitattributes` to prevent CRLF issues:

```
*.py text eol=lf
*.service text eol=lf
*.sh text eol=lf
```

Git will convert to the correct LF endings automatically.

---

# 🧰 **Troubleshooting**

### **Pedal does nothing**

Run:

```bash
wtype -k Down
```

If Netsurf doesn't scroll, it doesn't have focus.

### **TAB combo doesn't switch**

Use A-hold + B-tap — not simultaneous.

### **Scrolling too slow or too fast**

Change:

```bash
SCROLL_MULTIPLIER = 10
```

### **Pedal fires multiple times**

Check TRS jack wiring — Tip and Ring must be isolated.

---

# 🎉 **You're Ready for the Stage**

Your Pi will now:

* Load the newest lyrics HTML automatically
* Scroll via footswitch with smooth, stable control
* Recover browser focus via TAB combo
* Enter diagnostic mode for on-stage debugging
* Update itself automatically after every `git pull`
