import sys
from bs4 import BeautifulSoup

def extract_content(html_file):
    try:
        with open(html_file, 'r') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.find_all('article', class_='day-desc')
        
        for article in articles:
            print(article.prettify())
            
    except Exception as e:
        print(f"Error extracting content: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 extract_content.py <html_file>", file=sys.stderr)
        sys.exit(1)
        
    extract_content(sys.argv[1])
