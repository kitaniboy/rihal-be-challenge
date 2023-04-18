from __future__ import annotations
from nltk import sent_tokenize, word_tokenize, download
from nltk.corpus import stopwords
from PyPDF2 import PdfReader
from collections import Counter


# Define the stop words
download('punkt')
download('stopwords')
stop_words = set(stopwords.words('english'))


def get_pasrsed_sentences(pdf_reader: PdfReader):
    num_pages = len(pdf_reader.pages)
    full_text = ''.join(
        pdf_reader.pages[page_number].extract_text()
        .replace('\n', '').replace('\\n', '')
        for page_number in range(num_pages)
    )

    # Tokenize the page text into sentences
    sentences = sent_tokenize(full_text)

    yield from sentences


def keyword_search(text: str, keyword: str):
    keyword_lower = keyword.lower()
    # Check each sentence for the keyword
    return [
        sentence
        for sentence in text.split('#$#')
        if keyword_lower in sentence.lower()
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
    top_words_counts = word_counts.most_common(num_words)

    return [
        {'word': word, 'count': count}
        for word, count in top_words_counts
    ]
