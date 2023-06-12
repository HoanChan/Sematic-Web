from flask import render_template, request, jsonify
from models import default_world, onto, destroy_entity

def search_TC(ten, loai):
    print(f'search_TC: ten = {ten}, loai = {loai}')
    query_str = """
    PREFIX s: <http://hc.com/school#>
    SELECT ?tc
    WHERE {
    """    
    if loai == 'LopHoc': query_str += '?tc a s:LopHoc.'
    elif loai == 'ToChuc': query_str += '?tc a s:ToChuc. '
    else: query_str += '{?tc a s:ToChuc.} UNION {?tc a s:LopHoc.}'
    if ten: query_str += '?tc s:ten ?ten.' + f'FILTER(REGEX(?ten, ".*{ten}.*","i")).'
    query_str += '}'
    print(query_str)
    result = default_world.sparql(query_str)
    dsTC = []
    if result:
        dsTC = list(map(lambda tc: {'id': tc[0].name,
                                    'ten': tc[0].ten,
                                    'loai': 'Lớp học' if str(type(tc[0])) == 'school.LopHoc' else 'Tổ chức'}, result))
    return dsTC
def delete_TC(id):
    print(f'delete_TC: id = {id}')
    tc = onto.search_one(iri = f'*#{id}', loai = onto.ToChuc)
    if tc:
        destroy_entity(tc)
        return True
    return False

def get_TC(id):
    print(f'get_TC: id = {id}')
    tc = onto.search_one(iri = f'*#{id}', loai = onto.ToChuc)
    return tc

def new_TC():
    tc = onto.ToChuc()
    return tc.name, tc

def save_TC(id, ten, hocLop, ngaySinh, gioiTinh, hanhKiem):
    print(f'save_TC: id = {id}, ten = {ten}, hocLop = {hocLop}, ngaySinh = {ngaySinh}, gioiTinh = {gioiTinh}, hanhKiem = {hanhKiem}')
    tc = onto.search_one(iri = f'*#{id}', loai = onto.ToChuc)
    if tc:
        tc.ten = ten
        tc.hocLop = onto.search_one(iri = f'*#{hocLop}', loai = onto.LopHoc)            
        tc.ngaySinh = ngaySinh
        tc.gioiTinh = gioiTinh
        tc.hanhKiem = hanhKiem
        return True
    return False

def initRouteTC(app):        
    @app.route("/toChuc/edit")
    def toChucEdit():
        dsTC = [{'name':'ToChuc','ten':'Tổ chức'},{'name':'LopHoc','ten':'Lớp học'}]
        return render_template("toChuc.html", dsTC = dsTC, edit=True)

    @app.route("/toChuc/search")
    def toChucSearch():
        dsTC = [{'name':'ToChuc','ten':'Tổ chức'},{'name':'LopHoc','ten':'Lớp học'}]
        return render_template("toChuc.html", dsTC = dsTC, edit=False)

    @app.route('/api/dsTC', methods=['GET'])
    def api_dsTC():
        ten = request.args.get('ten')
        loai = request.args.get('loai')
        dsTC = search_TC(ten, loai)
        # Đóng gói danh sách học sinh dưới dạng một mảng JSON và trả về cho người dùng
        return jsonify(dsTC)

    @app.route('/api/deleteTC', methods=['POST'])
    def api_deleteTC():
        id = request.form.get('id')
        result = delete_TC(id)
        return jsonify(result)

    @app.route('/api/getTC', methods=['GET'])
    def api_getTC():
        id = request.args.get('id')
        tc = get_TC(id)
        dsLop = onto.LopHoc.instances()
        return render_template("_TC.html", dsLop=dsLop, tc=tc)

    @app.route('/api/newTC', methods=['GET'])
    def api_newTC():
        id, tc = new_TC()
        dsLop = onto.LopHoc.instances()
        return {'id':id, 'html': render_template("_TC.html", dsLop=dsLop, tc=tc)}

    @app.route('/api/saveTC', methods=['POST'])
    def api_saveTC():
        id = request.form.get('id')
        ten = request.form.get('ten')
        hocLop = request.form.get('hocLop')
        ngaySinh = request.form.get('ngaySinh')
        gioiTinh = request.form.get('gioiTinh')
        hanhKiem = request.form.get('hanhKiem')
        result = save_TC(id, ten, hocLop, ngaySinh, gioiTinh, hanhKiem)
        return jsonify(result)
