from owlready2 import *
"""
Thiết lập các tập luật cho CSDL
    1.  Số lượng phụ huynh tối đa của một HS là 2
    2.  Phụ huynh có giới tính là nữ thì là mẹ
    3.  Phụ huynh có giới tính là nam thì là cha
    4.  Tính điểm trung bình của học sinh
    5.  Xếp loại học lực theo điểm trung bình
    6.  Học sinh có chung cha mẹ thì là anh em
    7.  Phụ huynh có chung con là vợ chồng
    8.  Giáo viên chỉ có thể nhập điểm môn mình dạy
    9.  Một lớp không được học 2 môn trùng tên
    10. Một lần không được mượn quá 5 cuốn sách
"""
def addRule(onto: Ontology, rule:str):
    with onto:
        rule = Imp()
        rule.set_as_rule(rule)
        # onto.rule.append(rule)
def addSWRLs(onto: Ontology):
    addRule(onto, ''' HocSinh(?hs) ^ count(?ph) > 2 -> false
                        PhuHuynh(?ph) ^ con(?ph, ?hs) ''')
    addRule(onto, ''' PhuHuynh(?ph) ^ gioiTinh(?ph, "Nữ") -> Me(?ph)
                        PhuHuynh(?ph) ^ gioiTinh(?ph, "Nam") -> Cha(?ph) ''')
    addRule(onto, ''' PhuHuynh(?ph1) ^ PhuHuynh(?ph2) ^ HocSinh(?hs) ^ con(?ph1, ?hs) ^ con(?ph2, ?hs) ^ differentFrom(?ph1, ?ph2) -> VoChong(?ph1, ?ph2) ''')
    addRule(onto, ''' Lop(?lop) ^ MonHoc(?mh1) ^ MonHoc(?mh2) ^ differentFrom(?mh1, ?mh2) ^ hoc(?lop, ?mh1) ^ hoc(?lop, ?mh2) -> false ''')
    addRule(onto, ''' HocSinh(?hs1) ∧ HocSinh(?hs2) ∧ PhuHuynh(?ph) ∧ con(?ph, ?hs1) ∧ con(?ph, ?hs2) ∧ differentFrom(?hs1, ?hs2) → AnhEm(?hs1, ?hs2) ''')