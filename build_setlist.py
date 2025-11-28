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

  @media print {{
    @page {{
      margin: 10mm !important;
    }}
    body {{
      margin: 0 !important;
      padding: 0 !important;
    }}
    .song {{
      page-break-inside: avoid;
      break-inside: avoid;
    }}
    p {{
      margin: 0 0 0.25em 0 !important;
    }}
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
    For any title that doesn't exist in SONGS,
    prompt the user to select the correct one from an
    alphabetized, numbered list. Then update the setlist file.
    """
    all_song_names = sorted(SONGS.keys())
    resolved = []
    changed = False

    for original in titles:
        if original in SONGS:
            resolved.append(original)
            continue

        # Prompt user for this unknown song
        print(f"\nSong not found in library: '{original}'")
        print("Please choose from the list below:")

        for idx, name in enumerate(all_song_names, start=1):
            print(f"  {idx}. {name}")

        while True:
            choice = input(
                "Type the number that corresponds to this song "
                "(or press Enter to skip this song): "
            ).strip()

            if choice == "":
                print(f"Skipping '{original}'. It will be omitted from this setlist.")
                break

            if not choice.isdigit():
                print("Please type a valid number.")
                continue

            n = int(choice)
            if 1 <= n <= len(all_song_names):
                selected = all_song_names[n - 1]
                print(f"Using '{selected}' for '{original}'.")
                resolved.append(selected)
                changed = True
                break
            else:
                print(f"Please enter a number between 1 and {len(all_song_names)}.")

    # If we made any substitutions, update setlist.txt
    if changed:
        print("\nUpdating setlist.txt with your choices...")
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
            # This should not happen if resolve_titles_with_user did its job,
            # but we keep this as a safety.
            raise ValueError(f"Song not found in library after resolution: '{title}'")
        sections.append(build_song_section(SONGS[title]))
    return HTML_TEMPLATE.format(body="\n\n".join(sections))


def make_output_filename(prefix: str = "setlist") -> str:
    """Create a dated output filename, avoiding overwrites."""
    today_str = date.today().strftime("%Y-%m-%d")
    base = f"{prefix}_{today_str}"
    filename = f"{base}.html"

    counter = 2
    while os.path.exists(filename):
        filename = f"{base}_{counter}.html"
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
    output_file = make_output_filename()
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Wrote {output_file}. Open it in a browser and print to PDF.")
