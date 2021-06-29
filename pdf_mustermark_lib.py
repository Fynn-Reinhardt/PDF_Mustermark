# -*- coding: utf-8 -*-
import re  # regex
import fitz  # pdf library


class PDFMustermark:
    """
    This class can search for instances of RegEx patterns in a PDF file and
    automatically highlight those instances.

    Attributes:
        doc: The PDF document
        pat: The RegEx Pattern
    """

    doc = None  # file object
    pat = None

    def __init__(self, file):
        """
        Constructor of the PDFMustermark class.

        Parameters:
            file: File name of the PDF that is to be worked on

        Throws:
            RuntimeError:
        """
        try:
            self.doc = fitz.open(file)
        except RuntimeError:
            raise

    def match_words(self, page, regex=None):
        """
        Matches words of a page with a RegEx pattern.

        Parameters:
            page: Page of the document.
            regex: RegEx pattern to be used. Uses the pat attribute if not
            specified. (default: None)

        Returns:
            List: A list of the words on the page that match the RegEx pattern.
        """
        if (regex):
            matches = re.findall(regex, self.doc[page].get_text())
        else:
            matches = self.pat.findall(self.doc[page].get_text())

        return matches

    def mark_word(self, page, target):
        """
        Marks all lines on a page that contain target.

        Parameters:
            page: Page of the document.
            target: Word that is to be highlighted.
        """
        wlist = self.doc[page].getText("words")  # make the word list
        for w in wlist:  # scan through all words on page
            if target in w[4]:  # w[4] is the word's string
                r = fitz.Rect(w[:4])  # make rect from word bbox
                anno = self.doc[page].add_highlight_annot(r)  # highlight
                anno.set_info(content=target)

    def mark_page(self, page, targets):
        """
        Executes mark_word() for a list of targets.

        Parameters:
            page: Page of the document.
            targets: List of targets.
        """
        for target in targets:
            self.mark_word(page, target)

    def mark_document(self, regex):
        """
        Marks all lines in a document that contain words that match the given
        regex expression.

        Parameters:
            regex: RegEx pattern to be used.
        """
        self.pat = re.compile(regex)
        for page in range(self.doc.page_count):
            self.mark_page(page, self.match_words(page))

    def save_close(self, file):
        """
        Saves the PDF file to a specified location.

        Parameters:
            file: File name and location where the file should be saved.
        """
        try:
            self.doc.save(file)
        except RuntimeError:
            raise
