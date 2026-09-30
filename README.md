# Web Crawling and Indexing

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python\&logoColor=white)](https://www.python.org/)]
[![Requests](https://img.shields.io/badge/Requests-HTTP%20Library-orange)]
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-Web%20Scraping-green)]
[![NLTK](https://img.shields.io/badge/NLTK-Natural%20Language%20Processing-blue)]

A Python based **Web Crawling and Information Retrieval project** 

The project demonstrates two fundamental stages of an Information Retrieval system:

1. **Web Crawling** – collecting web pages from a selected domain.
2. **Indexing** – processing the collected content and building an inverted index for efficient document retrieval.

The crawler starts from a seed URL and collects up to 700 pages from the same domain. The collected documents are then tokenized, normalized, stop words are removed, and stemming is applied before constructing an inverted index stored in JSON format.

---

## Project Overview

The objective of this project was to develop a basic web crawler and indexing system using Python.

The system starts with the following seed website:

**Seed URL:** https://www.wearetenet.com

The crawler was configured to collect a maximum of **700 unique pages** from the same domain.

### Project Results

| Component          |           Result |
| ------------------ | ---------------: |
| Seed Domain        | `wearetenet.com` |
| Maximum Pages      |              700 |
| Pages Crawled      |          **700** |
| Documents Indexed  |          **700** |
| Request Delay      |        2 seconds |
| Index Format       |             JSON |
| Stemming Algorithm |   Porter Stemmer |

---

## System Workflow

```text
Seed URL
   │
   ▼
URL Queue
   │
   ▼
Web Crawler
   │
   ├── Check URL
   ├── Request Page
   ├── Handle Errors
   ├── Extract Links
   └── Save Page Content
   │
   ▼
Crawled Documents
   │
   ▼
Tokenization
   │
   ▼
Normalization
   │
   ├── Lowercase
   ├── Remove Stop Words
   └── Porter Stemming
   │
   ▼
Inverted Index
   │
   ▼
inverted_index.json
```

---

# Section 01: Web Crawling

The first section of the project implements a web crawler using Python.

The crawler begins from the seed URL:

```text
https://www.wearetenet.com
```

A queue is used to manage URLs waiting to be crawled, while a set keeps track of URLs that have already been visited.

### Crawling Configuration

```python
SEED_URL = "https://www.wearetenet.com"
MAX_PAGES = 700
REQUEST_DELAY = 2
OUTPUT_DIR = "crawled_pages"
```

### Domain Restriction

The crawler is restricted to the selected domain. This prevents it from following links to external websites.

```python
parsed_seed = urlparse(SEED_URL)
BASE_DOMAIN = parsed_seed.netloc
```

The `is_valid_url()` function checks whether a discovered URL:

* Uses HTTP or HTTPS.
* Belongs to the selected domain.
* Does not point to excluded `/uploads/` paths.

### URL Queue

A `deque` is used to manage URLs that still need to be processed.

```python
url_queued = deque([SEED_URL])
```

When a page is downloaded, its links are extracted and valid links are added to the queue.

### Page Collection

For each valid URL, the crawler:

1. Removes already visited URLs.
2. Sends an HTTP request.
3. Checks whether the request was successful.
4. Saves the page content locally.
5. Extracts links from the page.
6. Adds new valid links to the queue.
7. Waits for two seconds before continuing.

### Request Delay

A two-second delay is included between requests:

```python
time.sleep(REQUEST_DELAY)
```

This reduces the request rate and helps avoid sending requests to the server too rapidly.

### Error Handling

Request errors are handled using:

```python
try:
    ...
except requests.exceptions.RequestException as e:
    ...
```

If a request fails, the error is displayed and the crawler waits before continuing.

### Crawling Result

The crawler successfully collected:

**700 pages**

The pages were stored locally inside the `crawled_pages` directory.

---

# Section 02: Indexing

After the crawling stage, the collected documents are processed to create an **inverted index**.

The indexing process consists of:

```text
Documents
    ↓
Tokenization
    ↓
Lowercase Conversion
    ↓
Stop Word Removal
    ↓
Stemming
    ↓
Inverted Index
    ↓
JSON File
```

## Tokenization

The project uses a regular expression to extract alphabetic words from the collected content.

```python
def tokenize(text):
    return re.findall(r'\b[a-zA-Z]+\b', text)
```

For example:

```text
"Digital Marketing Services"
```

is converted into tokens such as:

```text
Digital
Marketing
Services
```

---

## Normalization

The tokens are converted to lowercase.

Stop words are removed using the NLTK English stop-word list.

```python
stop_word = set(stopwords.words('english'))
```

The project also applies the **Porter Stemmer**:

```python
stemmer = PorterStemmer()
```

The normalization process therefore performs:

* Lowercase conversion
* Stop-word removal
* Porter stemming

For example, words such as:

```text
marketing
marketed
marketer
```

may be reduced to a common stem.

---

# Inverted Index

The project builds an inverted index using a Python `defaultdict`.

```python
inv_index = defaultdict(list)
```

The inverted index maps a term to the document IDs in which that term occurs.

Conceptually:

```text
term → [document IDs]
```

For example:

```json
{
    "market": [1, 5, 12, 20],
    "design": [2, 7, 15],
    "seo": [3, 4, 9]
}
```

This structure allows a search system to determine which documents contain a particular term without scanning every document individually.

---

## Index Storage

The final inverted index is stored as:

```text
inverted_index.json
```

The JSON file is generated using:

```python
with open("inverted_index.json", "w", encoding="utf-8") as f:
    json.dump(inv_index, f, indent=4)
```

---

# Technologies Used

| Technology          | Purpose                                  |
| ------------------- | ---------------------------------------- |
| Python              | Main programming language                |
| Requests            | Sending HTTP requests                    |
| BeautifulSoup       | Parsing HTML and extracting links        |
| NLTK                | Natural language processing              |
| Porter Stemmer      | Word stemming                            |
| JSON                | Storing the inverted index               |
| Regular Expressions | Tokenization and filename cleaning       |
| Collections         | Queue and inverted-index data structures |

---

# Repository Structure

```text
Web-Crawling-and-Indexing/
│
├── README.md
├── requirements.txt
├── web_crawler_indexer.py
├── inverted_index.json
│
├── crawled_pages/
│   └── ...
│
└── notebook/
    └── web_crawling_indexing.ipynb
```

> The `crawled_pages` directory contains the locally stored pages collected during the crawling process. Depending on repository size, this directory may be excluded from GitHub and retained locally for demonstration purposes.

---

# Installation

Clone the repository:

```bash
git clone https://github.com/DeharaLudwick/Web-Crawling-and-Indexing.git
```

Navigate into the project:

```bash
cd Web-Crawling-and-Indexing
```

Install the required Python libraries:

```bash
pip install requests beautifulsoup4 nltk
```

Download the NLTK English stop-word dataset:

```python
import nltk
nltk.download('stopwords')
```

---

# Running the Project

Run the Python script:

```bash
python web_crawler_indexer.py
```

The crawler will begin from the configured seed URL and collect pages until the maximum page limit is reached.

The indexing stage will then process the collected documents and generate:

```text
inverted_index.json
```

---

# Project Output

The completed project produced:

* **700 crawled web pages**
* **700 indexed documents**
* A locally stored collection of crawled page content
* An `inverted_index.json` file containing the generated inverted index
