from owlready2 import *
try: from model import *
except: from .model import *

def apply_rules(onto):

    # HocSinh(?hs1) ^ HocSinh(?hs2) ^ me(?hs1, ?ph1) ^ me(?hs2, ?ph2) ^ differentFrom(?hs1, ?hs2) ^ sameAs(?ph1, ?ph2) ^ ngaySinh(?hs1, ?ns1) ^ ngaySinh(?hs2, ?ns2) ^ greaterThanOrEqual(?ns1, ?ns2) ^ gioiTinh(?hs1, "Nam") -> anh(?hs1, ?hs2) ^ em(?hs2,?hs1)
    # HocSinh(?hs1) ^ HocSinh(?hs2) ^ me(?hs1, ?ph1) ^ me(?hs2, ?ph2) ^ differentFrom(?hs1, ?hs2) ^ sameAs(?ph1, ?ph2) ^ ngaySinh(?hs1, ?ns1) ^ ngaySinh(?hs2, ?ns2) ^ greaterThanOrEqual(?ns1, ?ns2) ^ gioiTinh(?hs1, "Nữ") -> chi(?hs1, ?hs2) ^ em(?hs2,?hs1)
    for hs1 in onto.HocSinh.instances():
        for hs2 in onto.HocSinh.instances():
            if hs1 != hs2 and hs1.me == hs2.me and hs1.ngaySinh > hs2.ngaySinh:  # Kiểm tra hai học sinh khác nhau + Kiểm tra mẹ của hai học sinh là cùng một người
                if hs1.gioiTinh == "Nam" and hs2 not in hs1.anh: hs1.anh.append(hs2)
                elif hs1.gioiTinh == "Nữ" and hs2 not in hs1.chi: hs1.chi.append(hs2)        
                if hs1 not in hs2.em: hs2.em.append(hs1)

    # Cập nhật thông tin HS
    for hs in onto.HocSinh.instances():        
        # HocSinh(?hs) ^ cha(?hs, ?c)  ^ me(?hs, ?m) -> phuHuynh(?hs, ?c) ^ phuHuynh(?hs, ?m) 
        # HocSinh(?hs) ^ cha(?hs, ?ph1) ^ me(?hs, ?ph2) -> vo(?ph1, ?ph2) ^ chong(?ph2, ?ph1)

        hs.phuHuynh= [hs.cha, hs.me]
        hs.cha.vo = hs.me
        hs.me.chong = hs.cha

        # Tính điểm số cho từng HS
        for diem in hs.diemSo:
            diemTB = round((sum(diem.heSo1) + sum(diem.heSo2)*2 + sum(diem.heSo3)*3) / (len(diem.heSo1) + len(diem.heSo2)*2 + len(diem.heSo3)*3),2)
            diem.diemTB = diemTB
        hs.diemTB = round(sum(d.diemTB for d in hs.diemSo) / len(hs.diemSo),2)

        # HocSinh(?hs) ^ diemTB(?hs, ?dtb) ^ greaterThanOrEqual(?dtb, 8.0) -> hocLuc(?hs, "Giỏi")
        # HocSinh(?hs) ^ diemTB(?hs, ?dtb) ^ greaterThanOrEqual(?dtb, 6.5) ^ lessThan(?dtb, 8.0) -> hocLuc(?hs, "Khá")
        # HocSinh(?hs) ^ diemTB(?hs, ?dtb) ^ greaterThanOrEqual(?dtb, 5.0) ^ lessThan(?dtb, 6.5) -> hocLuc(?hs, "Trung bình")
        # HocSinh(?hs) ^ diemTB(?hs, ?dtb) ^ lessThan(?dtb, 5.0) -> hocLuc(?hs, "Yếu")
    
        dtb = hs.diemTB    
        if dtb >= 8.0: 
            hs.hocLuc = "Giỏi"
        elif dtb >= 6.5 and dtb < 8.0:
            hs.hocLuc = "Khá"
        elif dtb >= 5.0 and dtb < 6.5:
            hs.hocLuc = "Trung bình"
        elif dtb < 5.0:
            hs.hocLuc = "Yếu"
        # HocSinh(?hs) ^ hocLuc(?hs, ?hl) ^ hanhKiem(?hs, ?hk) ^ equal(?hl, "Giỏi") ^ equal(?hk, "Tốt")-> danhHieu(?hs, "Học sinh giỏi")
        # HocSinh(?hs) ^ hocLuc(?hs, ?hl) ^ hanhKiem(?hs, ?hk) ^ equal(?hl, "Giỏi") ^ equal(?hk, "Khá")-> danhHieu(?hs, "Học sinh giỏi")
        # HocSinh(?hs) ^ hocLuc(?hs, ?hl) ^ hanhKiem(?hs, ?hk) ^ equal(?hl, "Khá") ^ equal(?hk, "Tốt") -> danhHieu(?hs, "Học sinh tiên tiến")
        # HocSinh(?hs) ^ hocLuc(?hs, ?hl) ^ hanhKiem(?hs, ?hk) ^ equal(?hl, "Khá") ^ equal(?hk, "Khá") -> danhHieu(?hs, "Học sinh tiên tiến")
    
        hl = hs.hocLuc
        hk = hs.hanhKiem
        
        if hl == "Giỏi" and (hk == "Tốt" or hk == "Khá"):
            hs.danhHieu = "Học sinh giỏi"
        elif hl == "Khá" and (hk == "Tốt" or hk == "Khá"):
            hs.danhHieu = "Học sinh tiên tiến"

    # # GiaoVien(?gv) ^ chucVu(?gv, ?dscv) ^ ChucVu(?cv) ^ endsWith(?cv,"cvToTruong") ^ member(?cv,?dscv) ^ toChuc(?gv,?tc) ^ phong(?tc,?p) -> phongLamViec(?gv, ?p)
    # for gv in onto.GiaoVien.instances():
    #     dscv = gv.chucVu
    #     for cv in onto.ChucVu.instances():
    #         if cv.endswith("cvToTruong") and cv in dscv:
    #             for tc in gv.toChuc:
    #                 p = tc.phong[0]
    #                 phong_lam_viec = onto.PhongLamViec()
    #                 phong_lam_viec.has_teacher.append(gv)
    #                 phong_lam_viec.has_room.append(p)
    # # LopHoc(?lh) ^ giaoVienChuNhiem(?lh,?gv) ^ phong(?lh,?p) -> phongLamViec(?gv, ?p)
    for lh in onto.LopHoc.instances():
        gv = lh.giaoVienChuNhiem
        p = lh.phong
        gv.phongLamViec=p

isPalletRunning = False
def startSyncPellet(onto):
    global isPalletRunning
    if isPalletRunning: return
    with onto:
        sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)
        isPalletRunning = True

def checkHermitRulers(onto):
    # Remove SWRL rules using built-in atoms
    for rule in onto.get_swrl_rules():
        if any(isinstance(atom, SWRLBuiltInAtom) for atom in rule.body) or any(isinstance(atom, SWRLBuiltInAtom) for atom in rule.head):
            print("Removing rule:", rule)
            onto.remove(rule)
            
isHermitRunning = False
def startSyncHermiT(onto):
    # checkHermitRulers(onto)
    global isHermitRunning
    if isHermitRunning: return
    with onto:
        sync_reasoner(debug=True, infer_property_values = True)
        isHermitRunning = True
    
def stopSyncPellet(onto):
    global isPalletRunning
    if not isPalletRunning: return
    with onto:
        sync_reasoner_pellet.stop()
        isPalletRunning = False

def stopSyncHermiT(onto):
    global isHermitRunning
    if not isHermitRunning: return
    with onto:
        sync_reasoner.stop()
        isHermitRunning = False
