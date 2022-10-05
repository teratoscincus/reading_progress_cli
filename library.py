import json
import pathlib

from book import Book

APP_DIR_PATH = pathlib.Path(__file__).parent.resolve()


class Library:
    """A representation of a library of books."""

    def __init__(self):
        """Init with archive and collection attribute."""
        self.archive = f"{APP_DIR_PATH}/archive.json"
        # Set collection attribute.
        self._get_collection()

    def _get_collection(self):
        """Set value of collection attribute by reading from a json file."""
        try:
            with open(self.archive, "r") as json_file:
                self.collection = json.load(json_file)
        except FileNotFoundError:
            with open(self.archive, "w") as json_file:
                self.collection = {}
                json.dump(self.collection, json_file)
            print("Archive not found. Creating a new empty archive json file.")

    def add_book(self):
        """Add a book to the library's collection."""
        book = Book()
        book.new_book()

        # Add book to collection and write to archive.
        self.archive_book(book)

    def set_currently_reading_book(self, book_title):
        """
        Mark book specified by title as currently being read, and return an instance of
        the book currently being read.
        Only one book at a time will be marked as currently being read.
        Removes status of currently being read from previous book that had it set to
        True.
        """
        if book_title in self.collection:
            # Remove status of previously read book.
            previously_read_book = self.get_currently_read_book()
            previously_read_book.currently_reading = False

            self.archive_book(previously_read_book)

            # Change status of book specifies by title.
            currently_read_book = self._get_book_by_title(book_title)
            currently_read_book.currently_reading = True

            # Return an instance of the book.
            return currently_read_book

    def _get_book_by_title(self, book_title):
        """Return an instance of a book specified by its title."""
        # Init book and assign value to its attributes.
        book = Book()
        book.title = book_title
        book.currently_reading = self.collection[book_title]["currently_reading"]
        book.total_pages = self.collection[book_title]["total_pages"]
        book.current_page = self.collection[book_title]["current_page"]
        book.chapters = self.collection[book_title]["chapters"]

        return book

    def get_currently_read_book(self):
        """Return an instance of the book marked as currently being read."""
        # Find book marked as currently being read.
        for book_title in self.collection:
            if self.collection[book_title]["currently_reading"] == True:
                break

        book = self._get_book_by_title(book_title)

        return book

    def archive_book(self, book):
        """
        Update the collection and write to the archive.
        Expects the argument for the book parameter to be an instance of a book.
        """
        self.collection[book.title] = {
            "currently_reading": book.currently_reading,
            "total_pages": book.total_pages,
            "current_page": book.current_page,
            "chapters": book.chapters,
        }
        with open(self.archive, "w") as json_file:
            json.dump(self.collection, json_file)
