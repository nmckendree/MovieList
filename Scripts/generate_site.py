
import string
from collections import defaultdict

def generate_html_page(title, items, output_file):
    item_dict = defaultdict(list)
    for item in sorted(items, key=lambda x: x.lower()):
        first_char = item[0].upper()
        if first_char not in string.ascii_uppercase:
            first_char = "#"
        item_dict[first_char].append(item)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .menu {{ margin-bottom: 20px; }}
        .menu a {{ margin: 0 5px; text-decoration: none; font-weight: bold; }}
        .section {{ margin-bottom: 30px; }}
        .section h2 {{ border-bottom: 1px solid #ccc; }}
        .item {{ margin-left: 20px; }}
        #searchBar {{ margin-bottom: 20px; padding: 8px; width: 300px; }}
    </style>
</head>
<body>
    <input type="text" id="searchBar" placeholder="Search...">
    <div class="menu">
"""
    for letter in string.ascii_uppercase:
        if letter in item_dict:
            html += f'<a href="#{letter}">{letter}</a> '
    #for letter in sorted(item_dict.keys()):
    #    html += f'<a href="#{letter}">{letter}</a> '

    html += "</div>\n"

    for letter in sorted(item_dict.keys()):
        html += f'<div class="section" id="{letter}">\n<h2>{letter}</h2>\n'
        for item in item_dict[letter]:
            html += f'<div class="item">{item}</div>\n'
        html += "</div>\n"


    html += """
<script>
document.getElementById("searchBar").addEventListener("input", function() {
    var query = this.value.toLowerCase();
    var sections = document.querySelectorAll(".section");
    sections.forEach(function(section) {
        var items = section.querySelectorAll(".item");
        var anyVisible = false;
        items.forEach(function(item) {
            if (item.textContent.toLowerCase().includes(query)) {
                item.style.display = "";
                anyVisible = true;
            } else {
                item.style.display = "none";
            }
        });
        section.style.display = anyVisible ? "" : "none";
    });
});
</script>
</body>
</html>
"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

def read_items_from_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def generate_index_page():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Index</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        a { display: block; margin: 10px 0; font-size: 20px; }
    </style>
</head>
<body>
    <h1>Welcome</h1>
    <a href="movie_list.html">Movies</a>
    <a href="tv_show_list.html">TV Shows</a>
</body>
</html>
"""
    with open("..\\index.html", "w", encoding="utf-8") as f:
        f.write(html)

# Generate all pages
movies = read_items_from_file("Movies.txt")
shows = read_items_from_file("Shows.txt")

generate_html_page("Movie List", movies, "..\\movie_list.html")
print(f'Generated Movies html')
generate_html_page("TV Show List", shows, "..\\tv_show_list.html")
print(f'Generated TV html')
generate_index_page()
print(f'Generated Index html')
