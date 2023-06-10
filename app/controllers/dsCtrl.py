from flask import render_template, request
from models import onto
try: from hsCtrl import get_HS
except: from .hsCtrl import get_HS

def initRouteDS(app):        

    @app.route('/api/getDS', methods=['GET'])
    def api_getDS():
        # dataMonHoc = [['Toan', 'Toán học'], ['NguVan', 'Ngữ văn'], ['HoaHoc', 'Hóa học'], ['LichSu', 'Lịch sử'], ['DiaLy', 'Địa lý'], 
        #             ['SinhHoc', 'Sinh học'], ['TiengAnh', 'Tiếng Anh'], ['GDCD', 'GDCD'], ['CongNghe', 'Công nghệ'], ['TheDuc', 'Thể dục']]
        dataMonHoc = {'Toan': 'Toán học', 'NguVan': 'Ngữ văn', 'HoaHoc': 'Hóa học', 'LichSu': 'Lịch sử', 'DiaLy': 'Địa lý', 
                      'SinhHoc': 'Sinh học', 'TiengAnh': 'Tiếng Anh', 'GDCD': 'GDCD', 'CongNghe': 'Công nghệ', 'TheDuc': 'Thể dục'}
        id = request.args.get('id')
        hs = get_HS(id)
        # Map môn học trong onto theo cấu trúc [mã môn học, tên môn học]
        dsMon = list(map(lambda mon: [mon.name, mon.ten], onto.MonHoc.instances()))
        # Lặp qua điểm số từng môn
        ds = []
        for diem in hs.diemSo:
            idMon = diem.monHoc.name
            tenMon = diem.monHoc.ten
            hs1 = [x for x in diem.heSo1]
            hs2 = [x for x in diem.heSo2]
            hs3 = [x for x in diem.heSo3]
            diemTB = diem.diemTB
            ds.append({'id': idMon, 'ten': tenMon, 'hs1': hs1, 'hs2': hs2, 'hs3': hs3, 'diemTB': diemTB})            
        
        return render_template("_DS.html", subjects=ds)
