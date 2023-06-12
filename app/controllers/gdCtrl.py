from flask import render_template, request, jsonify
from models import onto, default_world
try: from hsCtrl import get_HS
except: from .hsCtrl import get_HS
import re

def search_GD(lop, mon):
    print(f'search_GD: lop = {lop}, mon = {mon}')
    query_str = """
    PREFIX s: <http://hc.com/school#>
    SELECT ?gd
    WHERE {
        ?gd a s:GiangDay.
    """
    if mon: query_str += '?gd s:monHoc ?mon.' + f'FILTER(STRENDS(STR(?mon), "#{mon}")).'
    if lop: query_str += '?gd s:lopHoc ?lop.' + f'FILTER(STRENDS(STR(?lop), "#{lop}")).'
    query_str += '}'
    print(query_str)
    result = default_world.sparql(query_str)
    dsGD = []
    if result:
        dsGD = list(map(lambda gd: {'id': gd[0].name,
                                    'lopHoc': gd[0].lopHoc.ten,
                                    'monHoc': gd[0].monHoc.ten, 
                                    'gvID': gd[0].giaoVien.name,
                                    'dsGV': [{'id':gv.name, 'ten':gv.hoTen} for gv in onto.GiaoVien.instances() if gd[0].monHoc in gv.dayMon]}, result))
    return dsGD

def save_GD(id, dsDiem):
    print(f'save_GD: id = {id}, dsDiem = {dsDiem}')
    hs = onto.search_one(iri = f'*#{id}', type = onto.HocSinh)
    if hs:
        for diem in hs.giangDay:
            gd = dsDiem[diem.monHoc.name]
            diem.heSo1 = gd['hs1']
            diem.heSo2 = gd['hs2']
            diem.heSo3 = gd['hs3']
        return True
    return False

def initRouteGD(app):        

    @app.route('/api/getGD', methods=['GET'])
    def api_getGD():
        id = request.args.get('id')
        hs = get_HS(id)
        # Lặp qua điểm số từng môn
        gd = []
        for diem in hs.giangDay:
            idMon = diem.monHoc.name
            tenMon = diem.monHoc.ten
            hs1 = [x for x in diem.heSo1]
            hs2 = [x for x in diem.heSo2]
            hs3 = [x for x in diem.heSo3]
            diemTB = diem.diemTB
            gd.append({'id': idMon, 'ten': tenMon, 'hs1': hs1, 'hs2': hs2, 'hs3': hs3, 'diemTB': diemTB})            
        
        return render_template("_GD.html", subjects=gd)
    
    @app.route('/api/saveGD', methods=['POST'])
    def api_saveGD():
        id = request.form.get('id')
        # dsDiem = request.form.get('dsDiem') # Không chịu chạy = None luôn
        dsDiem = {}
        strRQ = str(request.form)
        # print(f'strRQ = {strRQ}')
        for match in re.finditer(r"\('([^']*)', '([^']*)'\)", strRQ):
            key, value = match.group(1), match.group(2)
            if key.startswith("dsDiem["):
                # Tách tên môn học và trường dữ liệu
                match = re.match(r'dsDiem\[(\w+)\]\[(\w+)\]', key)
                subject = match.group(1)
                field = match.group(2)
                # Tạo mục mới trong dsDiem nếu cần
                if subject not in dsDiem:
                    dsDiem[subject] = {}
                if field not in dsDiem[subject]:
                    dsDiem[subject][field] = []
                # Thêm giá trị vào dsDiem
                if field == 'id':
                    dsDiem[subject][field] += [value]
                else:
                    if value:
                        dsDiem[subject][field].append(float(value))

        result = save_GD(id, dsDiem)
        return jsonify(result)
    
    @app.route("/giangDay/edit")
    def giangDayEdit():
        dsLop = onto.LopHoc.instances()
        dsMon = onto.MonHoc.instances()
        return render_template("giangDay.html", dsLop=dsLop, dsMon=dsMon, edit=True)

    @app.route("/giangDay/search")
    def giangDaySearch():
        dsLop = onto.LopHoc.instances()
        dsMon = onto.MonHoc.instances()
        return render_template("giangDay.html", dsLop=dsLop, dsMon=dsMon, edit=False)
    
    @app.route('/api/dsGD', methods=['GET'])
    def api_dsGD():
        lop = request.args.get('lop')
        mon = request.args.get('mon')
        dsGD = search_GD(lop = lop, mon = mon)
        # Đóng gói danh sách học sinh dưới dạng một mảng JSON và trả về cho người dùng
        return jsonify(dsGD)
