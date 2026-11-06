# a. Run Flask in debug mode at 127.0.0.1.
# b. Create one route for the home page, "/".
# c. Return the welcome message when that route is requested.

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to Khaumu’s web site!"


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
