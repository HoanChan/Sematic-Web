from flask import Flask, render_template
from controllers.main_controller import MainController
import json

app = Flask(__name__, template_folder="views", static_folder="static")

# Khởi tạo controller
main_controller = MainController()

# Route mặc định
@app.route("/")
def index():
    # đọc file data/cards.json vào biến data
    data =  json.load(open('app/data/cards.json', encoding="utf-8"))
    print(data)
    return render_template("index.html", data=data)

# Route hiển thị thông tin hocSinh
# @app.route("/hocSinh/show/<str:id>")
# def showHocSinh(id):
#     hocSinh = main_controller.get_hocSinh(id)
#     return render_template("hocSinh.html", hocSinh=hocSinh)


if __name__ == "__main__":
    app.run(debug=True)