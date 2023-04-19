from __future__ import annotations
from nltk import sent_tokenize, word_tokenize, download
from nltk.corpus import stopwords
from PyPDF2 import PdfReader
from collections import Counter
from re import compile

from app.constants import SENTENCE_DELIMETER


# Define the stop words
download('punkt')
download('stopwords')
stop_words = set(stopwords.words('english'))
newline_pattern = compile(r'(\n|\\n)')


def get_pasrsed_pages_sentences(pdf_reader: PdfReader):
    for page_object in pdf_reader.pages:
        page_text = ''.join(
            newline_pattern.sub('', page_object.extract_text())
        )
        # Tokenize the page text into sentences
        sentences = sent_tokenize(page_text)

        yield SENTENCE_DELIMETER.join(sentences)


def keyword_search(text: str, keyword: str):
    keyword_lower = keyword.lower()
    # Check each sentence for the keyword
    return [
        sentence
        for sentence in text.split(SENTENCE_DELIMETER)
        if keyword_lower in sentence.lower()
    ]


def get_top_words(text: str, num_words=5):
    # Tokenize the page text into words
    words = word_tokenize(text)

    # Filter out stop words and non-alphabetic tokens
    filtered_words = [
        word.lower()
        for word in words
        if word.isalpha()
        and word.lower() not in stop_words
        and len(word) > 1
    ]

    # Count word occurrences and find the top num_words
    word_counts = Counter(filtered_words)
    top_words_counts = word_counts.most_common(num_words)

    return [
        {'word': word, 'count': count}
        for word, count in top_words_counts
    ]
