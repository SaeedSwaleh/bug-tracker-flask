from flask import Flask, render_template, request, redirect, url_for, flash
from models import User

app = Flask(__name__)
app.secret_key = "change-this-before-going-to-production"


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True) 