import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import pandas as pd
import signal
import sys
from bs4 import XMLParsedAsHTMLWarning
import warnings
import time

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
REQUEST_DELAY = 1
MAX_DEPTH = 5

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


def get_content_type(response):
    content_type = response.headers.get("Content-Type", "").lower()

    if "xml" in content_type:
        return "xml"
    elif "html" in content_type:
        return "html"
    else:
        content = response.text[:1000].strip()
        if content.startswith(("<?xml", "<rss")):
            return "xml"
        return "html"


def get_soup(response):
    content_type = get_content_type(response)
    return BeautifulSoup(
        response.content, "lxml-xml" if content_type == "xml" else "lxml"
    )


def get_internal_links(start_url, output_file="internal_routes.csv"):
    base_url = start_url.rstrip("/")
    to_visit = {(start_url, 0)}
    visited = set()
    all_links = set()

    def save_progress():
        df = pd.DataFrame({"URL": sorted(all_links)})
        df.to_csv(output_file, index=False)
        print(f"\Process save in '{output_file}' ({len(all_links)} URLs)")

    def signal_handler(sig, frame):
        print("\Stoping crawler...")
        save_progress()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    headers = {"User-Agent": USER_AGENT}

    try:
        while to_visit:
            current_url, depth = to_visit.pop()

            if depth > MAX_DEPTH:
                continue

            try:
                time.sleep(REQUEST_DELAY)
                response = requests.get(current_url, headers=headers, timeout=10)
                if response.status_code != 200:
                    continue
            except Exception as e:
                print(f"Error when accessing {current_url}: {str(e)}")
                continue

            soup = get_soup(response)
            visited.add(current_url)
            all_links.add(current_url)

            for link in soup.find_all(["a", "link"], href=True):
                href = link["href"].strip()

                if not href or href.startswith(("javascript:", "mailto:", "tel:")):
                    continue

                absolute_url = urljoin(base_url, href).split("#")[0]
                normalized_url = absolute_url.rstrip("/")

                if normalized_url.startswith(base_url) and (
                    normalized_url not in visited
                ):
                    to_visit.add((normalized_url, depth + 1))
                    all_links.add(normalized_url)

            if len(all_links) % 10 == 0:
                save_progress()

    except Exception as e:
        print(f"Unespected error: {e}")

    save_progress()
    return sorted(all_links)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Use: python script.py <url> <output file.csv>")
        sys.exit(1)
    start_url = f"{sys.argv[1]}"
    output_file = f"{sys.argv[2]}"
    print(f"""Starting crawler with:
    - User-Agent: {USER_AGENT}
    - Delay betwen requests: {REQUEST_DELAY}s
    - Max depth : {MAX_DEPTH} levels
Press Ctrl+C to stop and save.""")

    internal_links = get_internal_links(start_url, output_file)
    print(
        f"Process complete. {len(internal_links)} URLs save's in '{output_file}'"
    )
