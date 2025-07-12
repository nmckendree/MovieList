
import sys
from pathlib import Path
from collections import defaultdict
import string
from datetime import datetime

def read_items_from_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def generate_html_page(title, items, output_file):
    # Build alphabetic index
    item_dict = defaultdict(list)
    for item in sorted(items, key=lambda x: x.lower()):
        first_char = item[0].upper()
        if first_char not in string.ascii_uppercase:
            first_char = "#"
        item_dict[first_char].append(item)

    # HTML header with mobile viewport
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 10px; padding: 0; }}
    .back-btn {{ display: block; margin-bottom: 15px; padding: 10px; 
                 background: #007bff; color: #fff; text-align: center; 
                 text-decoration: none; border-radius: 4px; }}
    .menu {{ margin-bottom: 15px; overflow-x: auto; white-space: nowrap; }}
    .menu a {{ margin: 0 5px; text-decoration: none; padding: 6px 8px;
               background: #f0f0f0; border-radius: 4px; font-size: 0.9em; }}
    .section {{ margin-bottom: 20px; }}
    .section h2 {{ border-bottom: 1px solid #ccc; padding-bottom: 4px; }}
    .item {{ margin-left: 15px; padding: 4px 0; }}
    #searchBar {{ margin-bottom: 15px; padding: 8px; width: 100%; 
                 box-sizing: border-box; font-size: 1em; }}
  </style>
</head>
<body>
  <a href="index.html" class="back-btn">← Back to Main</a>
  <input type="text" id="searchBar" placeholder="Search...">
  <div class="menu">
"""
    # Alphabet navigation
    for letter in string.ascii_uppercase + "#":
        if letter in item_dict:
            html += f'<a href="#{letter}">{letter}</a> '
    html += "</div>\n"

    # Sections
    for letter in sorted(item_dict):
        html += f'<div class="section" id="{letter}">\n  <h2>{letter}</h2>\n'
        for item in item_dict[letter]:
            html += f'  <div class="item">{item}</div>\n'
        html += "</div>\n"

    # Search script
    html += """
<script>
const bar = document.getElementById("searchBar");
bar.addEventListener("input", () => {
  const q = bar.value.toLowerCase();
  document.querySelectorAll(".section").forEach(sec => {
    let showAny = false;
    sec.querySelectorAll(".item").forEach(it => {
      if (it.textContent.toLowerCase().includes(q)) {
        it.style.display = "";
        showAny = true;
      } else {
        it.style.display = "none";
      }
    });
    sec.style.display = showAny ? "" : "none";
  });
});
</script>
</body>
</html>
"""
    Path(output_file).write_text(html, encoding="utf-8")
    print(f"Wrote {output_file}")

def generate_tv_html_page(title, items, output_file):
    # Group seasons under each show
    show_dict = defaultdict(list)
    for line in items:
        if ',' in line:
            show, season = map(str.strip, line.split(',', 1))
            show_dict[show].append(season)

    # Build alphabetic index
    sections = defaultdict(list)
    for show in show_dict:
        letter = show[0].upper()
        if letter not in string.ascii_uppercase:
            letter = "#"
        sections[letter].append(show)

    # HTML header
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 10px; padding: 0; }}
    .back-btn {{ display: block; margin-bottom: 15px; padding: 10px; 
                 background: #28a745; color: #fff; text-align: center; 
                 text-decoration: none; border-radius: 4px; }}
    .menu {{ margin-bottom: 15px; overflow-x: auto; white-space: nowrap; }}
    .menu a {{ margin: 0 5px; text-decoration: none; padding: 6px 8px;
               background: #f0f0f0; border-radius: 4px; font-size: 0.9em; }}
    .section {{ margin-bottom: 20px; }}
    .section h2 {{ border-bottom: 1px solid #ccc; padding-bottom: 4px; }}
    .show-block {{ margin-top: 10px; }}
    .show {{ font-weight: bold; padding: 4px 0; }}
    .season {{ margin-left: 15px; color: #555; padding: 2px 0; }}
    #searchBar {{ margin-bottom: 15px; padding: 8px; width: 100%; 
                 box-sizing: border-box; font-size: 1em; }}
  </style>
</head>
<body>
  <a href="index.html" class="back-btn">← Back to Main</a>
  <input type="text" id="searchBar" placeholder="Search...">
  <div class="menu">
"""
    for letter in string.ascii_uppercase + "#":
        if letter in sections:
            html += f'<a href="#{letter}">{letter}</a> '
    html += "</div>\n"

    for letter in sorted(sections):
        html += f'<div class="section" id="{letter}">\n  <h2>{letter}</h2>\n'
        for show in sorted(sections[letter], key=str.lower):
            html += '  <div class="show-block">\n'
            html += f'    <div class="show">{show}</div>\n'
            for season in sorted(show_dict[show], key=str.lower):
                html += f'    <div class="season">{season}</div>\n'
            html += '  </div>\n'
        html += "</div>\n"

    html += """
<script>
const barTv = document.getElementById("searchBar");
barTv.addEventListener("input", () => {
  const q = barTv.value.toLowerCase();
  document.querySelectorAll(".section").forEach(sec => {
    let anySec = false;
    sec.querySelectorAll(".show-block").forEach(block => {
      const showTxt = block.querySelector(".show").textContent.toLowerCase();
      const seasonMatch = Array.from(block.querySelectorAll(".season"))
        .some(s => s.textContent.toLowerCase().includes(q));
      if (showTxt.includes(q) || seasonMatch) {
        block.style.display = "";
        anySec = true;
      } else {
        block.style.display = "none";
      }
    });
    sec.style.display = anySec ? "" : "none";
  });
});
</script>
</body>
</html>
"""
    Path(output_file).write_text(html, encoding="utf-8")
    print(f"Wrote {output_file}")

def generate_index_page(movie_count, show_count, output_file):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nick’s Movie & TV Show List</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 20px; text-align: center; }}
    h1 {{ margin-bottom: 10px; }}
    .meta {{ color: #555; margin-bottom: 20px; }}
    .btn {{ display: block; margin: 10px auto; padding: 12px 20px;
            background: #17a2b8; color: #fff; text-decoration: none;
            border-radius: 4px; width: 80%; max-width: 300px; }}
  </style>
</head>
<body>
  <h1>Nick’s Movie & TV Show List</h1>
  <div class="meta">
    Last updated: {now}<br>
    Movies: {movie_count} &nbsp;|&nbsp; TV Shows: {show_count}
  </div>
  <a href="movie_list.html" class="btn">View Movies</a>
  <a href="tv_show_list.html" class="btn">View TV Shows</a>
</body>
</html>
"""
    Path(output_file).write_text(html, encoding="utf-8")
    print(f"Wrote {output_file}")

def main():
    # Generate all pages
    movies = read_items_from_file("movie_list.txt")
    shows = read_items_from_file("tv_list.txt")

    generate_html_page("Movie List", movies, "..\\movie_list.html")
    print(f'Generated Movies html')
    generate_tv_html_page("TV Show List", shows, "..\\tv_show_list.html")
    print(f'Generated TV html')

    # TV show count excludes seasons
    unique_shows = {line.split(",")[0].strip() for line in shows if "," in line}
    generate_index_page(len(movies), len(unique_shows), "..\\index.html")
    print(f'Generated Index html')

if __name__ == "__main__":
    main()