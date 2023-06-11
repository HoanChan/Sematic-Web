from flask import render_template, request, jsonify
from models import default_world, onto, destroy_entity
from utils import toDate

def search_HS(hoTen, hocLop, ngaySinh, gioiTinh):
    print(f'search_HS: hoTen = {hoTen}, hocLop = {hocLop}, ngaySinh = {ngaySinh}, gioiTinh = {gioiTinh}')
    query_str = """
    PREFIX s: <http://hc.com/school#>
    SELECT ?hs
    WHERE {
        ?hs a s:HocSinh.
    """
    if hoTen: query_str += '?hs s:hoTen ?hoTen.' + f'FILTER(REGEX(?hoTen, ".*{hoTen}.*","i")).'
    if hocLop: query_str += '?hs s:hocLop ?lop. ' + f'FILTER(STRENDS(STR(?lop), "#{hocLop}")).'
    if ngaySinh: query_str += f'?hs s:ngaySinh "{toDate(ngaySinh)}".'
    if gioiTinh: query_str += f'?hs s:gioiTinh "{gioiTinh}".'
    query_str += '}'
    # print(query_str)
    result = default_world.sparql(query_str)
    dsHS = []
    if result:
        dsHS = list(map(lambda hs: {'id': hs[0].name,
                                    'hoTen': hs[0].hoTen, 
                                    'hocLop': hs[0].hocLop.ten, 
                                    'ngaySinh': hs[0].ngaySinh, 
                                    'gioiTinh': hs[0].gioiTinh}, result))
    return dsHS
def delete_HS(id):
    print(f'delete_HS: id = {id}')
    hs = onto.search_one(iri = f'*#{id}', type = onto.HocSinh)
    if hs:
        destroy_entity(hs)
        return True
    return False

def get_HS(id):
    print(f'get_HS: id = {id}')
    hs = onto.search_one(iri = f'*#{id}', type = onto.HocSinh)
    return hs

def new_HS():
    hs = onto.HocSinh()
    return hs.name, hs

def save_HS(id, hoTen, hocLop, ngaySinh, gioiTinh, hanhKiem):
    print(f'save_HS: id = {id}, hoTen = {hoTen}, hocLop = {hocLop}, ngaySinh = {ngaySinh}, gioiTinh = {gioiTinh}, hanhKiem = {hanhKiem}')
    hs = onto.search_one(iri = f'*#{id}', type = onto.HocSinh)
    if hs:
        hs.hoTen = hoTen
        hs.hocLop = onto.search_one(iri = f'*#{hocLop}', type = onto.LopHoc)            
        hs.ngaySinh = ngaySinh
        hs.gioiTinh = gioiTinh
        hs.hanhKiem = hanhKiem
        return True
    return False

def initRouteHS(app):        
    @app.route("/hocSinh/edit")
    def hocSinhEdit():
        dsLop = onto.LopHoc.instances()
        dsHS = []
        return render_template("hocSinh.html", dsLop=dsLop, dsHS=dsHS, edit=True)

    @app.route("/hocSinh/search")
    def hocSinhSearch():
        dsLop = onto.LopHoc.instances()
        dsHS = []
        return render_template("hocSinh.html", dsLop=dsLop, dsHS=dsHS, edit=False)

    @app.route('/api/dsHS', methods=['GET'])
    def api_dsHS():
        hoTen = request.args.get('hoTen')
        hocLop = request.args.get('hocLop')
        ngaySinh = request.args.get('ngaySinh')
        gioiTinh = request.args.get('gioiTinh')
        dsHS = search_HS(hoTen, hocLop, ngaySinh, gioiTinh)
        # Đóng gói danh sách học sinh dưới dạng một mảng JSON và trả về cho người dùng
        return jsonify(dsHS)

    @app.route('/api/deleteHS', methods=['POST'])
    def api_deleteHS():
        id = request.form.get('id')
        result = delete_HS(id)
        return jsonify(result)

    @app.route('/api/getHS', methods=['GET'])
    def api_getHS():
        id = request.args.get('id')
        hs = get_HS(id)
        dsLop = onto.LopHoc.instances()
        return render_template("_HS.html", dsLop=dsLop, hs=hs)

    @app.route('/api/newHS', methods=['GET'])
    def api_newHS():
        id, hs = new_HS()
        dsLop = onto.LopHoc.instances()
        return {'id':id, 'html': render_template("_HS.html", dsLop=dsLop, hs=hs)}

    @app.route('/api/saveHS', methods=['POST'])
    def api_saveHS():
        id = request.form.get('id')
        hoTen = request.form.get('hoTen')
        hocLop = request.form.get('hocLop')
        ngaySinh = request.form.get('ngaySinh')
        gioiTinh = request.form.get('gioiTinh')
        hanhKiem = request.form.get('hanhKiem')
        result = save_HS(id, hoTen, hocLop, ngaySinh, gioiTinh, hanhKiem)
        return jsonify(result)
