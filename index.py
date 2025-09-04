from flask import Flask, request, jsonify, send_file, redirect
from quote import quote 

app = Flask(__name__)

# Root route
@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    if not query:
        return redirect("/search")
    return send_file("index.html")

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
    return jsonify(results)


app.run(debug=True, port=3000)
