import time
import requests
import re
from typing import Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}


class BookScraper:
    """Handles scraping operations for books.toscrape.com."""

    def __init__(self, delay: float = 1.0):
        """Initialize the scraper with a request delay.

        Args:
            delay: Seconds to wait between requests (default: 1.0)
        """
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def _get_soup(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch a page and return BeautifulSoup object.

        Args:
            url: URL to fetch

        Returns:
            BeautifulSoup object or None if request fails
        """
        try:
            time.sleep(self.delay)  # rate limiting
            response = self.session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def scrape_categories(self) -> list:
        """Scrape all available book categories.

        Returns:
            List of category names and URLs
        """
        soup = self._get_soup(BASE_URL)
        if not soup:
            return []

        # DOM Tree Navigation example 1: Parent -> Child -> Grandchild
        category_list = soup.find('ul', class_='nav-list').find('ul').find_all('li')
        return [
            {
                'name': li.a.text.strip(),
                'url': urljoin(BASE_URL, li.a['href'])
            }
            for li in category_list
        ]

    def scrape_books_in_category(self, category_url: str) -> list:
        """Scrape all books in a category.

        Args:
            category_url: URL of the category page

        Returns:
            List of book data dictionaries
        """
        books = []
        current_url = category_url

        while current_url:
            soup = self._get_soup(current_url)
            if not soup:
                break

            # Process books on current page
            # Different Selection Method 1: -> CSS Selector
            book_elements = soup.select('article.product_pod')
            for book in book_elements:
                try:
                    # Different Selection Method 2: -> Navigable String/Dictionary Access
                    title = book.h3.a['title']  # Attribute Chaining (DOM Tree Navigation example 2), Data Types Extracted 1: -> string
                    price_text = book.select('p.price_color')[0].text
                    # Data Types Extracted 2: -> Numeric Data (Float)
                    price = self._parse_price(price_text)
                    # Data Types Extracted 3: -> Attributes
                    rating = book.p['class'][1]  # Second class is the rating
                    # Data Types Extracted 4: -> Links (URLS)
                    book_url = urljoin(current_url, book.h3.a['href'])

                    # Get full book details by visiting book page
                    book_details = self._scrape_book_details(book_url)

                    books.append({
                        'title': title,
                        'price': price,
                        'rating': rating,
                        'availability': book_details.get('availability', ''),
                        'description': book_details.get('description', ''),
                        'url': book_url
                    })
                except (IndexError, KeyError, AttributeError) as e:
                    print(f"Error parsing book element: {e}")
                    continue

            # Check for next page
            # Different Selection Method 1: -> CSS Selector
            next_button = soup.select_one('li.next > a')
            if next_button:
                current_url = urljoin(current_url, next_button['href'])
            else:
                current_url = None

        return books

    def _parse_price(self, price_text: str) -> float:
        """Parse price text into float value.

        Args:
            price_text: Price text including currency symbol

        Returns:
            Price as float
        """
        try:
            # Remove non-numeric characters except decimal point
            cleaned = re.sub(r'[^\d.]', '', price_text)
            return float(cleaned)
        except ValueError:
            print(f"Could not parse price: {price_text}")
            return 0.0

    def _scrape_book_details(self, book_url: str) -> dict:
        """Scrape additional details from a book's individual page.

        Args:
            book_url: URL of the book's page

        Returns:
            Dictionary with availability and description
        """
        soup = self._get_soup(book_url)
        if not soup:
            return {}

        details = {}

        # Get availability
        # Different Selection Method 3: -> find()/find_all() with attributes
        availability = soup.find('p', class_='availability')
        if availability:
            # Data Types Extracted 5: -> Boolean-like Data
            details['availability'] = availability.get_text(strip=True)

        # Get description
        # Different Selection Method 3: -> find()/find_all() with attributes
        product_description = soup.find('div', id='product_description')
        if product_description:
            # DOM Tree Navigation example 3: Sibling Navigation
            description = product_description.find_next_sibling('p')
            if description:
                details['description'] = description.get_text(strip=True)

        return details