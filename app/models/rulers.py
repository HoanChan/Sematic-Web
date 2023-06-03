from model import *
from owlready2 import *

# HocSinh(?hs) ^ cha(?hs, ?c)  ^ me(?hs, ?m) -> phuHuynh(?hs, ?c) ^ phuHuynh(?hs, ?m) 

for hs in onto.HocSinh.instances():
    hs.phuHuynh.append(hs.cha)
    hs.phuHuynh.append(hs.me)

# HocSinh(?hs) ^ cha(?hs, ?ph1) ^ me(?hs, ?ph2) -> vo(?ph1, ?ph2) ^ chong(?ph2, ?ph1)

for hs in onto.HocSinh.instances():
    hs.cha.vo = hs.me
    hs.me.chong = hs.cha

# HocSinh(?hs1) ^ HocSinh(?hs2) ^ me(?hs1, ?ph1) ^ me(?hs2, ?ph2) ^ differentFrom(?hs1, ?hs2) ^ sameAs(?ph1, ?ph2) ^ ngaySinh(?hs1, ?ns1) ^ ngaySinh(?hs2, ?ns2) ^ greaterThanOrEqual(?ns1, ?ns2) ^ gioiTinh(?hs1, "Nam") -> anh(?hs1, ?hs2) ^ em(?hs2,?hs1)
# HocSinh(?hs1) ^ HocSinh(?hs2) ^ me(?hs1, ?ph1) ^ me(?hs2, ?ph2) ^ differentFrom(?hs1, ?hs2) ^ sameAs(?ph1, ?ph2) ^ ngaySinh(?hs1, ?ns1) ^ ngaySinh(?hs2, ?ns2) ^ greaterThanOrEqual(?ns1, ?ns2) ^ gioiTinh(?hs1, "Nữ") -> chi(?hs1, ?hs2) ^ em(?hs2,?hs1)
for hs1 in onto.HocSinh.instances():
    for hs2 in onto.HocSinh.instances():
        if hs1 != hs2 and hs1.me == hs2.me and hs1.ngaySinh > hs2.ngaySinh:  # Kiểm tra hai học sinh khác nhau + Kiểm tra mẹ của hai học sinh là cùng một người
            if hs1.gioiTinh == "Nam": hs1.anh.append(hs2)
            else: hs1.chi.append(hs2)        
            hs2.em.append(hs1)
# HocSinh(?hs) ^ diemTB(?hs, ?dtb) ^ greaterThanOrEqual(?dtb, 8.0) -> hocLuc(?hs, "Giỏi")
# HocSinh(?hs) ^ diemTB(?hs, ?dtb) ^ greaterThanOrEqual(?dtb, 6.5) ^ lessThan(?dtb, 8.0) -> hocLuc(?hs, "Khá")
# HocSinh(?hs) ^ diemTB(?hs, ?dtb) ^ greaterThanOrEqual(?dtb, 5.0) ^ lessThan(?dtb, 6.5) -> hocLuc(?hs, "Trung bình")
# HocSinh(?hs) ^ diemTB(?hs, ?dtb) ^ lessThan(?dtb, 5.0) -> hocLuc(?hs, "Yếu")
for hs in onto.HocSinh.instances():
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
for hs in onto.HocSinh.instances():
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
# for lh in onto.LopHoc.instances():
#     gv = lh.giaoVienChuNhiem[0]
#     p = lh.phong[0]
#     phong_lam_viec = onto.PhongLamViec()
#     phong_lam_viec.has_teacher.append(gv)
#     phong_lam_viec.has_room.append(p)