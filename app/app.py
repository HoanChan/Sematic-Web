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

@app.route('/api/deleteHS', methods=['POST'])
def api_deleteHS():
    id = request.form.get('id')
    result = main_controller.delete_HS(id)
    return jsonify(result)

@app.route('/api/getHS', methods=['GET'])
def api_getHS():
    id = request.args.get('id')
    hs = main_controller.get_HS(id)
    print(hs)
    dsLop = main_controller.get_dsLop()
    return render_template("_HS.html", dsLop=dsLop, hs=hs)

@app.route('/api/newHS', methods=['GET'])
def api_newHS():
    id, hs = main_controller.new_HS()
    dsLop = main_controller.get_dsLop()
    return {'id':id, 'html': render_template("_HS.html", dsLop=dsLop, hs=hs)}

@app.route('/api/saveHS', methods=['POST'])
def api_saveHS():
    id = request.form.get('id')
    hoTen = request.form.get('hoTen')
    hocLop = request.form.get('hocLop')
    ngaySinh = request.form.get('ngaySinh')
    gioiTinh = request.form.get('gioiTinh')
    result = main_controller.save_HS(id, hoTen, hocLop, ngaySinh, gioiTinh)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)