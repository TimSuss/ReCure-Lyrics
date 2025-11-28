# build_setlist.py
import os
from datetime import date
from songs import SONGS

SETLIST_FILE = "setlist.txt"

# >>> SET THIS <<<
# False = shorthand teleprompter lyrics
# True  = full DOCX lyrics
USE_FULL_LYRICS = True

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
    margin-bottom: 1.5em;
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
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Setlist file not found: {filename}")
    titles = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            t = line.strip()
            if t:
                titles.append(t)
    return titles

def build_song_section(song):
    # Per-song override wins
    if song.use_full and song.lyrics_full_html.strip():
        lyrics = song.lyrics_full_html
    else:
        lyrics = song.lyrics_html

    return f"""
<div class="song">
  <h1 class="title">{song.title}</h1>
  <div class="notes">{song.notes_html}</div>
  <div class="lyrics">{lyrics}</div>
</div>
""".strip()


def build_html(setlist_titles):
    sections = []
    for title in setlist_titles:
        if title not in SONGS:
            raise ValueError(f"Song not found: {title}")
        sections.append(build_song_section(SONGS[title]))
    return HTML_TEMPLATE.format(body="\n\n".join(sections))

def make_output_filename(prefix="setlist"):
    today = date.today().strftime("%Y-%m-%d")
    base = f"{prefix}_{today}"
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
    print(f"Created {output_file}")
