"""Render the Flask templates into a static site in `dist/` for Netlify.

Netlify cannot run the Flask/gunicorn server, so only the static pages
(home, upload, about) and the `static/` assets are published. Uses only the
standard library so it runs without installing any pip packages.
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / 'dist'

# Same endpoint names as the routes in app.py
ROUTES = {'index': '/', 'upload': '/upload', 'about': '/about', 'popup': '/popup'}

PAGES = ['index.html', 'upload.html', 'about.html']

URL_FOR = re.compile(r"\{\{\s*url_for\(\s*['\"](\w+)['\"]\s*\)\s*\}\}")


def render(template):
    html = (ROOT / 'templates' / template).read_text(encoding='utf-8')
    html = URL_FOR.sub(lambda m: ROUTES[m.group(1)], html)
    leftover = re.search(r'\{\{|\{%', html)
    if leftover:
        raise ValueError(f'Unsupported template syntax in {template}: {html[leftover.start():leftover.start() + 60]!r}')
    return html


if OUT.exists():
    shutil.rmtree(OUT)
shutil.copytree(ROOT / 'static', OUT / 'static')

for page in PAGES:
    (OUT / page).write_text(render(page), encoding='utf-8')

print(f'Static site written to {OUT}')
