from flask import Flask, render_template
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

from controllers.nvCtrl import initRouteNV
initRouteNV(app)

from controllers.dsCtrl import initRouteDS
initRouteDS(app)

from controllers.tcCtrl import initRouteTC
initRouteTC(app)

from controllers.lhCtrl import initRouteLH
initRouteLH(app)

from controllers.mhCtrl import initRouteMH
initRouteMH(app)

from controllers.gdCtrl import initRouteGD
initRouteGD(app)

from controllers.hdCtrl import initRouteHD
initRouteHD(app)

from controllers.tbCtrl import initRouteTB
initRouteTB(app)

if __name__ == "__main__":
    app.run(debug=True)