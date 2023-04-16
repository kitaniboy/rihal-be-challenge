from __future__ import annotations
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from PyPDF2 import PdfFileReader
from collections import Counter


# Define the stop words
stop_words = set(stopwords.words('english'))


def get_pasrsed_sentences(pdf_reader: PdfFileReader):
    num_pages = pdf_reader.numPages

    for page_num in range(num_pages):
        page = pdf_reader.getPage(page_num)
        page_text = page.extractText()

        # Tokenize the page text into sentences
        sentences = sent_tokenize(page_text)

        yield from sentences


def keyword_search(text: str, keyword: str):
    # Check each sentence for the keyword
    return [
        sentence
        for sentence in text.split('\n')
        if keyword.lower() in sentence.lower()
    ]


def get_top_words(text: str, num_words=5):
    # Tokenize the page text into words
    words = word_tokenize(text)

    # Filter out stop words and non-alphabetic tokens
    filtered_words = [
        word.lower()
        for word in words
        if word.isalpha() and word.lower() not in stop_words
    ]

    # Count word occurrences and find the top num_words
    word_counts = Counter(filtered_words)
    top_words = word_counts.most_common(num_words)

    return dict(top_words)
