from scraper import BookScraper
from models import Book, Category
from storage import DataStorage


def main():
    # Initialize components
    scraper = BookScraper(delay=1.5)  # conservative delay
    storage = DataStorage()

    print("Starting scraping process...")

    # Step 1: Scrape all categories
    print("Fetching categories...")
    categories_data = scraper.scrape_categories()

    if not categories_data:
        print("Failed to fetch categories. Exiting.")
        return

    # Step 2: Scrape books for each category
    all_categories = []
    all_books = []

    for cat_data in categories_data[:3]:  # Limit to 3 categories for demo
        print(f"Scraping category: {cat_data['name']}...")
        books_data = scraper.scrape_books_in_category(cat_data['url'])

        # Create Category and Book objects
        category = Category(cat_data['name'])

        for book_data in books_data:
            book = Book(
                title=book_data['title'],
                price=book_data['price'],
                rating=book_data['rating'],
                availability=book_data['availability'],
                description=book_data.get('description', ''),
                url=book_data['url']
            )
            category.add_book(book)
            all_books.append(book_data)

        all_categories.append(category)

    # Step 3: Save data
    print("Saving data...")
    storage.save_to_csv(all_books, 'output/books.csv')

    # Convert categories to serializable format for JSON
    categories_serializable = [
        {
            'name': cat.name,
            'books': [book.to_dict() for book in cat.books]
        }
        for cat in all_categories
    ]
    storage.save_to_json(categories_serializable, 'output/categories.json')

    # Step 4: Process and analyze data
    print("Analyzing data...")
    analysis_results = storage.process_data(all_categories)
    storage.save_to_json(analysis_results, 'output/analysis.json')

    print("Scraping complete!")
    print(f"Total books scraped: {analysis_results['total_books']}")
    print(f"Categories analyzed: {len(analysis_results['categories'])}")


if __name__ == "__main__":
    main()
