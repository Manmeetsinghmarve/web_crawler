import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Web crawler function
def crawl_webpage(url, max_depth, current_depth=0, visited=None):
    if visited is None:
        visited = set()

    # Stop if max depth is reached
    if current_depth > max_depth:
        return visited

    # Avoid revisiting the same page
    if url in visited:
        return visited

    visited.add(url)

    try:
        # Fetch page content
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        # Handle any request errors
        print(f"Error fetching {url}: {e}")
        return visited

    # Find all anchor tags with href
    for link in soup.find_all('a', href=True):
        next_url = urljoin(url, link['href'])
        if next_url not in visited:
            # Recursive crawl to the next depth level
            visited = crawl_webpage(next_url, max_depth, current_depth + 1, visited)

    return visited

# API to trigger the crawler
@app.route('/crawl', methods=['POST'])
def crawl_endpoint():
    try:
        # Extract parameters from the request
        data = request.get_json()
        root_url = data.get('url')
        depth = int(data.get('depth'))

        if not root_url or depth is None:
            return jsonify({"error": "Please provide both 'url' and 'depth'."}), 400

        # Start crawling the root webpage up to the given depth
        crawled_links = crawl_webpage(root_url, depth)
        return jsonify({"crawled_links": list(crawled_links)}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

