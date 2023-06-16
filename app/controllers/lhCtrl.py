from flask import render_template, request, jsonify
from models import default_world, onto, destroy_entity

def delete_LH(id):
    print(f'delete_LH: id = {id}')
    tc = onto.search_one(iri = f'*#{id}', loai = onto.LopHoc)
    if tc:
        destroy_entity(tc)
        return True
    return False

def get_LH(id):
    print(f'get_LH: id = {id}')
    tc = onto.search_one(iri = f'*#{id}', loai = onto.LopHoc)
    return tc

def new_LH():
    tc = onto.LopHoc()
    return tc.name, tc

def save_LH(id, ten, hocLop, ngaySinh, gioiTinh, hanhKiem):
    print(f'save_LH: id = {id}, ten = {ten}, hocLop = {hocLop}, ngaySinh = {ngaySinh}, gioiTinh = {gioiTinh}, hanhKiem = {hanhKiem}')
    tc = onto.search_one(iri = f'*#{id}', loai = onto.LopHoc)
    if tc:
        tc.ten = ten
        tc.hocLop = onto.search_one(iri = f'*#{hocLop}', loai = onto.LopHoc)            
        tc.ngaySinh = ngaySinh
        tc.gioiTinh = gioiTinh
        tc.hanhKiem = hanhKiem
        return True
    return False
def get_dsLH():    
    dsLop = []
    for lh in onto.LopHoc.instances():
        ten = lh.ten
        gvcn = lh.giaoVienChuNhiem.hoTen if lh.giaoVienChuNhiem else ""
        phong = ''.join([x.ten for x in lh.phong]) if lh.phong else ""
        slHS = len(lh.dsHocSinh)
        lh = {'ten': ten, 'gvcn': gvcn, 'phong': phong, 'slHS': slHS}
        dsLop.append(lh)
    return dsLop

def initRouteLH(app):        
    @app.route("/lopHoc/edit")
    def lopHocEdit():
        return render_template("lopHoc.html", dsLop = get_dsLH(), edit=True)

    @app.route("/lopHoc/search")
    def lopHocSearch():
        return render_template("lopHoc.html", dsLop = get_dsLH(), edit=False)

    @app.route('/api/dsLH', methods=['GET'])
    def api_dsLH():
        ten = request.args.get('ten')
        loai = request.args.get('loai')
        dsLH = search_LH(ten, loai)
        # Đóng gói danh sách học sinh dưới dạng một mảng JSON và trả về cho người dùng
        return jsonify(dsLH)

    @app.route('/api/deleteLH', methods=['POST'])
    def api_deleteLH():
        id = request.form.get('id')
        result = delete_LH(id)
        return jsonify(result)

    @app.route('/api/getLH', methods=['GET'])
    def api_getLH():
        id = request.args.get('id')
        tc = get_LH(id)
        dsLop = onto.LopHoc.instances()
        return render_template("_LH.html", dsLop=dsLop, tc=tc)

    @app.route('/api/newLH', methods=['GET'])
    def api_newLH():
        id, tc = new_LH()
        dsLop = onto.LopHoc.instances()
        return {'id':id, 'html': render_template("_LH.html", dsLop=dsLop, tc=tc)}

    @app.route('/api/saveLH', methods=['POST'])
    def api_saveLH():
        id = request.form.get('id')
        ten = request.form.get('ten')
        hocLop = request.form.get('hocLop')
        ngaySinh = request.form.get('ngaySinh')
        gioiTinh = request.form.get('gioiTinh')
        hanhKiem = request.form.get('hanhKiem')
        result = save_LH(id, ten, hocLop, ngaySinh, gioiTinh, hanhKiem)
        return jsonify(result)
