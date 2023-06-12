from owlready2 import *

# Tạo ontology
onto = get_ontology("http://hc.com/school")
with onto:
    class ChucVu(Thing): pass
    class ToChuc(Thing): pass
    class Nguoi(Thing): pass
    class NhanVien(Nguoi): pass
    class PhuHuynh(Nguoi): pass
    class Cha(PhuHuynh): pass
    class Me(PhuHuynh): pass
    class LopHoc(ToChuc): pass
    class HocSinh(Nguoi): pass
    class Anh(HocSinh): pass
    class Chi(HocSinh): pass
    class Em(HocSinh): pass
    class GiaoVien(NhanVien): pass
    class MonHoc(Thing): pass
    class DiemSo(Thing): pass
    class GiangDay(Thing): pass
    class Phong(Thing): pass
    class HoatDong(Thing): pass
    class DiemDanh(Thing): pass
    class ThietBi(Thing): pass
    
    # -------- Các thuộc tính của Đối tượng -------- #
    # InverseFunctionalProperty: Giống khoá chính trong SQL, không được trùng
    # FunctionalProperty: chỉ nhận 1 giá trị duy nhất (Không thể có tên)
    # -------- Các thuộc tính của Chức vụ -------- #
    class ten(ChucVu >> str, FunctionalProperty): pass
    class phuCap(ChucVu >> float, FunctionalProperty): pass
    # -------- Các thuộc tính của Tổ chức -------- #
    class ten(ToChuc >> str, FunctionalProperty): pass
    class thanhVien(ToChuc >> Nguoi): pass
    class phong(ToChuc >> Phong): pass
    # -------- Các thuộc tính của Người -------- #
    class hoTen(Nguoi >> str, FunctionalProperty): pass
    class ngaySinh(Nguoi >> datetime.date, FunctionalProperty): pass
    class gioiTinh(Nguoi >> str, FunctionalProperty): pass
    class toChuc(Nguoi >> ToChuc): 
        inverse_property = thanhVien # Đảo ngược thuộc tính, nếu có 1 người thuộc 1 tổ chức thì tổ chức đó có 1 thành viên là người đó
    # -------- Các thuộc tính của Nhân viên -------- #
    class chucVu(NhanVien >> ChucVu): pass
    class heSoLuong(NhanVien >> float, FunctionalProperty): pass
    # -------- Các thuộc tính của Phụ huynh -------- #
    class ngheNghiep(PhuHuynh >> str, FunctionalProperty): pass
    class con(PhuHuynh >> HocSinh): pass
    # -------- Các thuộc tính của Lớp học -------- #
    class giaoVienChuNhiem(LopHoc >> GiaoVien, FunctionalProperty): pass
    class dsHocSinh(LopHoc >> HocSinh): pass
    # -------- Các thuộc tính của Học sinh -------- #
    class hocLop(HocSinh >> LopHoc, FunctionalProperty): inverse_property = dsHocSinh
    class phuHuynh(HocSinh >> PhuHuynh): inverse_property = con
    class me(HocSinh >> Me, FunctionalProperty): is_a = [phuHuynh]        
    class cha(HocSinh >> Cha, FunctionalProperty): is_a = [phuHuynh]        
    class diemSo(HocSinh >> DiemSo): pass
    class diemTB(HocSinh >> float, FunctionalProperty): pass # Đáng lý phải được suy ra từ tập luật nhưng không viết được
    class hanhKiem(HocSinh >> str, FunctionalProperty): pass
    # -------- Các thuộc tính của Giáo viên -------- #
    class dayMon(GiaoVien >> MonHoc):pass
    class trinhDo(GiaoVien >> str, FunctionalProperty): pass
    class giangDay(GiaoVien >> GiangDay): pass
    class lopChuNhiem(GiaoVien >> LopHoc, FunctionalProperty): 
        inverse_property = giaoVienChuNhiem
    # -------- Các thuộc tính của Môn học -------- #    
    class ten(MonHoc >> str, FunctionalProperty): pass
    class giaoVienDay(MonHoc >> GiaoVien):
        inverse_property = dayMon
    class soTiet(MonHoc >> int, FunctionalProperty): pass
    # -------- Các thuộc tính của Điểm -------- #
    class hocSinh(DiemSo >> HocSinh, FunctionalProperty): 
        inverse_property = diemSo
    class monHoc(DiemSo >> MonHoc, FunctionalProperty): pass
    class heSo1(DiemSo >> float): pass
    class heSo2(DiemSo >> float): pass
    class heSo3(DiemSo >> float): pass
    class diemTB(DiemSo >> float, FunctionalProperty): pass # Đáng lý phải được suy ra từ tập luật nhưng không viết được
    # -------- Các thuộc tính của Giảng dạy -------- #
    class giaoVien(GiangDay >> GiaoVien, FunctionalProperty): inverse_property = giangDay
    class lopHoc(GiangDay >> LopHoc, FunctionalProperty): pass
    class monHoc(GiangDay >> MonHoc, FunctionalProperty): pass
    # -------- Các thuộc tính của Phòng -------- #
    class ten(Phong >> str, FunctionalProperty): pass
    class suDungBoi(Phong >> ToChuc): inverse_property = phong
    # -------- Các thuộc tính của Hoạt động -------- #
    class ten(HoatDong >> str, FunctionalProperty): pass
    class ngayBatDau(HoatDong >> datetime.date, FunctionalProperty): pass
    class ngayKetThuc(HoatDong >> datetime.date, FunctionalProperty): pass
    class quanLy(HoatDong >> Nguoi): pass
    class thamGia(HoatDong >> Nguoi): pass
    # -------- Các thuộc tính của Điểm danh -------- #
    class nguoi(DiemDanh >> Nguoi, FunctionalProperty): pass
    class hoatDong(DiemDanh >> HoatDong, FunctionalProperty): pass
    class ngayGio(DiemDanh >> datetime.datetime, FunctionalProperty): pass
    class trangThai(DiemDanh >> str, FunctionalProperty): pass
    # -------- Các thuộc tính của Thiết bị -------- #
    class ten(ThietBi >> str, FunctionalProperty): pass
    class soLuong(ThietBi >> int, FunctionalProperty): pass
    class phong(ThietBi >> Phong, FunctionalProperty): pass
    # -------- Các thuộc tính của Sử dụng cho Ruler - Không nhập dữ liệu mà dựa vào tập luật để sinh ra -------- #
    class anhChiEm(HocSinh >> HocSinh): pass
    class anh(HocSinh >> Anh): is_a = [anhChiEm] 
    class chi(HocSinh >> Chi): is_a = [anhChiEm] 
    class em(HocSinh >> Em): is_a = [anhChiEm] 
    class vo(Cha >> Me, FunctionalProperty): pass
    class chong(Me >> Cha, FunctionalProperty): pass
    class hocLuc(HocSinh >> str, FunctionalProperty): pass
    class danhHieu(HocSinh >> str, FunctionalProperty): pass
    class phongLamViec(NhanVien >> Phong): pass
    # -------- Các tập luật -------- # # https://www.w3.org/Submission/SWRL/
    rule = Imp()
    rule.set_as_rule(''' HocSinh(?hs) ^ cha(?hs, ?c)  ^ me(?hs, ?m) -> phuHuynh(?hs, ?c) ^ phuHuynh(?hs, ?m)  ''')
    rule = Imp()
    rule.set_as_rule(''' HocSinh(?hs) ^ cha(?hs, ?ph1) ^ me(?hs, ?ph2) -> vo(?ph1, ?ph2) ^ chong(?ph2, ?ph1) ''')
    # rule = Imp()
    # rule.set_as_rule(''' HocSinh(?hs1) ^ HocSinh(?hs2) ^ me(?hs1, ?ph1) ^ me(?hs2, ?ph2) ^ differentFrom(?hs1, ?hs2) ^ sameAs(?ph1, ?ph2) ^ ngaySinh(?hs1, ?ns1) ^ ngaySinh(?hs2, ?ns2) ^ greaterThanOrEqual(?ns1, ?ns2) ^ gioiTinh(?hs1, "Nam") -> anh(?hs1, ?hs2) ^ em(?hs2,?hs1) ''')
    # rule = Imp()
    # rule.set_as_rule(''' HocSinh(?hs1) ^ HocSinh(?hs2) ^ me(?hs1, ?ph1) ^ me(?hs2, ?ph2) ^ differentFrom(?hs1, ?hs2) ^ sameAs(?ph1, ?ph2) ^ ngaySinh(?hs1, ?ns1) ^ ngaySinh(?hs2, ?ns2) ^ greaterThanOrEqual(?ns1, ?ns2) ^ gioiTinh(?hs1, "Nữ") -> chi(?hs1, ?hs2) ^ em(?hs2,?hs1) ''')
    rule = Imp()
    rule.set_as_rule(''' HocSinh(?hs) ^ diemTB(?hs, ?dtb) ^ greaterThanOrEqual(?dtb, 8.0) -> hocLuc(?hs, "Giỏi") ''')
    rule = Imp()
    rule.set_as_rule(''' HocSinh(?hs) ^ diemTB(?hs, ?dtb) ^ greaterThanOrEqual(?dtb, 6.5) ^ lessThan(?dtb, 8.0) -> hocLuc(?hs, "Khá") ''')
    rule = Imp()
    rule.set_as_rule(''' HocSinh(?hs) ^ diemTB(?hs, ?dtb) ^ greaterThanOrEqual(?dtb, 5.0) ^ lessThan(?dtb, 6.5) -> hocLuc(?hs, "Trung bình") ''')
    rule = Imp()
    rule.set_as_rule(''' HocSinh(?hs) ^ diemTB(?hs, ?dtb) ^ lessThan(?dtb, 5.0) -> hocLuc(?hs, "Yếu") ''')
    # rule = Imp()
    # rule.set_as_rule(''' HocSinh(?hs) ^ hocLuc(?hs, ?hl) ^ hanhKiem(?hs, ?hk) ^ equal(?hl, "Giỏi") ^ equal(?hk, "Tốt")-> danhHieu(?hs, "Học sinh giỏi") ''')
    # rule = Imp()
    # rule.set_as_rule(''' HocSinh(?hs) ^ hocLuc(?hs, ?hl) ^ hanhKiem(?hs, ?hk) ^ equal(?hl, "Giỏi") ^ equal(?hk, "Khá")-> danhHieu(?hs, "Học sinh giỏi") ''')
    rule = Imp()
    rule.set_as_rule(''' HocSinh(?hs) ^ hocLuc(?hs, ?hl) ^ hanhKiem(?hs, ?hk) ^ startsWith(?hl, "Gi") ^ endsWith(?hk, "t")-> danhHieu(?hs, "Học sinh giỏi") ''')
    rule = Imp()
    rule.set_as_rule(''' HocSinh(?hs) ^ hocLuc(?hs, ?hl) ^ hanhKiem(?hs, ?hk) ^ startsWith(?hl, "Gi") ^ startsWith(?hk, "Kh")-> danhHieu(?hs, "Học sinh giỏi") ''')
    # rule = Imp()
    # rule.set_as_rule(''' HocSinh(?hs) ^ hocLuc(?hs, ?hl) ^ hanhKiem(?hs, ?hk) ^ equal(?hl, "Khá") ^ equal(?hk, "Tốt") -> danhHieu(?hs, "Học sinh tiên tiến") ''')
    # rule = Imp()
    # rule.set_as_rule(''' HocSinh(?hs) ^ hocLuc(?hs, ?hl) ^ hanhKiem(?hs, ?hk) ^ equal(?hl, "Khá") ^ equal(?hk, "Khá") -> danhHieu(?hs, "Học sinh tiên tiến") ''')
    rule = Imp()
    rule.set_as_rule(''' HocSinh(?hs) ^ hocLuc(?hs, ?hl) ^ hanhKiem(?hs, ?hk) ^ startsWith(?hl, "Kh") ^ endsWith(?hk, "t") -> danhHieu(?hs, "Học sinh tiên tiến") ''')
    rule = Imp()
    rule.set_as_rule(''' HocSinh(?hs) ^ hocLuc(?hs, ?hl) ^ hanhKiem(?hs, ?hk) ^ startsWith(?hl, "Kh") ^ startsWith(?hk, "Kh") -> danhHieu(?hs, "Học sinh tiên tiến") ''')

    # rule = Imp()
    # rule.set_as_rule(''' HocSinh(?hs1) ^ HocSinh(?hs2) ^ me(?hs1, ?ph1) ^ me(?hs2, ?ph2) ^ differentFrom(?hs1, ?hs2) ^ sameAs(?ph1, ?ph2) -> anh(?hs1, ?hs2) ''')
    # rule = Imp()
    # rule.set_as_rule(''' HocSinh(?hs) ^ diemSo(?hs, ?ds) ^ heSo1(?ds, ?hs1) ^ heSo2(?ds, ?hs2) ^ heSo3(?ds, ?hs3) ^ listConcat(?list, ?hs1, ?hs2, ?hs2, ?hs3, ?hs3, ?hs3) ^ length(?list, ?len) ^ add(?tong, ?list) ^ divide(?dtb, ?tong, ?len) ^ round(?kq, ?dtb, 2) -> diemTB(?hs, ?kq)''')

    # Giáo viên làm tổ trưởng của tổ nào thì có phòng làm việc là phòng của tổ đó
    # rule = Imp()
    # rule.set_as_rule(''' GiaoVien(?gv) ^ chucVu(?gv, ?dscv) ^ ChucVu(?cv) ^ endsWith(?cv,"cvToTruong") ^ member(?cv,?dscv) ^ toChuc(?gv,?tc) ^ phong(?tc,?p) -> phongLamViec(?gv, ?p) ''')
    # Giáo viên chủ nhiệm lớp nào thì có phòng làm việc là lớp đó
    # rule = Imp()
    # rule.set_as_rule(''' LopHoc(?lh) ^ giaoVienChuNhiem(?lh,?gv) ^ phong(?lh,?p) -> phongLamViec(?gv, ?p) ''')
    ####### Các hàm hỗ trợ: #######
