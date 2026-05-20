from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route("/")
def empty_index():
    return render_template('index.html')

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/index.html")
def index2():
    return render_template('index.html')

@app.route("/categories2.html")
def try_categories():
    return render_template('categories2.html')

@app.route("/categories.html")
def categories():
    return render_template('categories.html')

@app.route("/categories")
def categories2():
    return render_template('categories.html')

@app.route("/categories-thermal-paper.html")
def thermal():
    return render_template('thermal_paper.html')

@app.route("/categories-thermal-paper")
def thermal2():
    return render_template('thermal_paper.html')

@app.route("/cart.html")
def cart():
    return render_template('cart.html')

@app.route("/cart")
def cart2():
    return render_template('cart.html')

@app.route("/privacy-policy")
def priva():
    return render_template('privacy-policy.html')

@app.route("/terms-and-conditions")
def terms():
    return render_template('terms.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)