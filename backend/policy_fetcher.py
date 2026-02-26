import os
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
import io

# ----------- Cleaning ----------
def clean_text(text):
    lines = text.split("\n")
    clean_lines = []

    blacklist_keywords = [
        "Follow Us", "Twitter", "Facebook",
        "Instagram", "LinkedIn",
        "Skip to", "Contact Us"
    ]

    for line in lines:
        line = line.strip()
        if len(line) < 40:
            continue
        if any(word in line for word in blacklist_keywords):
            continue
        clean_lines.append(line)

    return "\n".join(clean_lines)


# ----------- Online Web Sources ----------
OFFICIAL_SOURCES = {
    "AICTE_About": "https://www.aicte-india.org/about-us",
    "AICTE_Schemes": "https://www.aicte-india.org/schemes",
    "AICTE_Approval": "https://www.aicte-india.org/approval-process-handbook",

    "UGC_About": "https://www.ugc.gov.in/page/About-UGC.aspx",
    "UGC_Schemes": "https://www.ugc.gov.in/page/Schemes.aspx",

    "MOE_About": "https://www.education.gov.in/en/about-ministry"

    "AICTE_Approval_24_27": "https://cdnbbsr.s3waas.gov.in/s35938b4d054136e5d59ada6ec9c295d7a/uploads/2025/03/2025031399.pdf",
    "AICTE_Approval_23_24": "https://aiktc.ndl.gov.in/items/ea215e5b-5d31-4942-a4b7-391310f7e153",
    "AICTE_Approval_22_23": "https://rknec.edu/Registrar/AICTE%20APPROVALS/AICTE-Approval%20Process%20Handbook%202022-23.pdf",
    "UGC_Guidelines_Dev_Assist": "https://www.ugc.gov.in/oldpdf/xiplanpdf/universitesdevelopmentassitanceoctober.pdf",
    "UGC_Regulations_Draft_25": "https://www.pcla.co.in/images/2025/Draft_UGC_Regulations_2025.pdf",
    "UGC_Regulations_18": "https://nluo.ac.in/storage/2024/05/UGC-Regulations-2018-for-appointment-of-teachers-and-academic-staff.pdf",
}


# ----------- Online PDF Links ----------
PDF_URLS = [
    "https://www.education.gov.in/sites/upload_files/mhrd/files/NEP_Final_English_0.pdf"
    "NEP_2020": "https://www.education.gov.in/sites/upload_files/mhrd/files/NEP_Final_English_0.pdf",

    # AICTE Approval Handbook
    "AICTE_Approval_Handbook": "https://cdnbbsr.s3waas.gov.in/s35938b4d054136e5d59ada6ec9c295d7a/uploads/2025/03/2025031399.pdf",

    #  UGC Student Support
    "UGC_Student_Support": "https://www.ugc.ac.in/pdfnews/9118819_Students-Support.pdf",

    # UGC Regulations 2018
    "UGC_Regulations_2018": "https://nluo.ac.in/storage/2024/05/UGC-Regulations-2018-for-appointment-of-teachers-and-academic-staff.pdf",

]

# ----------- Local PDF Folder ----------
LOCAL_PDF_FOLDER = "backend/policies"


# ----------- Fetch Webpage ----------
def fetch_webpage(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        return clean_text(soup.get_text())
    except:
        return ""


# ----------- Extract Online PDF ----------
def extract_pdf_from_url(url):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        reader = PdfReader(io.BytesIO(response.content))

        text = ""
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"

        return clean_text(text)
    except:
        return ""


# ----------- Extract Local PDF ----------
def extract_local_pdf(filepath):
    try:
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
        return clean_text(text)
    except:
        return ""

# ----------- Fetch All Policies ----------
def fetch_all_policies():
    combined_text = ""

    # Web sources
    for url in WEB_SOURCES:
        combined_text += fetch_webpage(url) + "\n"

    # Online PDFs
    for url in PDF_URLS:
        combined_text += extract_pdf_from_url(url) + "\n"

    # Local PDFs
    if os.path.exists(LOCAL_PDF_FOLDER):
        for file in os.listdir(LOCAL_PDF_FOLDER):
            if file.endswith(".pdf"):
                path = os.path.join(LOCAL_PDF_FOLDER, file)
                combined_text += extract_local_pdf(path) + "\n"

    return combined_text
