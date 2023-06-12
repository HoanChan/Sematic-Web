from flask import render_template, request, jsonify
from models import default_world, onto, destroy_entity

def delete_MH(id):
    print(f'delete_MH: id = {id}')
    tc = onto.search_one(iri = f'*#{id}', loai = onto.MonHoc)
    if tc:
        destroy_entity(tc)
        return True
    return False

def get_MH(id):
    print(f'get_MH: id = {id}')
    tc = onto.search_one(iri = f'*#{id}', loai = onto.MonHoc)
    return tc

def new_MH():
    tc = onto.MonHoc()
    return tc.name, tc

def save_MH(id, ten, hocMon, ngaySinh, gioiTinh, hanhKiem):
    print(f'save_MH: id = {id}, ten = {ten}, hocMon = {hocMon}, ngaySinh = {ngaySinh}, gioiTinh = {gioiTinh}, hanhKiem = {hanhKiem}')
    tc = onto.search_one(iri = f'*#{id}', loai = onto.MonHoc)
    if tc:
        tc.ten = ten
        tc.hocMon = onto.search_one(iri = f'*#{hocMon}', loai = onto.MonHoc)            
        tc.ngaySinh = ngaySinh
        tc.gioiTinh = gioiTinh
        tc.hanhKiem = hanhKiem
        return True
    return False
def get_dsMH():    
    dsMon = []
    for mh in onto.MonHoc.instances():
        ten = mh.ten
        soTiet = mh.soTiet
        slGV = len(mh.giaoVienDay)
        mh = {'ten': ten, 'soTiet': soTiet, 'slGV': slGV}
        dsMon.append(mh)
    return dsMon

def initRouteMH(app):        
    @app.route("/monHoc/edit")
    def monHocEdit():
        return render_template("monHoc.html", dsMon = get_dsMH(), edit=True)

    @app.route("/monHoc/search")
    def monHocSearch():
        return render_template("monHoc.html", dsMon = get_dsMH(), edit=False)

    @app.route('/api/dsMH', methods=['GET'])
    def api_dsMH():
        ten = request.args.get('ten')
        loai = request.args.get('loai')
        dsMH = search_MH(ten, loai)
        # Đóng gói danh sách học sinh dưới dạng một mảng JSON và trả về cho người dùng
        return jsonify(dsMH)

    @app.route('/api/deleteMH', methods=['POST'])
    def api_deleteMH():
        id = request.form.get('id')
        result = delete_MH(id)
        return jsonify(result)

    @app.route('/api/getMH', methods=['GET'])
    def api_getMH():
        id = request.args.get('id')
        tc = get_MH(id)
        dsMon = onto.MonHoc.instances()
        return render_template("_MH.html", dsMon=dsMon, tc=tc)

    @app.route('/api/newMH', methods=['GET'])
    def api_newMH():
        id, tc = new_MH()
        dsMon = onto.MonHoc.instances()
        return {'id':id, 'html': render_template("_MH.html", dsMon=dsMon, tc=tc)}

    @app.route('/api/saveMH', methods=['POST'])
    def api_saveMH():
        id = request.form.get('id')
        ten = request.form.get('ten')
        hocMon = request.form.get('hocMon')
        ngaySinh = request.form.get('ngaySinh')
        gioiTinh = request.form.get('gioiTinh')
        hanhKiem = request.form.get('hanhKiem')
        result = save_MH(id, ten, hocMon, ngaySinh, gioiTinh, hanhKiem)
        return jsonify(result)
