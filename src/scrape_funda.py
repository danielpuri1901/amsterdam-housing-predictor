"""
Funda Real Estate Scraper (Educational/Portfolio Use Only)

DISCLAIMER:
- This is for educational purposes and portfolio projects only
- Always check website's robots.txt and terms of service
- Add delays between requests to be respectful
- Do not use for commercial purposes without permission
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random


class FundaScraper:
    """
    Scrapes rental listings from Funda for Amsterdam student housing.

    USAGE GUIDELINES:
    - Use for personal learning/portfolio only
    - Add delays between requests (respectful scraping)
    - Check robots.txt before scraping
    - Don't overwhelm the server
    """

    def __init__(self):
        self.base_url = "https://www.funda.nl"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        self.listings = []

    def scrape_listings(self, city="amsterdam", max_pages=5):
        """
        Scrape rental listings from Funda.

        Args:
            city (str): City to search in
            max_pages (int): Number of pages to scrape

        Returns:
            pd.DataFrame: Scraped listings
        """
        print(f"🏠 Starting to scrape Funda listings for {city}...")
        print("⚠️  Remember: This is for educational use only!\n")

        for page in range(1, max_pages + 1):
            url = f"{self.base_url}/huur/{city}/p{page}/"

            print(f"Scraping page {page}/{max_pages}...")

            try:
                # Add delay to be respectful (2-5 seconds)
                time.sleep(random.uniform(2, 5))

                response = requests.get(url, headers=self.headers, timeout=10)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # This is a simplified example - actual selectors need updating
                    # based on current Funda website structure
                    listings = soup.find_all('div', class_='search-result')

                    for listing in listings:
                        try:
                            data = self._extract_listing_data(listing)
                            if data:
                                self.listings.append(data)
                        except Exception as e:
                            print(f"⚠️  Error parsing listing: {e}")
                            continue

                    print(f"✅ Page {page}: Found {len(listings)} listings")
                else:
                    print(f"❌ Failed to fetch page {page} (Status: {response.status_code})")

            except Exception as e:
                print(f"❌ Error on page {page}: {e}")
                continue

        print(f"\n🎉 Scraping complete! Total listings: {len(self.listings)}")
        return pd.DataFrame(self.listings)

    def _extract_listing_data(self, listing):
        """
        Extract data from a single listing.

        Note: Selectors need to be updated based on actual website structure.
        This is a template/example.
        """
        try:
            # Example structure - needs to be adapted to actual Funda HTML
            data = {
                'address': listing.find('h2', class_='address').text.strip() if listing.find('h2', class_='address') else None,
                'price': self._extract_price(listing),
                'size': self._extract_size(listing),
                'rooms': self._extract_rooms(listing),
                'location': self._extract_location(listing),
                'url': listing.find('a')['href'] if listing.find('a') else None
            }
            return data
        except Exception as e:
            return None

    def _extract_price(self, listing):
        """Extract price from listing (remove €, /mnd, etc.)"""
        try:
            price_elem = listing.find('span', class_='price')
            if price_elem:
                price_text = price_elem.text.strip()
                # Remove €, spaces, '/mnd', etc.
                price = ''.join(filter(str.isdigit, price_text))
                return int(price) if price else None
        except:
            return None

    def _extract_size(self, listing):
        """Extract size in m²"""
        try:
            size_elem = listing.find('span', text=lambda t: 'm²' in t if t else False)
            if size_elem:
                size_text = size_elem.text.strip()
                size = ''.join(filter(str.isdigit, size_text))
                return int(size) if size else None
        except:
            return None

    def _extract_rooms(self, listing):
        """Extract number of rooms"""
        try:
            rooms_elem = listing.find('span', text=lambda t: 'kamer' in t.lower() if t else False)
            if rooms_elem:
                rooms_text = rooms_elem.text.strip()
                rooms = ''.join(filter(str.isdigit, rooms_text))
                return int(rooms) if rooms else None
        except:
            return None

    def _extract_location(self, listing):
        """Extract neighborhood/district"""
        try:
            location_elem = listing.find('div', class_='location')
            return location_elem.text.strip() if location_elem else None
        except:
            return None

    def save_data(self, filename='data/raw/funda_scraped_data.csv'):
        """Save scraped data to CSV"""
        if self.listings:
            df = pd.DataFrame(self.listings)
            df.to_csv(filename, index=False)
            print(f"\n💾 Data saved to: {filename}")
            print(f"📊 Total records: {len(df)}")
            return df
        else:
            print("❌ No data to save!")
            return None


# Alternative: Using Funda's API (if available)
class FundaAPIClient:
    """
    Use Funda's official API (requires API key).

    More reliable and legal than scraping!
    Get API key from: https://www.funda.nl/api
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://partnerapi.funda.nl/feeds/Aanbod.svc"

    def get_listings(self, city="amsterdam", listing_type="huur"):
        """
        Fetch listings using official API.

        Note: Requires registered API key from Funda
        """
        url = f"{self.base_url}/json/{self.api_key}/?type={listing_type}&zo=/{city}/"

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return pd.DataFrame(data['Objects'])
            else:
                print(f"API Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None


def main():
    """
    Main function - Example usage
    """
    print("=" * 70)
    print("FUNDA REAL ESTATE SCRAPER")
    print("Educational/Portfolio Use Only")
    print("=" * 70)

    print("\n📋 IMPORTANT NOTES:")
    print("1. This scraper is for EDUCATIONAL purposes only")
    print("2. Always respect website's robots.txt and ToS")
    print("3. Use appropriate delays between requests")
    print("4. Consider using official APIs when available")
    print("5. Don't use scraped data commercially without permission\n")

    # Method 1: Web Scraping (Basic Example)
    print("METHOD 1: Web Scraping (Requires manual selector updates)")
    scraper = FundaScraper()

    # Note: This is a template - selectors need updating based on current site
    print("\n⚠️  WARNING: HTML selectors in this script are EXAMPLES only!")
    print("You need to inspect Funda's current website and update the selectors.")
    print("Use browser DevTools (F12) to find the correct CSS classes.\n")

    # Uncomment to run (after updating selectors):
    # df = scraper.scrape_listings(city="amsterdam", max_pages=2)
    # scraper.save_data()

    # Method 2: Using API (Recommended if you have access)
    print("\nMETHOD 2: Official API (RECOMMENDED)")
    print("Get API key from: https://www.funda.nl/api")
    print("This is the legal, reliable way to get Funda data!\n")

    # Example API usage (requires real API key):
    # api_client = FundaAPIClient(api_key="YOUR_API_KEY_HERE")
    # df = api_client.get_listings(city="amsterdam")

    print("\n💡 NEXT STEPS:")
    print("1. Register for Funda Partner API (recommended)")
    print("2. OR manually inspect Funda website and update CSS selectors")
    print("3. Run scraper with small page count first (test)")
    print("4. Process data using existing data_preprocessing.py")
    print("5. Retrain models with real data!")


if __name__ == "__main__":
    main()
