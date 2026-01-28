import requests
from bs4 import BeautifulSoup
import re
from fastapi import HTTPException

def scrape_wikipedia(url: str):
    if "wikipedia.org/wiki/" not in url:
        raise HTTPException(status_code=400, detail="Invalid Wikipedia URL")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Title
    title_tag = soup.find('h1', {'id': 'firstHeading'})
    title = title_tag.text.strip() if title_tag else "Unknown Title"

    # Summary (first meaningful paragraph)
    summary = ""
    content_div = soup.find('div', {'id': 'mw-content-text'})
    if content_div:
        # Find paragraphs in the parser output div
        parser_output = content_div.find('div', {'class': 'mw-parser-output'})
        if parser_output:
            for p in parser_output.find_all('p', recursive=False):
                if p.text.strip():
                    summary = p.text.strip()
                    break
    
    if not summary:
        summary = "No summary available."

    # Section Headings
    sections = []
    for h in soup.find_all(['h2', 'h3']):
        span = h.find('span', {'class': 'mw-headline'})
        if span:
            sections.append(span.text.strip())

    # Clean Content text (limited to avoid token limits, prioritizing query relevance)
    # We will extract text from paragraphs
    content_text = ""
    if content_div:
        paragraphs = content_div.find_all('p')
        content_text = "\n".join([p.text.strip() for p in paragraphs if p.text.strip()])
    
    # Simple cleanup
    content_text = re.sub(r'\[\d+\]', '', content_text) # Remove citation like [1]
    
    # Truncate content if too long (heuristic, can be adjusted)
    max_chars = 15000 
    if len(content_text) > max_chars:
        content_text = content_text[:max_chars]

    return {
        "title": title,
        "summary": summary,
        "sections": sections,
        "content_text": content_text
    }
