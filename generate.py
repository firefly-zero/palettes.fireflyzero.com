from __future__ import annotations
import json
from pathlib import Path

import requests
from jinja2 import Environment, FileSystemLoader
from jinja_markdown2 import MarkdownExtension

URL = 'https://lospec.com/palette-list/load?colorNumberFilterType=exact&colorNumber=16&page={page}&tag=&sortingType=downloads'
ROOT = Path(__file__).parent


def download() -> list[dict]:
    result = []
    for page in range(3):
        resp = requests.get(URL.format(page=page))
        resp.raise_for_status()
        result.extend(resp.json()["palettes"])
    return result


def get_palettes() -> list[dict]:
    path = ROOT / ".palettes.json"
    if path.exists():
        return json.loads(path.read_text())
    result = download()
    path.write_text(json.dumps(result))
    return result


palettes = get_palettes()
env = Environment(loader=FileSystemLoader('templates'))
env.add_extension(MarkdownExtension)
public_dir = Path('public')
public_dir.mkdir(exist_ok=True)
template = env.get_template('index.html.j2')
content = template.render(palettes=palettes)
Path('public', 'index.html').write_text(content)
