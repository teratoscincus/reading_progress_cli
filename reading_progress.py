import argparse

from library import Library

parser = argparse.ArgumentParser()
# Add new book.
parser.add_argument(
    "-ab",
    "--add_book",
    nargs="?",
    const=True,
    help=(
        "Add a new book to the collection."
        " Contents of the book will be filled in through the CLI."
    ),
)
# Change book marked as currently reading.
parser.add_argument(
    "-cr",
    "--currently_reading",
    help=(
        "Switch between books to mark as currently reading."
        " Specify the title of the book withing quotation marks."
    ),
)
# Mark a page as current page.
parser.add_argument(
    "-bp",
    "--bookmark_page",
    help=(
        "Bookmark current page of book marked as currently reading."
        " Accepts an integer."
    ),
    type=int,
)
# Mark a chapter as finished.
parser.add_argument(
    "-fc",
    "--finished_chapter",
    help=(
        "Log a chapter in the book marked as currently reading as finished."
        " Specify the name of the chapter withing quotation marks."
        " Checks if bookmarked page is in the chapter being marked as finished."
        " If so, the bookmark will be moved to the first page of the first chapter"
        " identified as unfinished."
    ),
)
args = parser.parse_args()

# Init library and book marked as currently being read.
library = Library()
currently_read_book = library.get_currently_read_book()

if args.add_book:
    library.add_book()

if args.currently_reading:
    # Mark book as currently being read.
    library.set_currently_reading_book(args.currently_reading)

if args.bookmark_page:
    # Update value of current_page attribute.
    currently_read_book.bookmark_page(args.bookmark_page)

if args.finished_chapter:
    chapter = currently_read_book.chapters[args.finished_chapter]

    # Mark given chapter as finished.
    chapter["finished"] = True

    # Make sure current page is not in a chapter marked as finished.
    current_page = currently_read_book.current_page
    # Attempt to bookmark current_page.
    currently_read_book.bookmark_page(current_page)


# Save changes.
library.archive_book(currently_read_book)
