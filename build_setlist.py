# build_setlist.py
import os
import re
from datetime import date
import difflib
from songs import SONGS

import sys
import platform

try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

SETLIST_FILE = os.path.join("input", "setlist.txt")

# Case-insensitive map: lowercase name → canonical name
SONGS_LOWER = {name.lower(): name for name in SONGS.keys()}



HTML_TEMPLATE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  /* CSS Paged Media - for PDF generation */
  @page {{
    size: A4 portrait;
    margin: 20mm 10mm;
    background: #1a1a1a;
  }}

  body {{
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 20pt;
    line-height: 1.5;
    color: #e0e0e0;
    background: #1a1a1a;
    margin: 0;
    padding: 0;
  }}

  .song {{
    margin-bottom: 2em;
    page-break-inside: avoid;
    break-inside: avoid;
    orphans: 3;
    widows: 3;
  }}

  h1.title {{
    font-size: 22pt;
    margin: 0 0 0.3em 0;
    font-weight: 700;
    color: #f0f0f0;
    page-break-after: avoid;
    break-after: avoid;
  }}

  .notes {{
    font-size: 11pt;
    color: #999;
    margin-bottom: 0.5em;
    page-break-after: avoid;
    break-after: avoid;
  }}

  .lyrics {{
    font-size: 20pt;
  }}

  .lyrics,
  .lyrics * {{
    color: #e0e0e0 !important;
    background: transparent !important;
  }}

  .lyrics p {{
    margin: 0 0 0.3em 0;
  }}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def read_setlist(filename: str):
    """Reads titles from setlist.txt, one per line."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Setlist file not found: {filename}")
    titles = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            t = line.strip()
            if t:
                titles.append(t)
    return titles


def resolve_titles_with_user(titles):
    """
    Resolve titles from setlist.txt against SONGS.

    - Case-insensitive match first.
    - If no match, show fuzzy suggestions (using difflib),
      plus a full alphabetized list of songs with numbers.
    - User must type a number; nothing is auto-accepted.
    - If any changes were made, setlist.txt is rewritten
      with canonical song titles.
    """
    all_song_names = sorted(SONGS.keys())
    index_by_name = {name: idx + 1 for idx, name in enumerate(all_song_names)}
    resolved = []
    changed = False

    for original in titles:
        stripped = original.strip()
        lower = stripped.lower()

        # 1) Case-insensitive direct match
        if lower in SONGS_LOWER:
            canonical = SONGS_LOWER[lower]
            resolved.append(canonical)
            continue

        # 2) No direct match: fuzzy suggestions

        print("\nAll songs:")
        for idx, name in enumerate(all_song_names, start=1):
            print(f"  {idx}. {name}")
        print(f"\nSong not found in library: '{original}'")

        close_lower = difflib.get_close_matches(
            lower,
            list(SONGS_LOWER.keys()),
            n=5,
            cutoff=0.6,
        )
        suggestion_names = [SONGS_LOWER[l] for l in close_lower]

        if suggestion_names:
            print("Close matches (suggested numbers):")
            for name in suggestion_names:
                num = index_by_name[name]
                print(f"  {num}. {name}")
        else:
            print("No close matches found.")

        # 3) Let user choose a number or skip
        while True:
            choice = input(
                "Type the NUMBER that corresponds to this song "
            ).strip()

            if not choice.isdigit():
                print("Please type a valid number.")
                continue

            n = int(choice)
            if 1 <= n <= len(all_song_names):
                canonical = all_song_names[n - 1]
                print(f"Using '{canonical}' for '{original}'.")
                resolved.append(canonical)
                changed = True
                break
            else:
                print(f"Please enter a number between 1 and {len(all_song_names)}.")

    # 4) If we changed anything, rewrite the setlist file with canonical names
    if changed:
        print("\nUpdating setlist file with your choices...")
        with open(SETLIST_FILE, "w", encoding="utf-8") as f:
            for t in resolved:
                f.write(t + "\n")
        print("setlist.txt updated.\n")

    return resolved


def build_song_section(song):
    """
    Choose which lyrics to render:
    - If song.use_full and full lyrics exist: use full
    - Else if shorthand exists: use shorthand
    - Else if full exists: fallback to full
    - Else: empty
    """
    if song.use_full and song.lyrics_full_html.strip():
        lyrics = song.lyrics_full_html
    elif song.lyrics_html.strip():
        lyrics = song.lyrics_html
    elif song.lyrics_full_html.strip():
        lyrics = song.lyrics_full_html
    else:
        lyrics = ""

    lyrics = sanitize_lyrics_html(lyrics)

    return f"""