#     _BUILTINS = { "equal", "notEqual", "lessThan", "lessThanOrEqual", "greaterThan", "greaterThanOrEqual",
#               "add", "subtract", "multiply", "divide", "integerDivide", "mod", "pow", "unaryPlus", "unaryMinus",
#               "abs", "ceiling", "floor", "round", "roundHalfToEven", "sin", "cos", "tan",
#               "booleanNot", "stringEqualIgnoreCase", "stringConcat", "substring", "stringLength",
#               "normalizeSpace", "upperCase", "lowerCase", "translate", "contains", "containsIgnoreCase",
#               "startsWith", "endsWith", "substringBefore", "substringAfter", "matches", "replace", "tokenize",
#               "yearMonthDuration", "dayTimeDuration", "dateTime", "date", "time", "addYearMonthDurations",
#               "subtractYearMonthDurations", "multiplyYearMonthDuration", "divideYearMonthDurations",
#               "addDayTimeDurations", "subtractDayTimeDurations", "multiplyDayTimeDurations",
#               "divideDayTimeDuration", "subtractDates", "subtractTimes", "addYearMonthDurationToDateTime",
#               "addDayTimeDurationToDateTime", "subtractYearMonthDurationFromDateTime",
#               "subtractDayTimeDurationFromDateTime", "addYearMonthDurationToDate", "addDayTimeDurationToDate",
#               "subtractYearMonthDurationFromDate", "subtractDayTimeDurationFromDate", "addDayTimeDurationToTime",
#               "subtractDayTimeDurationFromTime", "subtractDateTimesYieldingYearMonthDuration",
#               "subtractDateTimesYieldingDayTimeDuration", "resolveURI", "anyURI",
#               "listConcat", "listIntersection", "listSubtraction", "member", "length", "first", "rest", "sublist",
#               "empty",
# }