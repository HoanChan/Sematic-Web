from owlready2 import *

# Tạo ontology
# onto = get_ontology("http://hc.com/school")
onto = get_ontology("app/data/education.owl").load()
with onto:
    class ChucVu(Thing): pass
    class ToChuc(Thing): pass
    class Nguoi(Thing): pass
    class NhanVien(Nguoi): pass
    class PhuHuynh(Nguoi): pass
    class LopHoc(ToChuc):
        def __str__(self):
            return ' - '.join([self.ten, getattr(self.giaoVienChuNhiem,'hoTen',''), getattr(self.phongHoc,'ten','')])
    class HocSinh(Nguoi): 
        def __str__(self):
            return ' - '.join([self.hoTen, self.ngaySinh, self.gioiTinh, getattr(self.hocLop,'ten','')])
    class GiaoVien(NhanVien): 
        def __str__(self):
            return ' - '.join([self.hoTen, self.ngaySinh, self.gioiTinh, self.trinhDo, [mon.ten for mon in self.dayMon], getattr(self.lopChuNhiem,'ten','')])
    class MonHoc(Thing): pass
    class DiemSo(Thing): pass
    class TheDocGia(Thing): pass
    class TacGia(Thing): pass
    class NhaXuatBan(Thing): pass
    class Sach(Thing): pass
    class TheLoai(Thing): pass
    class PhieuMuon(Thing): pass
    class Phong(Thing): pass
    class HoatDong(Thing): pass
    class DiemDanh(Thing): pass
    
    # -------- Các thuộc tính của Đối tượng -------- #
    # InverseFunctionalProperty: Giống khoá chính trong SQL, không được trùng
    # FunctionalProperty: chỉ nhận 1 giá trị duy nhất (Không thể có tên)
    class ten(DatatypeProperty, FunctionalProperty):
        domain = [ChucVu, ToChuc, LopHoc, MonHoc, NhaXuatBan, Sach, TheLoai, Phong, HoatDong]
        range = [str]
    class moTa(ObjectProperty, FunctionalProperty): 
        domain = [ChucVu, MonHoc, Phong, TheLoai, HoatDong]
        range = [str]
    # -------- Các thuộc tính của Chức vụ -------- #
    class phuCap(ChucVu >> int, FunctionalProperty): pass
    class toChuc(ChucVu >> ToChuc): pass
    # -------- Các thuộc tính của Tổ chức -------- #
    class thanhVien(ToChuc >> Nguoi): pass
    class phong(ToChuc >> Phong): pass
    # -------- Các thuộc tính của Người -------- #
    class hoTen(Nguoi >> str, FunctionalProperty): pass
    class ngaySinh(Nguoi >> datetime.date, FunctionalProperty): pass
    class gioiTinh(Nguoi >> str, FunctionalProperty): pass
    class thuocToChuc(Nguoi >> ToChuc): 
        inverse_property = thanhVien # Đảo ngược thuộc tính, nếu có 1 người thuộc 1 tổ chức thì tổ chức đó có 1 thành viên là người đó
    # -------- Các thuộc tính của Nhân viên -------- #
    class chucVu(NhanVien >> ChucVu): pass
    class luong(NhanVien >> int, FunctionalProperty): pass
    # -------- Các thuộc tính của Phụ huynh -------- #
    class ngheNghiep(Nguoi >> str, FunctionalProperty): pass
    class con(PhuHuynh >> HocSinh): pass
    # -------- Các thuộc tính của Lớp học -------- #
    class giaoVienChuNhiem(LopHoc >> GiaoVien, FunctionalProperty): pass
    class phongHoc(LopHoc >> Phong, FunctionalProperty): pass
    class dsHocSinh(LopHoc >> HocSinh): pass
    # -------- Các thuộc tính của Học sinh -------- #
    class hocLop(HocSinh >> LopHoc, FunctionalProperty): 
        inverse_property = dsHocSinh
    class phuHuynh(HocSinh >> PhuHuynh): 
        inverse_property = con
    class diemSo(HocSinh >> DiemSo): pass
    # -------- Các thuộc tính của Giáo viên -------- #
    class dayMon(GiaoVien >> MonHoc):pass
    class trinhDo(GiaoVien >> str, FunctionalProperty): pass
    class lopChuNhiem(GiaoVien >> LopHoc, FunctionalProperty): 
        inverse_property = giaoVienChuNhiem
    # -------- Các thuộc tính của Môn học -------- #
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
    # -------- Các thuộc tính của Thẻ Đọc giả -------- #
    class docGia(TheDocGia >> Nguoi, FunctionalProperty): pass
    class ngayCap(TheDocGia >> datetime.date, FunctionalProperty): pass
    class ngayHetHan(TheDocGia >> datetime.date, FunctionalProperty): pass
    class sachDaDoc(TheDocGia >> Sach): pass
    # -------- Các thuộc tính của Tác giả + Nhà xuất bản -------- #
    class dsSach(ObjectProperty): 
        domain = [TacGia, NhaXuatBan, TheLoai]
        range = [Sach]    
    # -------- Các thuộc tính của Sách -------- #
    class tacGia(Sach >> TacGia, FunctionalProperty): pass
    class nhaXuatBan(Sach >> NhaXuatBan, FunctionalProperty): pass
    class theLoai(Sach >> TheLoai): pass
    class giaTien(Sach >> int, FunctionalProperty): pass
    class soLuong(Sach >> int, FunctionalProperty): pass
    # -------- Các thuộc tính của Thể loại -------- #
    
    # -------- Các thuộc tính của Phiếu mượn -------- #
    class theDocGia(PhieuMuon >> TheDocGia, FunctionalProperty): pass
    class ngayMuon(PhieuMuon >> datetime.date, FunctionalProperty): pass
    class ngayTra(PhieuMuon >> datetime.date, FunctionalProperty): pass
    class sachMuon(PhieuMuon >> Sach): pass
    # -------- Các thuộc tính của Phòng -------- #
    class suDungBoi(Phong >> ToChuc): pass
    # -------- Các thuộc tính của Hoạt động -------- #
    class ngayBatDau(HoatDong >> datetime.date, FunctionalProperty): pass
    class ngayKetThuc(HoatDong >> datetime.date, FunctionalProperty): pass
    class quanLy(HoatDong >> Nguoi): pass
    class thamGia(HoatDong >> Nguoi): pass
    # -------- Các thuộc tính của Điểm danh -------- #
    class nguoiDiemDanh(DiemDanh >> Nguoi, FunctionalProperty): pass
    class hoatDong(DiemDanh >> HoatDong, FunctionalProperty): pass
    class ngayGio(DiemDanh >> datetime.datetime, FunctionalProperty): pass
    class trangThai(DiemDanh >> str, FunctionalProperty): pass