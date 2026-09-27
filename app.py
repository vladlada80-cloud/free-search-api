from flask import Flask, request, jsonify
from duckduckgo_search import DDGS

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "service": "Free Search API"
    })

@app.route("/search")
def search():
    query = request.args.get("q")

    if not query:
        return jsonify({
            "error": "Missing query. Use /search?q=your_query"
        }), 400

    try:
        results = []

        with DDGS() as ddgs:
            search_results = ddgs.text(
                query,
                max_results=10
            )

            for result in search_results:
                results.append({
                    "title": result.get("title"),
                    "url": result.get("href"),
                    "snippet": result.get("body")
                })

        return jsonify({
            "query": query,
            "results": results
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080
    )
