import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
import io

# ----------- Cleaning ----------
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


# ----------- Official Sources ----------
OFFICIAL_SOURCES = {
    "UGC": "https://www.ugc.gov.in/",
    "AICTE": "https://www.aicte-india.org/",
    "MOE": "https://www.education.gov.in/"
}


# ----------- Fetch webpage ----------
def fetch_webpage(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print("Error fetching:", e)
        return ""


# ----------- Fetch all policies (SOURCE AWARE) ----------
def fetch_all_policies():
    data = {}

    for name, url in OFFICIAL_SOURCES.items():
        html = fetch_webpage(url)
        if not html:
            continue

        soup = BeautifulSoup(html, "html.parser")
        paragraphs = soup.find_all("p")

        raw_text = ""
        for p in paragraphs:
            raw_text += p.get_text() + "\n"

        data[name] = clean_text(raw_text)

    return data
