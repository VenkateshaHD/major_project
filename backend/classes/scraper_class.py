import requests
from bs4 import BeautifulSoup
import urllib.parse

class ScraperService:
    def __init__(self):
        # We will use some realistic user agents to avoid immediate blocking
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'
        }

    def scrape_reviews(self, url: str):
        """
        Scrapes product reviews from a given URL.
        Since Amazon/Flipkart have strong anti-bot protections, this implementation
        will attempt a basic scrape but fall back to a mocked list of reviews if
        it fails to find standard review elements or gets blocked.
        """
        domain = urllib.parse.urlparse(url).netloc
        
        try:
            # We attempt a real GET request
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                reviews = []
                
                # Try Amazon specific review classes
                if 'amazon' in domain:
                    review_elements = soup.find_all('span', {'data-hook': 'review-body'})
                    for el in review_elements:
                        text = el.get_text(strip=True)
                        if text:
                            reviews.append(text)
                            
                # Try Flipkart specific review classes
                elif 'flipkart' in domain:
                    review_elements = soup.find_all('div', {'class': 't-ZTKy'})
                    for el in review_elements:
                        text = el.get_text(strip=True)
                        if text:
                            # Remove READ MORE text
                            text = text.replace('READ MORE', '').strip()
                            reviews.append(text)
                
                # If we actually found reviews, return them
                if len(reviews) > 0:
                    return reviews[:10] # limit to 10 for demo

            # If request fails or no reviews found, fall back to mock data
            print(f"Failed to scrape real reviews from {url}. Falling back to mock data.")
            return self._get_mock_reviews(domain)
            
        except Exception as e:
            print(f"Scraping error: {e}. Falling back to mock data.")
            return self._get_mock_reviews(domain)

    def _get_mock_reviews(self, domain):
        """Provides mock reviews for demonstration purposes."""
        return [
            f"This product I bought from {domain} is absolutely amazing. Highly recommend!",
            "Terrible quality, it broke within 2 days of usage. Do not buy.",
            "It's an okay product. Does what it says, but nothing spectacular.",
            "I love it! The best purchase I've made this year.",
            "Complete waste of money. The seller is unresponsive."
        ]
