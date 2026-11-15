import requests
from flask import Flask, render_template

app = Flask(__name__)

MEME_API_URL = "https://meme-api.com/gimme/wholesomememes"


@app.route("/")
def index():
    response = requests.request("GET", MEME_API_URL, timeout=10)
    response.raise_for_status()
    meme = response.json()
    return render_template(
        "meme.html",
        meme_url=meme["url"],
        subreddit=meme["subreddit"],
    )


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")