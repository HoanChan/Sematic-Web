from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__, template_folder="views", static_folder="static")

# Route mặc định
@app.route("/")
def index():
    # đọc file data/cards.json vào biến data
    data =  json.load(open('app/data/cards.json', encoding="utf-8"))
    return render_template("index.html", data=data)

from controllers.hsCtrl import initRouteHS
initRouteHS(app)

if __name__ == "__main__":
    app.run(debug=True)