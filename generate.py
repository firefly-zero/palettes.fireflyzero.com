from __future__ import annotations
from pathlib import Path

import requests
from jinja2 import Environment, FileSystemLoader
from jinja_markdown2 import MarkdownExtension

URL = 'https://lospec.com/palette-list/load?colorNumberFilterType=exact&colorNumber=16&page={page}&tag=&sortingType=downloads'

def download()-> list[dict]:
    result = []
    for page in range(3):
        resp = requests.get(URL.format(page=page))
        resp.raise_for_status()
        result.extend(resp.json()["palettes"])
    return result

palettes = download()
env = Environment(loader=FileSystemLoader('templates'))
env.add_extension(MarkdownExtension)
public_dir = Path('public')
public_dir.mkdir(exist_ok=True)
template = env.get_template('index.html.j2')
content = template.render(palettes=palettes)
Path('public', 'index.html').write_text(content)
