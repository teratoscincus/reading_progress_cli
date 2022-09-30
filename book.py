class Book:
    """A representation of a book."""

    def __init__(self):
        """
        Init attributes:
        title as an empty string.
        currently_reading as False.
        current_page as an integer value of 1.
        chapters as an empty dict.
        """
        self.title = ""
        self.currently_reading = False
        self.current_page = 1
        self.chapters = {}

    def new_book(self):
        """Set values for the title and chapters attribute."""
        self.title = input("Title of book: ").lower()
        self._set_chapters()

    def _set_chapters(self):
        """Set the values of the chapters attribute."""
        print("Enter 'q' when there are no more chapters to add.")
        while True:
            chapter_name = input("Enter name of chapter: ").lower()
            if chapter_name == "q":
                break

            # First page is 1 for the first chapter.
            if len(self.chapters) == 0:
                chapter_first_page = 1
            else:
                chapter_first_page = chapter_last_page + 1

            chapter_last_page = self._set_page_number()
            chapter_total_pages = chapter_last_page - chapter_first_page

            self.chapters[chapter_name] = {
                "finished": False,
                "first_page": chapter_first_page,
                "last_page": chapter_last_page,
                "total_pages": chapter_total_pages,
            }

    def _set_page_number(self):
        """Set page number and check that it's a numerical value."""
        while True:
            page_number = input("Last page of chapter: ")
            try:
                return int(page_number)
            except ValueError:
                print("Must be a numerical value. Try again.")
