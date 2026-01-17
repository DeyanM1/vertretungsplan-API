from typing import Any, Sequence

from playwright.sync_api import sync_playwright

# Your exported cookies
cookies: Sequence[Any] = [
    {"name": "sid", "value": "g6t083i1ht77nferb96q6vaopr", "url": "https://www.start.schulportal.hessen.de"},
    {"name": "SPH-Session", "value": "2ef9c14ca844c3b3ab5feaee5d155b41904aa6c0242610108447ba301af8857f", "url": "https://www.start.schulportal.hessen.de"},
    {"name": "i", "value": "5201", "url": "https://www.start.schulportal.hessen.de"},

]

BASE_URL = "https://start.schulportal.hessen.de/meinunterricht.php"
OUTPUT_FILE = "protected.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = browser.new_page()

    # Set cookies
    page.context.add_cookies(cookies)

    # Go to the page
    page.goto(f"{BASE_URL}/meinunterricht.php")

    # Wait until network is idle (all JS/XHR finished)
    page.wait_for_load_state("networkidle")

    html = page.content()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    browser.close()

print("HTML saved to", OUTPUT_FILE)
