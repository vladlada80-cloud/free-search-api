from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

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
            "error": "Missing query"
        }), 400

    try:
        response = requests.get(
            "https://www.google.com/search",
            params={
                "q": query,
                "num": 10,
                "hl": "en"
            },
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/140.0.0.0 Safari/537.36"
                )
            },
            timeout=15
        )

        soup = BeautifulSoup(response.text, "html.parser")

        results = []

        for block in soup.select("div.MjjYud"):
            link = block.select_one("a")
            title = block.select_one("h3")

            if not link or not title:
                continue

            url = link.get("href")

            if not url or not url.startswith("http"):
                continue

            snippet_element = block.select_one(
                "div.VwiC3b"
            )

            results.append({
                "title": title.get_text(" ", strip=True),
                "url": url,
                "snippet": (
                    snippet_element.get_text(" ", strip=True)
                    if snippet_element
                    else ""
                )
            })

            if len(results) >= 10:
                break

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
