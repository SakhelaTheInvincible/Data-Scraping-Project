import json
import csv
import os
from typing import List, Dict
from models import Book, Category


class DataStorage:
    """Handles saving and loading scraped data."""

    @staticmethod
    def save_to_csv(data: List[Dict], filename: str) -> None:
        """Save data to CSV file.

        Args:
            data: List of dictionaries to save
            filename: Output filename
        """
        if not data:
            return

        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            keys = data[0].keys()

            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)

        except (IOError, OSError) as e:
            print(f"Error saving CSV file {filename}: {e}")

    @staticmethod
    def save_to_json(data, filename: str) -> None:
        """Save data to JSON file.

        Args:
            data: Data to serialize (should be JSON-serializable)
            filename: Output filename
        """
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        except (IOError, OSError, TypeError) as e:
            print(f"Error saving JSON file {filename}: {e}")

    @staticmethod
    def load_from_json(filename: str):
        """Load data from JSON file.

        Args:
            filename: JSON file to load

        Returns:
            Deserialized data or None if error occurs
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading JSON file {filename}: {e}")
            return None

    @staticmethod
    def process_data(categories: List[Category]) -> Dict:
        """Perform analysis on scraped data.

        Args:
            categories: List of Category objects

        Returns:
            Dictionary with analysis results
        """
        results = {
            'total_books': sum(cat.book_count for cat in categories),
            'categories': []
        }

        for category in categories:
            avg_price = sum(book.price for book in category.books) / category.book_count if category.book_count else 0
            rating_counts = {rating: 0 for rating in range(1, 6)}

            for book in category.books:
                rating = Book.RATING_MAPPING.get(book.rating, 0)
                if rating in rating_counts:
                    rating_counts[rating] += 1

            results['categories'].append({
                'name': category.name,
                'book_count': category.book_count,
                'average_price': round(avg_price, 2),
                'rating_distribution': rating_counts
            })

        return results
