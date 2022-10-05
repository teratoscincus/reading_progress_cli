class Book:
    """A representation of a book."""

    def __init__(self):
        """
        Init attributes:
        title as an empty string.
        currently_reading as False.
        total_pages and current_page as an integer value of 1.
        chapters as an empty dict.
        """
        self.title = ""
        self.currently_reading = False
        self.total_pages = 1
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

            # Set total number of pages and break.
            if chapter_name == "q":
                self.total_pages = chapter_last_page
                break

            # First page is 1 for the first chapter.
            if len(self.chapters) == 0:
                chapter_first_page = 1
            else:
                chapter_first_page = chapter_last_page + 1

            # Ensure that an integer is given as page number.
            chapter_last_page = self._set_page_number()
            chapter_total_pages = chapter_last_page - chapter_first_page + 1

            # Set info for each chapter.
            self.chapters[chapter_name] = {
                "finished": False,
                "total_pages": chapter_total_pages,
                "first_page": chapter_first_page,
                "last_page": chapter_last_page,
            }

    def _set_page_number(self):
        """Set page number and check that it's a numerical value."""
        while True:
            page_number = input("Last page of chapter: ")
            try:
                return int(page_number)
            except ValueError:
                print("Must be a numerical value. Try again.")

    def bookmark_page(self, page_number):
        """
        Setter method for the current_page attribute, expects and integer argument.
        Doesn't allow page to bookmarked if it's in a chapter marked as finished.
        In such a case it will call a method to find the first chapter not marked as
        finished and place the bookmark on the first page of that chapter.
        """
        if page_number != None:
            for chapter in self.chapters:
                # Check what chapter the page is in.
                if (
                    self.chapters[chapter]["first_page"]
                    <= page_number
                    <= self.chapters[chapter]["last_page"]
                ):
                    # Name of chapter of given page number.
                    page_number_chapter = chapter
                    # Bookmark given page only if the chapter it's in is not finished.
                    if self.chapters[chapter]["finished"] == False:
                        self.current_page = page_number
                        break
            # If loop is exited without a break.
            # Happens when given page_number is not in an unfinished chapter.
            else:
                # Check for unfinished chapters.
                unfinished_chapter = self._get_first_unfinished_chapter_name()
                try:
                    # Bookmark first page of first unfinished chapter.
                    first_page = self.chapters[unfinished_chapter]["first_page"]

                # All chapters are finished.
                # Throws a KeyError if there are no unfinished chapters.
                except KeyError:
                    # Prevent progress greater than 100%.
                    self.current_page = None
                    error_message = "All chapters finished!"

                # In case an unfinished chapters is found.
                else:
                    self.current_page = first_page

                    error_message = (
                        f"Page {page_number} is in the chapter '{page_number_chapter.title()}'"
                        " that is marked as finished.\nNOTE: Placing bookmark on first page of"
                        f" '{unfinished_chapter.title()}' which is the first chapter"
                        " identified as unfinished."
                    )

                print(error_message)

    def _get_first_unfinished_chapter_name(self):
        """Return name of the first chapter in ascending order that is unfinished."""
        for chapter in self.chapters:
            if self.chapters[chapter]["finished"] == False:
                return chapter

    def get_finished_chapter_names(self):
        """Return a list of the names of chapters that are finished."""
        finished_chapters = []

        # Append all chapters marked as finished to list.
        for chapter in self.chapters:
            if self.chapters[chapter]["finished"] == True:
                finished_chapters.append(chapter)

        return finished_chapters

    def get_current_chapter_name(self):
        """
        Return a string with the name of the chapter containing the page that is
        bookmarked.
        """
        # current_page is None is all chapters are finished.
        if self.current_page:
            # Find chapter with bookmarked page.
            for chapter in self.chapters:
                if (
                    self.chapters[chapter]["first_page"]
                    <= self.current_page
                    <= self.chapters[chapter]["last_page"]
                ):
                    return chapter
