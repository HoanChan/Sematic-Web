from flask import render_template, request, jsonify
from models import onto, default_world
from models.rulers import apply_DiemSoHS_Rules
try: from hsCtrl import get_HS
except: from .hsCtrl import get_HS
import re

def search_DS(lop, mon):
    print(f'search_DS: lop = {lop}, mon = {mon}')
    query_str = """
    PREFIX s: <http://hc.com/school#>
    SELECT ?ds
    WHERE {
        ?ds a s:DiemSo.
    """
    if mon: query_str += '?ds s:monHoc ?mon.' + f'FILTER(STRENDS(STR(?mon), "#{mon}")).'
    if lop: query_str += '?ds s:hocSinh ?hs. ?hs s:hocLop ?lop.' + f'FILTER(STRENDS(STR(?lop), "#{lop}")).'
    query_str += '}'
    # print(query_str)
    result = default_world.sparql(query_str)
    dsDS = []
    if result:
        dsDS = list(map(lambda ds: {'id': ds[0].name,
                                    'lop':ds[0].hocSinh.hocLop.ten,
                                    'mon':ds[0].monHoc.ten,
                                    'hoTen': ds[0].hocSinh.hoTen,
                                    'ngaySinh': ds[0].hocSinh.ngaySinh, 
                                    'gioiTinh': ds[0].hocSinh.gioiTinh,
                                    'tx1':ds[0].tx1,
                                    'tx2':ds[0].tx2,
                                    'tx3':ds[0].tx3,
                                    'gk':ds[0].gk,
                                    'ck':ds[0].ck,
                                    'diemTB':ds[0].diemTB}, result))
    return dsDS

def save_DS(id, dsDiem):
    print(f'save_DS: id = {id}, dsDiem = {dsDiem}')
    hs = onto.search_one(iri = f'*#{id}', type = onto.HocSinh)
    if hs:
        for diem in hs.diemSo:
            ds = dsDiem[diem.monHoc.name]
            diem.tx1 = ds['tx1']
            diem.tx2 = ds['tx2']
            diem.tx3 = ds['tx3']
            diem.gk = ds['gk']
            diem.ck = ds['ck']
        #     conDiem = (ds['hs1']+ds['hs2']*2 + ds['hs3']*3)
        #     diem.diemTB = round(sum(conDiem)/len(conDiem),2) # Tính điểm trung bình vì chưa có luật để tính tự động
        # # Tính điểm trung bình chung
        # hs.diemTB = round(sum([x.diemTB for x in hs.diemSo])/len(hs.diemSo),2)
        apply_DiemSoHS_Rules(hs) # Áp dụng luật tính điểm và học lực và danh hiệu
        return True
    return False

def initRouteDS(app):        

    @app.route('/api/getDS', methods=['GET'])
    def api_getDS():
        id = request.args.get('id')
        hs = get_HS(id)
        # Lặp qua điểm số từng môn
        ds = []
        for diem in hs.diemSo:
            idMon = diem.monHoc.name
            tenMon = diem.monHoc.ten
            tx1 = diem.tx1
            tx2 = diem.tx2
            tx3 = diem.tx3
            gk = diem.gk
            ck = diem.ck
            diemTB = diem.diemTB
            ds.append({'id': idMon, 'ten': tenMon, 'tx1': tx1, 'tx2': tx2, 'tx3': tx3, 'gk': gk, 'ck': ck, 'diemTB': diemTB})            
        
        return render_template("_DS.html", subjects=ds)
    
    @app.route('/api/saveDS', methods=['POST'])
    def api_saveDS():
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
                    dsDiem[subject][field] = value
                else:
                    if value:
                        dsDiem[subject][field] = float(value)

        result = save_DS(id, dsDiem)
        return jsonify(result)
    
    @app.route("/diemSo/edit")
    def diemSoEdit():
        dsLop = onto.LopHoc.instances()
        dsMon = onto.MonHoc.instances()
        return render_template("diemSo.html", dsLop=dsLop, dsMon=dsMon, edit=True)

    @app.route("/diemSo/search")
    def diemSoSearch():
        dsLop = onto.LopHoc.instances()
        dsMon = onto.MonHoc.instances()
        return render_template("diemSo.html", dsLop=dsLop, dsMon=dsMon, edit=False)
    
    @app.route('/api/dsDS', methods=['GET'])
    def api_dsDS():
        lop = request.args.get('lop')
        mon = request.args.get('mon')
        dsDS = search_DS(lop = lop, mon = mon)
        # Đóng gói danh sách học sinh dưới dạng một mảng JSON và trả về cho người dùng
        return jsonify(dsDS)
