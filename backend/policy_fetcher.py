import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

OFFICIAL_SOURCES = {
    "AICTE_About": "https://www.aicte-india.org/about-us",
    "AICTE_Schemes": "https://www.aicte-india.org/schemes",
    "AICTE_Approval": "https://www.aicte-india.org/approval-process-handbook",

    "UGC_About": "https://www.ugc.gov.in/page/About-UGC.aspx",
    "UGC_Schemes": "https://www.ugc.gov.in/page/Schemes.aspx",

    "MOE_About": "https://www.education.gov.in/en/about-ministry"
}


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


def fetch_webpage(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print("Error fetching:", e)
        return ""


def fetch_all_policies():
    data = {}

    for name, url in OFFICIAL_SOURCES.items():
        html = fetch_webpage(url)
        if not html:
            continue

        soup = BeautifulSoup(html, "lxml")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator="\n")
        cleaned = clean_text(text)

        data[name] = cleaned

    return data
