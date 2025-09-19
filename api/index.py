from flask import Flask, request, jsonify, send_file, redirect
from quote import quote 
from google import genai
import random

import os
import sys
print('LIST LIST')
print(os.listdir('.'))


if 'Zlibrary.py' in os.listdir('.'):
    from Zlibrary import Zlibrary
else:
    sys.path.append('./api')
    from Zlibrary import Zlibrary

from io import BytesIO


# Create Zlibrary object and login
Z = Zlibrary(email="zenberry.music@gmail.com", password="zlibPass8")

app = Flask(__name__)


client = genai.Client(api_key="AIzaSyCO4CaWfuolgFco93vdGbYEjqOf9CcqXws")


# Root route
@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    if not query:
        return redirect("/search")
    return send_file("main.html")

@app.route("/read")
def reader():
    return send_file("reader.html")

@app.route("/epub")
def get_epub():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Search for EPUB books
    results = Z.search(message=query, extensions='epub')
    if not results.get('books'):
        return jsonify({"error": "No books found"}), 404

    # Download first book as bytes
    book_info = results['books'][0]
    book_bytes = Z.downloadBook(book_info)[1]  # Assuming this returns bytes
    print(type(book_bytes), book_bytes)

    if not book_bytes:
        return jsonify({"error": "Failed to download book"}), 500

    # Send EPUB to client as a file-like object
    return send_file(
        BytesIO(book_bytes),
        mimetype='application/epub+zip',
        download_name=f"{book_info['title']}.epub",
        as_attachment=True
    )

# Route for the search page
@app.route("/search")
def search_page():
    return send_file("search.html")

# API endpoint to get quotes as JSON
@app.route("/quotes")
def get_quotes():
    search = request.args.get("q", "")
    limit = int(request.args.get("limit", 20))
    if not search:
        return jsonify([])

    results = quote(search, limit=limit)
    if not results:
        return jsonify([])
    filtered = [q for q in results if len(q.get("quote", "")) <= 300]
    selected = random.sample(filtered, min(11, len(filtered)))
    # print(results)
    
    return jsonify(selected)

@app.route("/related")
def get_related():
    current_author = request.args.get("q", "")
    if not current_author:
        return jsonify([])

    # 1. Get a related author
    response = client.models.generate_content(
        model="gemma-3-27b-it",
        contents=f"Please give me a book author who is similar to {current_author}. Just the name without a dot, nothing more, please."
    )
    related_author = response.text.strip()
    if not related_author:
        return jsonify([])

    # 2. Fetch quotes for that related author using the existing quote() function
    quotes_for_related = quote(related_author, limit=20)
    filtered = [q for q in quotes_for_related if len(q.get("quote", "")) <= 300]
    selected = random.sample(filtered, min(11, len(filtered)))
    

    return jsonify({
        "related_author": related_author,
        "quotes": selected
    })


if __name__ == "__main__":
    app.run(port=3000)
