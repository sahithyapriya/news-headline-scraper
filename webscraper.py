import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = input("Enter the news website URL (e.g. https://www.ntnews.com): ").strip()
KEYWORD = input("Enter a keyword to highlight (or leave blank): ").strip()
HEADERS = {"User-Agent": "Mozilla/5.0"}

TAG_LIST = ['h1', 'h2', 'h3', 'a']

BANNED_WORDS = [
    'తెలంగాణ', 'జాతీయ', 'క్రీడలు', 'లైఫ్ స్టైల్', 'ఫోటోలు',
    'హైదరాబాద్', 'వీడియోలు', 'sports','సైన్స్‌ అండ్‌ టెక్నాలజీ','ఆంధ్రప్రదేశ్','ఎడ్యుకేషన్ & కెరీర్‌','లైఫ్‌స్టైల్‌','బ‌తుక‌మ్మ పాట‌లు','ఎవర్‌గ్రీన్‌', 'videos', 'photos',
    'opinion', 'editorial', 'world', 'business', 'advertisement',
    'subscribe', 'lifestyle', 'weather', 'home'
]

def fetch_html(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f" Error fetching page: {e}")
        return None

def extract_clean_headlines(html):
    soup = BeautifulSoup(html, 'html.parser')
    headlines = []

    for tag in soup.find_all(TAG_LIST):
        text = tag.get_text(strip=True)

        if not text or len(text) < 12:
            continue

        if any(banned.lower() in text.lower() for banned in BANNED_WORDS):
            continue

        if KEYWORD and KEYWORD.lower() in text.lower():
            text = text.replace(KEYWORD, f"**{KEYWORD}**")

        if text not in headlines:
            headlines.append(text)

    return headlines

def save_to_file(headlines):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = "headlines.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("NEWS HEADLINES\n")
        file.write("========================================\n")
        file.write(f"Scraped from: {URL}\n")
        file.write(f"Scraped on  : {timestamp}\n")
        file.write("========================================\n\n")

        for i, headline in enumerate(headlines, 1):
            file.write(f"{i}. {headline}\n")

    print(f"{len(headlines)} headlines saved to '{filename}'.")

def main():
    print("Starting News Scraper...")
    html = fetch_html(URL)
    if html:
        headlines = extract_clean_headlines(html)
        if headlines:
            save_to_file(headlines)
        else:
            print("No valid headlines found.")
    else:
        print("Failed to fetch HTML.")

if __name__ == "__main__":
    main()
