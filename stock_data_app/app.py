from flask import Flask, render_template, jsonify
import scraper

app = Flask(__name__)

@app.route('/')
def stocks_data():
    # data = scraper.sorted_data()
    results = scraper.sorted_data()
    return jsonify(results=results)

if __name__ == "__main__":
    app.run(debug=True)

