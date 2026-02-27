import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

OFFICIAL_SOURCES = {
    "UGC": "https://www.ugc.gov.in/",
    "AICTE": "https://www.aicte-india.org/",
    "MOE": "https://www.education.gov.in/"
}

MAX_PAGES_PER_SITE = 5   # Limit crawling depth for safety


def clean_text(text):
    lines = text.split("\n")
    clean_lines = []

    blacklist_keywords = [
        "Follow Us", "Twitter", "Facebook", "Instagram",
        "LinkedIn", "Skip to", "Screen Reader",
        "Text Size", "Contact Us"
    ]

    for line in lines:
        line = line.strip()
        if len(line) < 40:
            continue
        if any(word in line for word in blacklist_keywords):
            continue
        clean_lines.append(line)

    return "\n".join(clean_lines)


def fetch_html(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except:
        return ""


def extract_internal_links(base_url, soup):
    links = set()
    domain = urlparse(base_url).netloc

    for a in soup.find_all("a", href=True):
        full_url = urljoin(base_url, a["href"])
        if urlparse(full_url).netloc == domain:
            links.add(full_url)

    return list(links)


def crawl_site(name, base_url):
    visited = set()
    to_visit = [base_url]
    collected_text = ""

    while to_visit and len(visited) < MAX_PAGES_PER_SITE:
        url = to_visit.pop(0)

        if url in visited:
            continue

        html = fetch_html(url)
        if not html:
            continue

        soup = BeautifulSoup(html, "lxml")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator="\n")
        collected_text += "\n" + clean_text(text)

        visited.add(url)

        new_links = extract_internal_links(base_url, soup)
        for link in new_links:
            if link not in visited:
                to_visit.append(link)

    return collected_text

def fetch_all_policies():
    data = {}

    for name, url in OFFICIAL_SOURCES.items():
        print(f"Crawling {name} site...")
        data[name] = crawl_site(name, url)

    return data
