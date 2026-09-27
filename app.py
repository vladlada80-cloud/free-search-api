from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

SEARXNG_URL = "https://search.ononoki.org"


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
            "error": "Missing query"
        }), 400

    try:
        response = requests.get(
            f"{SEARXNG_URL}/search",
            params={
                "q": query,
                "format": "json",
                "categories": "general"
            },
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )

        data = response.json()

        results = []

        for item in data.get("results", [])[:10]:
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": item.get("content", "")
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
