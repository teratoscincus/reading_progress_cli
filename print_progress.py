def print_progress(currently_read_book_info, progress_info, unfinished_chapters):
    """
    Print a message to the CLI about the reading progress.
    Expects two tuple or list arguments.
    The first container should have a string with the title of a book, a list names of
    chapters that have been finished, and the name of the chapter currently being read.
    The second container should have two integers in succession followed bu two floating
    point values.
    """
    # Unpack params.
    (
        currently_read_book,
        currently_finished_chapters,
        currently_read_chapter,
    ) = currently_read_book_info
    (
        current_chapter_pages_left,
        current_chapter_pages_read,
        chapter_progress_percent,
        total_progress_percent,
    ) = progress_info

    # A chapter is currently being read.
    if currently_read_chapter:
        progress_message = (
            f"\n  Currently on page {currently_read_book.current_page} in"
            f" '{currently_read_book.title.title()}'.\n"
            f"\n  You have {current_chapter_pages_left} pages left of"
            f" '{currently_read_chapter.title()}'.\n"
            f"  You have read {current_chapter_pages_read} pages in the chapter so far."
            f"\n\n  Book progress:\t{round(total_progress_percent, 2)}%\n"
            f"  Chapter progress:\t{round(chapter_progress_percent, 2)}%"
        )
    # All chapters are finished.
    else:
        progress_message = (
            f"\n  Currently reading '{currently_read_book.title.title()}'.\n"
            f"  Book progress:\t{round(total_progress_percent, 2)}%\n"
            "\n  Congratulation! You have read the entire book."
        )
    print(progress_message)

    if currently_finished_chapters:
        # Print bullet list of finished chapters.
        print("\n  Chapters finished:")
        for i, chapter in enumerate(currently_finished_chapters):
            print(f"   {i}\t{chapter.title()}")

    if unfinished_chapters:
        # Print bullet list of finished chapters.
        print("\n  Chapters remaining:")
        for i, chapter in enumerate(unfinished_chapters):
            print(f"   {i}\t{chapter.title()}")
