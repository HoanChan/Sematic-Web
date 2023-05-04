from flask import Flask, render_template, request, jsonify
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
    return render_template("index.html", data=data)

# Route hiển thị thông tin hocSinh
# @app.route("/hocSinh/show/<string:id>")
# def showHocSinh(id):
#     hocSinh = main_controller.get_hocSinh(id)
#     return render_template("hocSinh.html", hocSinh=hocSinh)

@app.route("/hocSinh")
def hocSinh():
    dsLop = main_controller.get_dsLop()
    dsHS = []
    return render_template("hocSinh.html", dsLop=dsLop, dsHS=dsHS)

@app.route('/api/dsHS', methods=['GET'])
def api_dsHS():
    hoTen = request.args.get('hoTen')
    hocLop = request.args.get('hocLop')
    ngaySinh = request.args.get('ngaySinh')
    gioiTinh = request.args.get('gioiTinh')
    dsHS = main_controller.search_HS(hoTen, hocLop, ngaySinh, gioiTinh)
    # Đóng gói danh sách học sinh dưới dạng một mảng JSON và trả về cho người dùng
    return jsonify(dsHS)

if __name__ == "__main__":
    app.run(debug=True)