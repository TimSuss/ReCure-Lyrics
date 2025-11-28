# build_setlist.py
import os
from songs import SONGS

SETLIST_FILE = "setlist.txt"

HTML_TEMPLATE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Teleprompter Setlist</title>
<style>
  @page {{
    size: A4;
    margin: 15mm;
  }}

  body {{
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 18pt;
    line-height: 1.4;
    color: #000;
    background: #ffffff;
  }}

  .song {{
    page-break-after: always;
  }}

  h1.title {{
    font-size: 26pt;
    margin: 0 0 0.2em 0;
    font-weight: 700;
  }}

  .notes {{
    font-size: 12pt;
    color: #555;
    margin-bottom: 0.8em;
  }}

  .lyrics {{
    font-size: 18pt;
  }}

  /* Utility styles for intra-line emphasis */
  .highlight {{
    font-weight: 700;
    color: #c00000; /* strong red */
  }}

  .cue {{
    font-style: italic;
    color: #0066cc; /* blue cue text */
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

  /* Optional: fake "marker" vibe for quick visual anchors */
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
<section class="song">
  <h1 class="title">{song.title}</h1>
  <div class="notes">{song.notes_html}</div>
  <div class="lyrics">{song.lyrics_html}</div>
</section>
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


if __name__ == "__main__":
    # Load titles from setlist.txt
    titles = read_setlist(SETLIST_FILE)

    # Build HTML
    html = build_html(titles)

    # Write output
    output_file = "setlist.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Wrote {output_file}. Open it in a browser and print to PDF.")
