import requests
from bs4 import BeautifulSoup
import datetime
import re
import config

def clip_article():
    print("🌐 Welcome to the Second Brain Web Clipper!")
    url = input("Paste the URL of the article: ").strip()
    
    if not url:
        print("No URL provided. Exiting.")
        return

    print("   📡 Fetching webpage...")
    try:
        # We use a standard User-Agent so websites don't block our script thinking it's a malicious bot
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the Title
        title = soup.title.string if soup.title else "Clipped_Article"
        safe_title = re.sub(r'[\\/*?:"<>|]', "", title).strip() # Remove characters that break file names
        
        # Extract the actual content (finding all paragraph tags)
        print("   🧹 Cleaning formatting and extracting text...")
        paragraphs = soup.find_all('p')
        article_text = "\n\n".join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 20])
        
        if not article_text:
            print("⚠️ Could not extract meaningful paragraph text from this page.")
            return

        # Format and save the output directly to your inbox
        filename = f"Clipped - {safe_title[:50]}.txt"
        filepath = config.INBOX_DIR / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"Source URL: {url}\n")
            f.write(f"Clipped on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write("-" * 40 + "\n\n")
            f.write(article_text)
            
        print(f"✅ Successfully clipped! Saved as '{filename}' in your inbox directory.")
        
    except Exception as e:
        print(f"❌ Error clipping article: {e}")

if __name__ == "__main__":
    clip_article()