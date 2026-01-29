from fastapi import FastAPI
import logging

from pydantic import BaseModel
from typing import Optional
import requests
import re
from bs4 import BeautifulSoup
logging.basicConfig(
    filename="api.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


app = FastAPI(title="NGO Phone Discovery API")

# -------- Models --------

class DiscoverRequest(BaseModel):
    ngo_name: str
    email: Optional[str] = None
    location: Optional[str] = None


class DiscoverResponse(BaseModel):
    ngo_name: str
    phone: Optional[str]
    confidence: float
    source: Optional[str]
    status: str


# -------- Constants --------

PHONE_REGEX = r'(\+91[\s\-]?\d{10}|\b\d{10}\b)'
HEADERS = {"User-Agent": "Mozilla/5.0"}


# -------- Helper Functions --------

def extract_domain(email: str):
    try:
        domain = email.split("@")[1].lower()
        if domain not in ["gmail.com", "yahoo.com", "outlook.com"]:
            return "https://" + domain
    except:
        return None
def search_official_website(ngo_name: str, location: str = ""):
    query = f"{ngo_name} {location} official website"
    url = f"https://duckduckgo.com/html/?q={query}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        results = soup.select(".result__a")
        for link in results[:3]:
            href = link.get("href")
            if href and "http" in href:
                return href
    except:
        pass

    return None



def crawl_page_for_phone(url: str):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text(" ")
        phones = re.findall(PHONE_REGEX, text)
        return list(set(phones))
    except:
        return []


def calculate_confidence(found_on_contact_page: bool, phone_count: int):
    score = 0.0

    if found_on_contact_page:
        score += 0.5

    if phone_count >= 2:
        score += 0.3
    elif phone_count == 1:
        score += 0.2

    return round(min(score, 1.0), 2)


# -------- Routes --------

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/discover-phone", response_model=DiscoverResponse)
def discover_phone(data: DiscoverRequest):
    logging.info(f"Search started for NGO: {data.ngo_name}")

    base_url = None

    # 1. Try email domain first
    if data.email:
        base_url = extract_domain(data.email)

    # 2. If email fails, search website
    if not base_url:
        base_url = search_official_website(
            data.ngo_name,
            data.location or ""
        )

    if not base_url:
        return DiscoverResponse(
            ngo_name=data.ngo_name,
            phone=None,
            confidence=0.0,
            source=None,
            status="not_found"
        )


    pages = [
        base_url,
        base_url + "/contact",
        base_url + "/about"
    ]

    for page in pages:
        phones = crawl_page_for_phone(page)
        if phones:
            logging.info(
                f"Phone found for {data.ngo_name} | Phone: {phones[0]} | Source: {page}"
            )

            confidence = calculate_confidence(
                found_on_contact_page="/contact" in page,
                phone_count=len(phones)
            )

            return DiscoverResponse(
                ngo_name=data.ngo_name,
                phone=phones[0],
                confidence=confidence,
                source=page,
                status="found"
            )

    logging.warning(f"No phone found for NGO: {data.ngo_name}")

    return DiscoverResponse(
        ngo_name=data.ngo_name,
        phone=None,
        confidence=0.0,
        source=None,
        status="not_found"
    )


