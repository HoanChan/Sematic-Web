from flask import render_template, request, jsonify
from models import default_world, onto, destroy_entity

def delete_HD(id):
    print(f'delete_HD: id = {id}')
    hd = onto.search_one(iri = f'*#{id}', loai = onto.HoatDong)
    if hd:
        destroy_entity(hd)
        return True
    return False

def get_HD(id):
    print(f'get_HD: id = {id}')
    hd = onto.search_one(iri = f'*#{id}', loai = onto.HoatDong)
    return hd

def new_HD():
    hd = onto.HoatDong()
    return hd.name, hd

def save_HD(id, ten, hocHD, ngaySinh, gioiTinh, hanhKiem):
    print(f'save_HD: id = {id}, ten = {ten}, hocHD = {hocHD}, ngaySinh = {ngaySinh}, gioiTinh = {gioiTinh}, hanhKiem = {hanhKiem}')
    hd = onto.search_one(iri = f'*#{id}', loai = onto.HoatDong)
    if hd:
        hd.ten = ten
        hd.hocHD = onto.search_one(iri = f'*#{hocHD}', loai = onto.HoatDong)            
        hd.ngaySinh = ngaySinh
        hd.gioiTinh = gioiTinh
        hd.hanhKiem = hanhKiem
        return True
    return False
def get_dsHD():    
    dsHD = []
    for hd in onto.HoatDong.instances():
        hd = {'name': hd.name, 'ten': hd.ten, 'ngayBD': hd.ngayBatDau, 'ngayKT': hd.ngayKetThuc, 'slQL': len(hd.quanLy), 'slTV':  len(hd.thamGia)}
        dsHD.append(hd)
    # print(f'get_dsHD: dsHD = {dsHD}')
    return dsHD

def initRouteHD(app):        
    @app.route("/hoatDong/edit")
    def hoatDongEdit():
        return render_template("hoatDong.html", dsHD = get_dsHD(), edit=True)

    @app.route("/hoatDong/search")
    def hoatDongSearch():
        return render_template("hoatDong.html", dsHD = get_dsHD(), edit=False) 

    @app.route('/api/dsHD', methods=['GET'])
    def api_dsHD():
        ten = request.args.get('ten')
        loai = request.args.get('loai')
        dsHD = search_HD(ten, loai)
        # Đóng gói danh sách học sinh dưới dạng một mảng JSON và trả về cho người dùng
        return jsonify(dsHD)

    @app.route('/api/deleteHD', methods=['POST'])
    def api_deleteHD():
        id = request.form.get('id')
        result = delete_HD(id)
        return jsonify(result)

    @app.route('/api/getHD', methods=['GET'])
    def api_getHD():
        id = request.args.get('id')
        hd = get_HD(id)
        dsHD = onto.HoatDong.instances()
        return render_template("_HD.html", dsHD=dsHD, hd=hd)

    @app.route('/api/newHD', methods=['GET'])
    def api_newHD():
        id, hd = new_HD()
        dsHD = onto.HoatDong.instances()
        return {'id':id, 'html': render_template("_HD.html", dsHD=dsHD, hd=hd)}

    @app.route('/api/saveHD', methods=['POST'])
    def api_saveHD():
        id = request.form.get('id')
        ten = request.form.get('ten')
        hocHD = request.form.get('hocHD')
        ngaySinh = request.form.get('ngaySinh')
        gioiTinh = request.form.get('gioiTinh')
        hanhKiem = request.form.get('hanhKiem')
        result = save_HD(id, ten, hocHD, ngaySinh, gioiTinh, hanhKiem)
        return jsonify(result)
