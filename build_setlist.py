# build_setlist.py
import os
from datetime import date
from songs import SONGS

SETLIST_FILE = "setlist.txt"

HTML_TEMPLATE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 18pt;
    line-height: 1.4;
    color: #000;
    background: #ffffff;
    margin: 0;
    padding: 16px;
  }}

  .song {{
    margin-bottom: 1.5em;  /* visual separation only, no page break */
  }}

  h1.title {{
    font-size: 26pt;
    margin: 0 0 0.2em 0;
    font-weight: 700;
  }}

  .notes {{
    font-size: 12pt;
    color: #555;
    margin-bottom: 0.4em;
  }}

  .lyrics {{
    font-size: 18pt;
  }}

  .highlight {{
    font-weight: 700;
    color: #c00000;
  }}

  .cue {{
    font-style: italic;
    color: #0066cc;
  }}

  .note {{
    font-size: 80%;
    color: #777;
  }}

  .section-label {{
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 70%;
    color: #444;
  }}

  .marker-yellow {{
    background: #fff2a8;
  }}

  .marker-green {{
    background: #c6f6c6;
  }}

  p {{
    margin: 0 0 0.2em 0;
  }}
</style>
</head>
<body>
{body}
</body>
</html>
"""

def read_setlist(filename: str):
    """Reads a plain text setlist file, one title per line."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Setlist file not found: {filename}")

    titles = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            title = line.strip()
            if title:
                titles.append(title)

    return titles


def build_song_section(song):
    return f"""
<div class="song">
  <h1 class="title">{song.title}</h1>
  <div class="notes">{song.notes_html}</div>
  <div class="lyrics">{song.lyrics_html}</div>
</div>
""".strip()


def build_html(setlist_titles):
    sections = []
    for title in setlist_titles:
        if title not in SONGS:
            available = ", ".join(SONGS.keys())
            raise ValueError(
                f"Song not found in library: '{title}'.\n"
                f"Check spelling.\n\nAvailable titles:\n{available}"
            )
        sections.append(build_song_section(SONGS[title]))

    body = "\n\n".join(sections)
    return HTML_TEMPLATE.format(body=body)


def make_output_filename(prefix: str = "setlist") -> str:
    """Create a dated output filename, avoiding overwrites.

    Examples:
      setlist_2025-11-28.html
      setlist_2025-11-28_2.html
      setlist_2025-11-28_3.html
    """
    today_str = date.today().strftime("%Y-%m-%d")
    base = f"{prefix}_{today_str}"
    filename = f"{base}.html"

    counter = 2
    while os.path.exists(filename):
        filename = f"{base}_{counter}.html"
        counter += 1

    return filename


if __name__ == "__main__":
    # 1) Load titles from setlist.txt
    titles = read_setlist(SETLIST_FILE)

    # 2) Build HTML
    html = build_html(titles)

    # 3) Choose a non-clobbering output filename with today's date
    output_file = make_output_filename()

    # 4) Write output
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Wrote {output_file}. Open it in a browser and print to PDF.")
    print("Tip: disable headers/footers in the browser print dialog for a clean teleprompter view.")
