import sys, pathlib
from playwright.sync_api import sync_playwright
html = pathlib.Path(sys.argv[1]).resolve().as_uri()
out = sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1600, "height": 1200})
    pg.goto(html)
    pg.wait_for_timeout(600)
    pg.screenshot(path=out, full_page=True)
    b.close()
print("ok", out)
