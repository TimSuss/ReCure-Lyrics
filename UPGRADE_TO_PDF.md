# 🔄 Upgrading to PDF-Based Teleprompter

This document explains the migration from HTML/Netsurf to PDF/Zathura.

## 📋 What Changed

### Before (HTML-based)
- Generated HTML files
- Viewed in Netsurf browser
- JavaScript-based pagination
- Arrow key scrolling (3× multiplier)
- White background, black text

### After (PDF-based)
- Generated PDF files from HTML
- Viewed in Zathura PDF viewer
- Native PDF pagination with two-page spread
- Page Up/Page Down navigation
- **Dark mode** (dark background, light text)
- **Automatic text flow** across pages
- **Side-by-side book view**

---

## 🎨 Visual Changes

### Dark Mode Styling
- Background: `#1a1a1a` (dark gray)
- Text: `#e0e0e0` (light gray)
- Titles: `#f0f0f0` (bright white)
- Notes: `#999` (muted gray)

### Two-Page Spread
Pages are displayed side-by-side like an open book:
```
┌─────────────┬─────────────┐
│   Page 1    │   Page 2    │
│             │             │
│  [Song 1]   │  [Song 2]   │
│             │             │
└─────────────┴─────────────┘
```

When you press the pedal to "turn the page":
```
┌─────────────┬─────────────┐
│   Page 2    │   Page 3    │
│             │             │
│  [Song 2]   │  [Song 3]   │
│             │             │
└─────────────┴─────────────┘
```

---

## 🛠️ Installation Steps (Raspberry Pi)

### 1. Install New Dependencies

```bash
# Install Zathura and WeasyPrint dependencies
sudo apt update
sudo apt install -y zathura git \
  python3-pip python3-cffi python3-brotli \
  libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0

# Install WeasyPrint (needed for PDF generation on the Pi)
pip3 install weasyprint --break-system-packages
```

**Note on --break-system-packages:** This flag is required on modern Raspberry Pi OS. It's safe because:
- WeasyPrint only runs during the build process
- Doesn't conflict with system packages
- Alternative: Build PDFs on Windows and just copy them to the Pi

### 2. Update Service Files

```bash
# Copy updated service files
cd ~/projects/ReCure-Lyrics
cp systemd/*.service ~/.config/systemd/user/

# Reload and restart services
systemctl --user daemon-reload
systemctl --user restart teleprompter.service pedals.service
```

### 3. Verify Installation

Check that Zathura is installed:
```bash
which zathura
# Should output: /usr/bin/zathura
```

Check that WeasyPrint is installed:
```bash
python3 -c "from weasyprint import HTML; print('WeasyPrint OK')"
# Should output: WeasyPrint OK
```

---

## 🎹 Zathura Keyboard Shortcuts (for manual testing)

- `d` - Toggle dual-page mode (two-page spread)
- `Page Down` - Next page spread
- `Page Up` - Previous page spread
- `q` - Quit
- `f` - Toggle fullscreen
- `r` - Rotate
- `+`/`-` - Zoom in/out

---

## 📝 Building Your First PDF

On your **Windows development machine**:

```bash
# Navigate to the repo
cd C:\Git\recure-lyrics

# Run the build script
python build_setlist.py
```

This will:
1. Read `input/setlist.txt`
2. Resolve song titles with fuzzy matching
3. Generate HTML with dark mode styling
4. **Generate PDF** from the HTML
5. Save both to `output/setlist_YYYY-MM-DD.html` and `.pdf`

---

## 🔧 Troubleshooting

### WeasyPrint Installation Issues

**Option 1: Install with --break-system-packages (recommended)**

```bash
sudo apt install -y python3-pip python3-cffi python3-brotli \
  libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0
pip3 install weasyprint --break-system-packages
```

**Option 2: Build PDFs on Windows only (easier)**

If WeasyPrint installation on the Pi is problematic:
1. Build PDFs on your Windows machine: `python build_setlist.py`
2. Commit and push the generated PDF to git
3. Pull on the Pi - no WeasyPrint needed!
4. The teleprompter service will use the pre-built PDF

### Zathura Not Finding PDF Files

Check the service logs:
```bash
journalctl --user -u teleprompter.service -f
```

Ensure PDF files exist in the output directory:
```bash
ls -lh ~/projects/ReCure-Lyrics/output/*.pdf
```

### Pedals Not Working

Check pedals service:
```bash
journalctl --user -u pedals.service -f
```

Test manually with keyboard:
- `Page Down` should turn to next spread
- `Page Up` should turn to previous spread

---

## 🚀 Performance Considerations (Pi Zero 2 W)

### Why Zathura?
Zathura is **much lighter** than Netsurf for this use case:
- Native PDF rendering (no JavaScript overhead)
- Minimal memory footprint
- Fast page-turning
- Built-in two-page mode

### PDF Size
The PDFs are larger than HTML files (~500KB vs 50KB) but:
- No JavaScript parsing at runtime
- No DOM manipulation
- Faster initial load
- More predictable performance

### Expected Performance
- **PDF generation**: ~2-5 seconds on Windows, ~10-15 seconds on Pi
- **PDF viewer launch**: ~1-2 seconds
- **Page turning**: Instant (native PDF navigation)

---

## 📖 Technical Details

### CSS Paged Media
The HTML template uses CSS `@page` rules for proper PDF pagination:

```css
@page {
  size: A4 landscape;
  margin: 15mm;
  background: #1a1a1a;
}
```

### Page Break Control
Songs avoid being split across pages:
```css
.song {
  page-break-inside: avoid;
  break-inside: avoid;
}
```

### WeasyPrint Conversion
Python code:
```python
from weasyprint import HTML
HTML(string=html).write_pdf('output.pdf')
```

---

## 🎯 Benefits of PDF Approach

✅ **Consistent pagination** - Pages are always the same size
✅ **Dark mode** - Easy on the eyes during performances
✅ **Natural page-turning** - Book-like experience
✅ **Automatic text flow** - Long songs naturally span multiple pages
✅ **Lightweight viewer** - Better performance on Pi Zero 2 W
✅ **No JavaScript** - Simpler, more reliable
✅ **Print-ready** - Can actually print the setlist if needed

---

## 📚 Next Steps

1. **Test on Windows**: Run `python build_setlist.py` to generate a PDF
2. **Push to Git**: Commit and push your changes
3. **Pull on Pi**: The post-merge hook will auto-update services
4. **Reboot Pi**: Everything should launch automatically
5. **Test pedals**: Verify page-turning works correctly

---

## 🆘 Need Help?

Check the main [README.md](README.md) for full documentation.

For issues, check:
- System logs: `journalctl --user -u teleprompter.service -f`
- Pedal logs: `journalctl --user -u pedals.service -f`
- Service status: `systemctl --user status teleprompter.service pedals.service`
