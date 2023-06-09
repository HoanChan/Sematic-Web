from flask import render_template, request, jsonify
from models import default_world, onto, destroy_entity

def search_TB(ten, viTri):
    print(f'search_TB: ten = {ten}, viTri = {viTri}')
    query_str = """
    PREFIX s: <http://hc.com/school#>
    SELECT ?tb
    WHERE {
        ?tb a s:ThietBi.
    """
    if ten: query_str += '?tb s:ten ?ten.' + f'FILTER(REGEX(?ten, ".*{ten}.*","i")).'
    if viTri: query_str += '?tb s:viTri ?viTri. ' + f'FILTER(STRENDS(STR(?viTri), "#{viTri}")).'
    query_str += '}'
    # print(query_str)
    result = default_world.sparql(query_str)
    dsTB = []
    if result:
        dsTB = list(map(lambda tb: {'id': tb[0].name,
                                    'ten': tb[0].ten, 
                                    'viTri': tb[0].viTri.ten, 
                                    'soLuong': tb[0].soLuong}, result))
    return dsTB
def delete_TB(id):
    print(f'delete_TB: id = {id}')
    tb = onto.search_one(iri = f'*#{id}', type = onto.ThietBi)
    if tb:
        destroy_entity(tb)
        return True
    return False

def get_TB(id):
    print(f'get_TB: id = {id}')
    tb = onto.search_one(iri = f'*#{id}', type = onto.ThietBi)
    return tb

def new_TB():
    tb = onto.ThietBi()
    return tb.name, tb

def save_TB(id, ten, viTri, hanhKiem):
    print(f'save_TB: id = {id}, ten = {ten}, viTri = {viTri}, ngaySinh = {ngaySinh}, gioiTinh = {gioiTinh}, hanhKiem = {hanhKiem}')
    tb = onto.search_one(iri = f'*#{id}', type = onto.ThietBi)
    if tb:
        tb.ten = ten
        tb.viTri = onto.search_one(iri = f'*#{viTri}', type = onto.Phong)            
        tb.ngaySinh = ngaySinh
        tb.gioiTinh = gioiTinh
        tb.hanhKiem = hanhKiem
        apply_DiemSoTB_Rules(tb) # Áp dụng luật tính danh hiệu
        return True
    return False

def initRouteTB(app):        
    @app.route("/thietBi/edit")
    def thietBiEdit():
        dsPhong = onto.Phong.instances()
        dsTB = []
        return render_template("thietBi.html", dsPhong=dsPhong, dsTB=dsTB, edit=True)

    @app.route("/thietBi/search")
    def thietBiSearch():
        dsPhong = onto.Phong.instances()
        dsTB = []
        return render_template("thietBi.html", dsPhong=dsPhong, dsTB=dsTB, edit=False)

    @app.route('/api/dsTB', methods=['GET'])
    def api_dsTB():
        ten = request.args.get('ten')
        viTri = request.args.get('viTri')
        ngaySinh = request.args.get('ngaySinh')
        gioiTinh = request.args.get('gioiTinh')
        dsTB = search_TB(ten, viTri)
        # Đóng gói danh sách học sinh dưới dạng một mảng JSON và trả về cho người dùng
        return jsonify(dsTB)

    @app.route('/api/deleteTB', methods=['POST'])
    def api_deleteTB():
        id = request.form.get('id')
        result = delete_TB(id)
        return jsonify(result)

    @app.route('/api/getTB', methods=['GET'])
    def api_getTB():
        id = request.args.get('id')
        tb = get_TB(id)
        dsPhong = onto.Phong.instances()
        return render_template("_TB.html", dsPhong=dsPhong, tb=tb)

    @app.route('/api/newTB', methods=['GET'])
    def api_newTB():
        id, tb = new_TB()
        dsPhong = onto.Phong.instances()
        return {'id':id, 'html': render_template("_TB.html", dsPhong=dsPhong, tb=tb)}

    @app.route('/api/saveTB', methods=['POST'])
    def api_saveTB():
        id = request.form.get('id')
        ten = request.form.get('ten')
        viTri = request.form.get('viTri')
        ngaySinh = request.form.get('ngaySinh')
        gioiTinh = request.form.get('gioiTinh')
        hanhKiem = request.form.get('hanhKiem')
        result = save_TB(id, ten, viTri, hanhKiem)
        return jsonify(result)
