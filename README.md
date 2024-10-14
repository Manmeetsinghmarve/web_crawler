# web_crawler

This project is a simple web crawling API built using Python and Flask. It allows users to crawl a specified root webpage up to a certain depth and returns the crawled links in a JSON response.

## Features:

- Crawl a webpage recursively up to a given depth.
- Return a JSON list of crawled links.
- Handles invalid inputs and errors gracefully.
- Includes unit tests for key functionalities.

## Prerequisites:

- Python 3.7+
- pip (Python package installer)

## Dependencies:

Install the required Python packages with:

- bash:
    pip install -r requirements.txt

## Request:

{
  "url": "https://example.com",
  "depth": 2
}

## Response:

{
  "crawled_links": [
    "https://example.com",
    "https://example.com/page1",
    "https://example.com/page2"
  ]
}
# Testing

python -m unittest test_web_crawler.py
