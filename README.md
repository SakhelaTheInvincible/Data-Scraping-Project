# Books to Scrape Web Scraper

A Python web scraping project that extracts book data from [books.toscrape.com](http://books.toscrape.com/), a practice site for web scraping.

## Features

- **Comprehensive Data Collection**:
  - Scrapes book titles, prices, ratings, availability, and descriptions
  - Handles pagination across category pages
  - Respectful scraping with rate limiting

- **Advanced Parsing**:
  - Uses multiple BeautifulSoup selection methods
  - Extracts text, links, numeric data, and attributes
  - Robust error handling for missing elements

- **Data Processing**:
  - Calculates average prices per category
  - Analyzes rating distributions
  - Exports to both CSV and JSON formats

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/book-scraper.git
   cd book-scraper
   ```
   
2. Activate environment and install required packages:

   ```bash
   pip install beautifulsoup4 requests pandas
   ```

## Usage

Run the main script:

```bash
python main.py
```

The script will:

- Scrape all available book categories
- Extract book data from each category
- Save results to the output/ directory:
  - `books.csv`: All books in CSV format
  - `categories.json`: Books organized by category
  - `analysis.json`: Statistical analysis results

## Project Structure

```
book-scraper/
├── main.py          # Main execution script
├── scraper.py       # Web scraping logic
├── models.py        # Data models (Book, Category)
├── storage.py       # Data saving and processing
├── README.md
└── CONTRIBUTIONS.md
```

## Implementation Details

### Selection Methods

- CSS Selectors: `soup.select('article.product_pod')`
- Attribute Finders: `soup.find('p', class_='availability')`
- DOM Navigation: `product_description.find_next_sibling('p')`

### Data Types Extracted

- Text content (titles, descriptions)
- Numeric data (prices, ratings)
- Links (book URLs)
- Attributes (rating classes)
- Boolean-like Data (availability)

### Rate Limiting

- Configurable delay between requests (default: 1.5 seconds)
- Session reuse for efficiency
- Proper HTTP headers included

### Customization

Modify `main.py` to:

- Adjust scraping speed (delay parameter)
- Change number of categories to scrape
- Modify output file paths

