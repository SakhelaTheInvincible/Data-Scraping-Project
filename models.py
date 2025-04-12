class Book:
    """Represents a book with its attributes."""

    RATING_MAPPING = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    def __init__(self, title: str, price: float, rating: int, availability: str, description: str = None,
                 url: str = None):
        """Initialize a Book instance.

        Args:
            title: Title of the book
            price: Price in GBP
            rating: Star rating (1-5)
            availability: Stock availability text
            description: Book description (optional)
            url: URL to book page (optional)
        """
        self._title = title
        self._price = price
        self._rating = rating
        self._availability = availability
        self._description = description
        self._url = url

    @property
    def title(self) -> str:
        return self._title

    @property
    def price(self) -> float:
        return self._price

    @property
    def rating(self) -> int:
        return self._rating

    @property
    def availability(self) -> str:
        return self._availability

    @property
    def description(self) -> str:
        return self._description

    @property
    def url(self) -> str:
        return self._url

    def to_dict(self) -> dict:
        """Convert book attributes to dictionary."""
        return {
            'title': self.title,
            'price': self.price,
            'rating': self.rating,
            'availability': self.availability,
            'description': self.description,
            'url': self.url
        }

    def __str__(self) -> str:
        return f"Book(title='{self.title}', price={self.price}, rating={self.rating})"


class Category:
    """Represents a book category with its books."""

    def __init__(self, name: str):
        """Initialize a Category instance.

        Args:
            name: Name of the category
        """
        self._name = name
        self._books = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def books(self) -> list:
        return self._books

    @property
    def book_count(self) -> int:
        return len(self._books)

    def add_book(self, book: Book) -> None:
        """Add a book to the category.

        Args:
            book: Book object to add
        """
        self._books.append(book)

    def get_books_by_rating(self, min_rating: int = 3) -> list:
        """Get books with minimum specified rating.

        Args:
            min_rating: Minimum rating to filter by (default: 3)

        Returns:
            List of Book objects meeting the rating criteria
        """
        return [book for book in self._books if book.rating >= min_rating]

    def __str__(self) -> str:
        return f"Category(name='{self.name}', book_count={self.book_count})"