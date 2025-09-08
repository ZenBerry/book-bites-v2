from flask import Flask, request, jsonify, send_file, redirect
from quote import quote 
from google import genai
import random

app = Flask(__name__)


client = genai.Client(api_key="AIzaSyCO4CaWfuolgFco93vdGbYEjqOf9CcqXws")


# Root route
@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    if not query:
        return redirect("/search")
    return send_file("main.html")

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
    filtered = [q for q in results if len(q.get("quote", "")) <= 300]
    selected = random.sample(filtered, min(11, len(filtered)))
    
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
