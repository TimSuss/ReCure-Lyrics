# build_setlist.py
from songs import SONGS

# 1) Define your setlist order here or load from a text file
SETLIST = [
    "Where",
    "A Night Like This",
    # etc...
]

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

def build_song_section(song: "Song") -> str:
    return f"""
<section class="song">
  <h1 class="title">{song.title}</h1>
  <div class="notes">
    {song.notes_html}
  </div>
  <div class="lyrics">
    {song.lyrics_html}
  </div>
</section>
""".strip()

def build_html(setlist_titles):
    sections = []
    for title in setlist_titles:
        if title not in SONGS:
            raise ValueError(f"Song not found in library: {title}")
        sections.append(build_song_section(SONGS[title]))
    body = "\n\n".join(sections)
    return HTML_TEMPLATE.format(body=body)

if __name__ == "__main__":
    html = build_html(SETLIST)
    output_file = "setlist.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {output_file}. Open it in a browser and print to PDF.")
