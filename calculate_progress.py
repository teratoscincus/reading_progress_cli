def calculate_progress(book_info):
    """
    Calculate progression of given book.
    Expects an instance of the Book class, a list of names of the finished chapters,
    and a string with the name of the chapter currently being read as elements of a
    list or tuple for an argument.
    Return a tuple of amount of pages left in given chapter, amount of pages read in
    given chapter, a percentage representing completion of given chapter, and a
    percentage representing completion of given book in total.
    """

    # Unpack list parameter.
    book, finished_chapters, current_chapter = book_info

    # Calculate reading progress.
    total_pages_read = 0
    for chapter in book.chapters:
        # Count total pages for each finished chapters.
        if chapter in finished_chapters:
            total_pages_read += book.chapters[chapter]["total_pages"]
        # Reading progress of chapter currently being read.
        elif chapter == current_chapter:
            current_chapter_total_pages = book.chapters[chapter]["total_pages"]
            current_chapter_pages_read = (
                book.current_page - book.chapters[chapter]["first_page"]
            )
            current_chapter_pages_left = (
                current_chapter_total_pages - current_chapter_pages_read
            )

    # Add number of read pages from chapter currently being read.
    total_pages_read += current_chapter_pages_read

    total_progress_percent = (total_pages_read / book.total_pages) * 100
    chapter_progress_percent = (
        current_chapter_pages_read / current_chapter_total_pages
    ) * 100

    return (
        current_chapter_pages_left,
        current_chapter_pages_read,
        chapter_progress_percent,
        total_progress_percent,
    )
