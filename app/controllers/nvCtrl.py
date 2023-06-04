from flask import render_template, request, jsonify
from models import onto, default_world, destroy_entity
from utils import toDate
from .mainCtrl import *

def search_NV(hoTen, toChuc, ngaySinh, gioiTinh):
    query_str = """
    PREFIX s: <http://hc.com/school#>
    SELECT ?nv
    WHERE {
        {?nv a s:NhanVien.} UNION {?nv a s:GiaoVien.}
    """
    if hoTen: query_str += '?nv s:hoTen ?hoTen.' + f'FILTER(REGEX(?hoTen, ".*{hoTen}.*","i")).'
    if toChuc: query_str += '?nv s:toChuc ?tc. ' + f'FILTER(STRENDS(STR(?tc), "#{toChuc}")).'
    if ngaySinh: query_str += f'?nv s:ngaySinh "{toDate(ngaySinh)}".'
    if gioiTinh: query_str += f'?nv s:gioiTinh "{gioiTinh}".'
    query_str += '}'
    result = default_world.sparql(query_str)
    dsNV = []
    if result:
        dsNV = list(map(lambda nv: {'id': nv[0].name,
                                    'hoTen': nv[0].hoTen, 
                                    'toChuc': ', '.join([x.ten for x in nv[0].toChuc]), 
                                    'ngaySinh': nv[0].ngaySinh, 
                                    'gioiTinh': nv[0].gioiTinh}, result))
    return dsNV
def delete_NV(id):
    nv = onto.search_one(iri = f'*#{id}', type = onto.NhanVien)
    if nv:
        destroy_entity(nv)
        return True
    return False

def get_NV(id):
    nv = onto.search_one(iri = f'*#{id}', type = onto.NhanVien)
    return nv

def new_NV():
    nv = onto.NhanVien()
    return nv.iri.split('#')[1], nv

def save_NV(id, hoTen, toChuc, ngaySinh, gioiTinh):
    print('save_NV', id, hoTen, toChuc, ngaySinh, gioiTinh)
    nv = onto.search_one(iri = f'*#{id}', type = onto.NhanVien)
    if nv:
        nv.hoTen = hoTen
        nv.toChuc = onto.search_one(iri = f'*#{toChuc}', type = onto.LopHoc)            
        nv.ngaySinh = ngaySinh
        nv.gioiTinh = gioiTinh
        return True
    return False

def initRouteNV(app):        
    @app.route("/nhanVien/edit")
    def nhanVienEdit():
        dsToChuc = get_dsToChuc(includeClass=False)
        dsNV = []
        return render_template("nhanVien.html", dsToChuc=dsToChuc, dsNV=dsNV, edit=True)

    @app.route("/nhanVien/search")
    def nhanVienSearch():
        dsToChuc = get_dsToChuc(includeClass=False)
        dsNV = []
        return render_template("nhanVien.html", dsToChuc=dsToChuc, dsNV=dsNV, edit=False)

    @app.route('/api/dsNV', methods=['GET'])
    def api_dsNV():
        hoTen = request.args.get('hoTen')
        toChuc = request.args.get('toChuc')
        ngaySinh = request.args.get('ngaySinh')
        gioiTinh = request.args.get('gioiTinh')
        dsNV = search_NV(hoTen, toChuc, ngaySinh, gioiTinh)
        # Đóng gói danh sách học sinh dưới dạng một mảng JSON và trả về cho người dùng
        return jsonify(dsNV)

    @app.route('/api/deleteNV', methods=['POST'])
    def api_deleteNV():
        id = request.form.get('id')
        result = delete_NV(id)
        return jsonify(result)

    @app.route('/api/getNV', methods=['GET'])
    def api_getNV():
        id = request.args.get('id')
        nv = get_NV(id)
        dsToChuc = get_dsToChuc(includeClass=False)
        return render_template("_NV.html", dsToChuc=dsToChuc, nv=nv)

    @app.route('/api/newNV', methods=['GET'])
    def api_newNV():
        id, nv = new_NV()
        dsToChuc = get_dsToChuc(includeClass=False)
        return {'id':id, 'html': render_template("_NV.html", dsToChuc=dsToChuc, nv=nv)}

    @app.route('/api/saveNV', methods=['POST'])
    def api_saveNV():
        id = request.form.get('id')
        hoTen = request.form.get('hoTen')
        toChuc = request.form.get('toChuc')
        ngaySinh = request.form.get('ngaySinh')
        gioiTinh = request.form.get('gioiTinh')
        result = save_NV(id, hoTen, toChuc, ngaySinh, gioiTinh)
        return jsonify(result)
