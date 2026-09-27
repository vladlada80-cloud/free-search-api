from flask import Flask, request, jsonify
import requests

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
        response = requests.get(
            "https://www.google.com/search",
            params={
                "q": query,
                "num": 10
            },
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=15
        )

        return jsonify({
            "query": query,
            "status": "search_request_sent",
            "source": "Google",
            "html_length": len(response.text)
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
