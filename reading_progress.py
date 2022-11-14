import argparse

from library import Library
from calculate_progress import calculate_progress
from print_progress import print_progress

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
    currently_read_book = library.set_currently_reading_book(book_title)

    # Check if given book title is in the library's collection.
    if currently_read_book:
        # Save changes.
        library.archive_book(currently_read_book)

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

        # Print reading progress.
        print_progress(currently_read_book_info, progress_info)
    else:
        print(
            f"\n  Sorry, couldn't find '{book_title}' in the collection.\n"
            "  Are you sure you spelled the title correctly?\n"
        )
        print("  Books currently in the collection:")
        for book_title in library.collection:
            print(f"    · {book_title.title()}")

# Init book marked as currently being read.
currently_read_book = library.get_currently_read_book()

# Bookmark a page in book currently being read.
if args.bookmark_page:
    # Update value of current_page attribute.
    currently_read_book.bookmark_page(args.bookmark_page)

    # Save changes.
    library.archive_book(currently_read_book)

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

        # Save changes.
        library.archive_book(currently_read_book)

        # Used for below call to calculate_progress() and print().
        currently_read_chapter = currently_read_book.get_current_chapter_name()
        currently_finished_chapters = currently_read_book.get_finished_chapter_names()
        currently_unfinished_chapters = (
            currently_read_book.get_unfinished_chapter_names()
        )

        # Parse calculate_progress() call argument.
        currently_read_book_info = (
            currently_read_book,
            currently_finished_chapters,
            currently_read_chapter,
        )
        # Calculate reading progress.
        progress_info = calculate_progress(currently_read_book_info)

        # Print reading progress.
        print_progress(
            currently_read_book_info, progress_info, currently_unfinished_chapters
        )
    else:
        warning_message = (
            f"\n  Sorry, couldn't find the chapter '{chapter_title.title()}' in the"
            " book.\n"
            "  Perhaps there was an typo in the given title, or it's part of another"
            " book?\n"
        )
        print(warning_message)
        # List chapters of currently read book.
        print(f"  Chapters of '{currently_read_book.title.title()}':")
        for chapter in currently_read_book.chapters:
            print(f"    · {chapter.title()}")

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
elif not (args.add_book or args.finished_chapter or args.currently_reading):
    # Used for below call to calculate_progress() and print_progress().
    currently_read_chapter = currently_read_book.get_current_chapter_name()
    currently_finished_chapters = currently_read_book.get_finished_chapter_names()
    currently_unfinished_chapters = currently_read_book.get_unfinished_chapter_names()

    # Parse calculate_progress() call argument.
    currently_read_book_info = (
        currently_read_book,
        currently_finished_chapters,
        currently_read_chapter,
    )
    # Calculate reading progress.
    progress_info = calculate_progress(currently_read_book_info)

    # Print reading progress.
    print_progress(
        currently_read_book_info, progress_info, currently_unfinished_chapters
    )
