#!/usr/bin/env python
# coding: utf-8

# IMPORT LIBRARIES
# ============================================================

import os
import time
import json
import re
from collections import deque, defaultdict

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

# SECTION 01: WEB CRAWLING
# ============================================================

SEED_URL = "https://www.wearetenet.com"

MAX_PAGES = 700

REQUEST_DELAY = 2

OUTPUT_DIR = "crawled_pages"


# Create the output directory if it does not already exist
os.makedirs(OUTPUT_DIR, exist_ok=True)


# Extract the domain name from the seed URL
parsed_seed = urlparse(SEED_URL)

BASE_DOMAIN = parsed_seed.netloc


# URL VALIDATION
# ------------------------------------------------------------

def is_valid_url(url):
    """
    Check whether a URL is valid for crawling.

    The URL must:
    - Use HTTP or HTTPS
    - Belong to the selected domain
    - Not belong to the /uploads/ path
    """

    parsed = urlparse(url)

    return (
        parsed.scheme in {"http", "https"}
        and parsed.netloc == BASE_DOMAIN
        and not parsed.path.startswith("/uploads/")
    )


# FILE NAME CLEANING
# ------------------------------------------------------------

def clean_filename(url):
    """
    Convert a URL into a filename that can safely
    be used for storing the crawled page.
    """

    return re.sub(r'[^a-zA-Z0-9]', '_', url)


# INITIALIZE CRAWLER
# ------------------------------------------------------------

visited_urls = set()

url_queued = deque([SEED_URL])

page_count = 0


# CRAWLING LOOP
# ------------------------------------------------------------

while url_queued and page_count < MAX_PAGES:

    # Get the next URL from the queue
    curr_url = url_queued.popleft()

    # Skip the URL if it has already been visited
    if curr_url in visited_urls:
        continue

    try:

        print(
            f"Crawling ({page_count + 1}/{MAX_PAGES}): {curr_url}"
        )

        # Send a request to the webpage
        response = requests.get(
            curr_url,
            timeout=10
        )

        # Raise an exception for unsuccessful HTTP responses
        response.raise_for_status()

        # Mark the URL as visited
        visited_urls.add(curr_url)

        # Create a filename from the URL
        filename = clean_filename(curr_url) + ".txt"

        filepath = os.path.join(
            OUTPUT_DIR,
            filename
        )

        # Save the webpage content locally
        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(response.text)

        # Increase the number of successfully crawled pages
        page_count += 1

        # Parse the webpage HTML
        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Find all hyperlinks on the page
        for link in soup.find_all(
            "a",
            href=True
        ):

            # Convert relative URLs into absolute URLs
            absolute_url = urljoin(
                curr_url,
                link["href"]
            )

            # Add valid and unvisited URLs to the queue
            if (
                is_valid_url(absolute_url)
                and absolute_url not in visited_urls
            ):

                url_queued.append(
                    absolute_url
                )

        # Wait before sending the next request
        time.sleep(REQUEST_DELAY)

    except requests.exceptions.RequestException as e:

        print("Error:", e)

        # Wait before retrying the next URL
        time.sleep(REQUEST_DELAY)


# CRAWLING RESULTS
# ------------------------------------------------------------

print("\nCrawling completed.")

print(
    "Total number of pages collected:",
    page_count
)


# SECTION 02: INDEXING
# ============================================================

# Initialize the Porter Stemmer
stemmer = PorterStemmer()


# Load the English stop-word list
stop_word = set(
    stopwords.words("english")
)


# Create the inverted index
inv_index = defaultdict(list)


# TOKENIZATION
# ------------------------------------------------------------

def tokenize(text):
    """
    Extract alphabetic words from the document text.
    """

    return re.findall(
        r'\b[a-zA-Z]+\b',
        text
    )


# NORMALIZATION
# ------------------------------------------------------------

def normalize(tokens):
    """
    Normalize tokens by:
    - Converting them to lowercase
    - Removing stop words
    - Applying Porter stemming
    """

    result = []

    for token in tokens:

        # Convert token to lowercase
        token = token.lower()

        # Remove stop words and apply stemming
        if token not in stop_word:

            result.append(
                stemmer.stem(token)
            )

    return result


# PROCESS CRAWLED DOCUMENTS
# ------------------------------------------------------------

doc_id = 0


for filename in os.listdir(OUTPUT_DIR):

    filepath = os.path.join(
        OUTPUT_DIR,
        filename
    )

    # Read the crawled document
    with open(
        filepath,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:

        text = file.read()

    # Tokenize the document
    tokens = tokenize(text)

    # Normalize the tokens
    normal_tokens = normalize(tokens)

    # Add each unique term to the inverted index
    for term in set(normal_tokens):

        inv_index[term].append(
            doc_id
        )

    # Move to the next document ID
    doc_id += 1


# INDEXING RESULTS
# ------------------------------------------------------------

print(
    "Indexing complete"
)

print(
    "Total number of documents indexed:",
    doc_id
)


# SAVE INVERTED INDEX
# ============================================================

with open(
    "inverted_index.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        inv_index,
        f,
        indent=4
    )


print(
    "Inverted index saved as inverted_index.json"
)