<div class="song">
  <h1 class="title">{song.title}</h1>
  <div class="notes">{song.notes_html}</div>
  <div class="lyrics">{lyrics}</div>
</div>
""".strip()


def sanitize_lyrics_html(raw_html: str) -> str:
    if not raw_html:
        return raw_html

    # Recover intended literal backslashes from escape sequences.
    raw_html = raw_html.replace("\t", "\\t")
    raw_html = raw_html.replace("\r", "\\r")
    raw_html = raw_html.replace("\b", "\\b")
    raw_html = raw_html.replace("\f", "\\f")

    # Strip embedded document wrappers/styles from pasted HTML.
    raw_html = re.sub(r"<style\b[^>]*>.*?</style>", "", raw_html, flags=re.IGNORECASE | re.DOTALL)
    raw_html = re.sub(r"<head\b[^>]*>.*?</head>", "", raw_html, flags=re.IGNORECASE | re.DOTALL)
    raw_html = re.sub(r"</?html\b[^>]*>", "", raw_html, flags=re.IGNORECASE)
    raw_html = re.sub(r"</?body\b[^>]*>", "", raw_html, flags=re.IGNORECASE)

    return raw_html.strip()


def build_html(setlist_titles):
    """
    Build the HTML output consisting of:
    1. Songs in the setlist, in order
    2. A separator line
    3. All remaining songs NOT in the setlist, alphabetized,
       each rendered with full song details (title, notes, lyrics).
    """
    sections = []

    # 1) Songs that ARE in the setlist
    for title in setlist_titles:
        if title not in SONGS:
            # Should not happen if resolve_titles_with_user was run
            raise ValueError(f"Song not found in library after resolution: '{title}'")
        sections.append(build_song_section(SONGS[title]))

    # 2) Separator line
    sections.append(
        """
<div class="song">
  <h1 class="title">------NOT INCLUDED------</h1>
</div>
""".strip()
    )

    # 3) Songs NOT in the setlist (alphabetized)
    included_set = set(setlist_titles)
    leftovers = sorted([name for name in SONGS.keys() if name not in included_set])

    for title in leftovers:
        sections.append(build_song_section(SONGS[title]))

    # Final document
    body = "\n\n".join(sections)
    return HTML_TEMPLATE.format(body=body)


def make_output_filename(prefix: str = "setlist") -> str:
    """Create a dated output filename inside ./output/, avoiding overwrites."""
    today_str = date.today().strftime("%Y-%m-%d")
    base_name = f"{prefix}_{today_str}.html"

    # ensure output directory exists
    os.makedirs("output", exist_ok=True)

    # try first version
    filename = os.path.join("output", base_name)

    # if it already exists, append _2, _3, etc.
    counter = 2
    while os.path.exists(filename):
        filename = os.path.join("output", f"{prefix}_{today_str}_{counter}.html")
        counter += 1

    return filename


if __name__ == "__main__":
    # 1) Read setlist.txt
    titles = read_setlist(SETLIST_FILE)

    # 2) Resolve any unknown titles by asking the user to choose
    titles = resolve_titles_with_user(titles)

    # 3) Build HTML from the resolved titles
    html = build_html(titles)

    # 4) Write out the dated HTML file
    html_file = make_output_filename()
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {html_file}")

    # 5) Generate PDF from HTML
    if WEASYPRINT_AVAILABLE:
        pdf_file = html_file.replace('.html', '.pdf')
        print(f"Generating PDF: {pdf_file}")
        try:
            HTML(string=html).write_pdf(pdf_file)
            print(f"✓ PDF generated successfully: {pdf_file}")
        except Exception as e:
            print(f"✗ PDF generation failed: {e}")
            print("\nYou can manually generate the PDF:")
            print(f"1. Open {html_file} in your browser")
            print("2. Press Ctrl+P (Print)")
            print("3. Select 'Save as PDF'")
            print(f"4. Save as: {html_file.replace('.html', '.pdf')}")
    else:
        # On Windows, offer to open HTML in browser for manual PDF export
        if platform.system() == 'Windows':
            print("\n" + "="*60)
            print("WeasyPrint not available on Windows.")
            print("Opening HTML file in your browser for manual PDF export...")
            print("="*60)
            print("\nSteps to create PDF:")
            print("1. Browser will open with the setlist")
            print("2. Press Ctrl+P (or Cmd+P on Mac)")
            print("3. Destination: 'Save as PDF'")
            print("4. Save as: " + html_file.replace('.html', '.pdf'))
            print("="*60 + "\n")

            import webbrowser
            webbrowser.open('file://' + os.path.abspath(html_file))
        else:
            print("\n✗ WeasyPrint not installed.")
            print("Install with: pip3 install weasyprint --break-system-packages")
