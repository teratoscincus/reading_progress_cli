import argparse

from library import Library
from calculate_progress import calculate_progress

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
# Bookmark page.
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
# List chapters of currently read book.
parser.add_argument(
    "-lc",
    "--list_chapters",
    nargs="?",
    const=True,
    help=("List chapters of currently read book."),
)
# List book titles in collection.
parser.add_argument(
    "-lb",
    "--list_books",
    nargs="?",
    const=True,
    help=("List book titles in collection."),
)
args = parser.parse_args()

# Init library.
library = Library()

# Add a new book.
if args.add_book:
    library.add_book()

# Change book currently being read.
if args.currently_reading:
    book_title = args.currently_reading.strip().lower()
    # Mark book as currently being read.
    library.set_currently_reading_book(book_title)

# Init book marked as currently being read.
currently_read_book = library.get_currently_read_book()

# Bookmark a page in book currently being read.
if args.bookmark_page:
    # Update value of current_page attribute.
    currently_read_book.bookmark_page(args.bookmark_page)

# Mark a chapter in book currently being read as completed.
if args.finished_chapter:
    chapter_title = args.finished_chapter.strip().lower()
    # Make sure given chapter is in the book.
    if chapter_title in currently_read_book.chapters:
        chapter = currently_read_book.chapters[chapter_title]

        # Mark given chapter as finished.
        chapter["finished"] = True

        # Make sure current page is not in a chapter marked as finished.
        current_page = currently_read_book.current_page
        # Attempt to bookmark current_page.
        currently_read_book.bookmark_page(current_page)
    else:
        warning_message = (
            f"'{chapter_title.title()}' is not a chapter of"
            f" '{currently_read_book.title.title()}'.\n"
            "Perhaps there was an typo in the given title, or it's part of another"
            " book?"
        )
        print(warning_message)

# Save changes.
library.archive_book(currently_read_book)

# List chapters of currently read book.
if args.list_chapters:
    print(f"\n  Currently reading '{currently_read_book.title.title()}'.")
    print("\n  Chapters of the book:")
    for chapter in currently_read_book.chapters:
        print(f"    · {chapter.title()}")
# List book titles in collection.
elif args.list_books:
    print(f"\n  Currently reading '{currently_read_book.title.title()}'.")
    print("\n  Books in collection:")
    for book_title in library.collection:
        print(f"    · {book_title.title()}")
# Show reading progress of book currently being read.
# Only do so when no listing or adding of a new book is made to reduce CLI clutter.
elif not args.add_book:
    # Used for below call to calculate_progress() and print().
    currently_read_chapter = currently_read_book.get_current_chapter_name()
    currently_finished_chapters = currently_read_book.get_finished_chapter_names()

    # Parse calculate_progress() call argument.
    currently_read_book_info = (
        currently_read_book,
        currently_finished_chapters,
        currently_read_chapter,
    )
    # Calculate reading progress.
    progress_info = calculate_progress(currently_read_book_info)
    (
        current_chapter_pages_left,
        current_chapter_pages_read,
        chapter_progress_percent,
        total_progress_percent,
    ) = progress_info

    # Print reading progress.
    # A chapter is currently being read.
    if chapter_progress_percent:
        progress_message = (
            f"\n  Currently reading '{currently_read_book.title.title()}'.\n"
            f"\n  You have {current_chapter_pages_left} pages left of"
            f" '{currently_read_chapter.title()}'.\n"
            f"  You have read {current_chapter_pages_read} pages in the chapter so far.\n"
            f"\n  Book progress:\t{round(total_progress_percent, 2)}%.\n"
            f"  Chapter progress:\t{round(chapter_progress_percent, 2)}%.\n"
        )
    # All chapters are finished.
    else:
        progress_message = (
            f"\n  Currently reading '{currently_read_book.title.title()}'.\n"
            f"  Book progress:\t{round(total_progress_percent, 2)}%.\n"
            "\n  Congratulation! You have read the entire book.\n"
        )
    print(progress_message)

    # Print bullet list of finished chapters.
    print("  Chapters finished:")
    for chapter in currently_finished_chapters:
        print(f"    · {chapter.title()}")
