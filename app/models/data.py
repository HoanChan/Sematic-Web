import random
import datetime 
from model import *
from owlready2 import *

def createDateTime(date_obj:datetime.date, hour=0, minute=0, second=0):
    time_obj = datetime.time(hour, minute, second)
    return datetime.datetime.combine(date_obj, time_obj)

def createRandomDate(start_year, end_year):
    return createRandomFromDate(f'01/01/{start_year}', f'31/12/{end_year}')

def createRandomFromDate(start:str, end:str): #01/01/2022
    start_date = datetime.date(year=int(start[6:]), month=int(start[3:5]), day=int(start[:2]))
    end_date = datetime.date(year=int(end[6:]), month=int(end[3:5]), day=int(end[:2]))
    days_in_range = (end_date - start_date).days + 1
    random_days = random.randint(0, days_in_range - 1)
    birth_date = start_date + datetime.timedelta(days=random_days)
    return  birth_date

def createRandomInfo():
    ho = random.choice(["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Lương", "Mai", "Trương", "Tạ", "Đào", 
                            "Đoàn", "Đinh", "Lâm", "Phùng", "Đoàn", "Bành", "Quách", "Thái", "Tô", "Tôn", "Tăng"])
    lot = random.choice(['Văn', 'Thị', 'Hồng', 'Anh', 'Quý', 'Bảo', "Thanh", "Thu", "Hữu", "Mai", "Đình", "Hoài", "Ngọc", "Minh", "Kim"])
    ten = random.choice(["An", "Bình", "Cường", "Dũng", "Hải", "Hiền", "Hoàng", "Hùng", "Khánh", "Linh", "Long", "Minh", "Nam", "Ngọc", "Nhật", "Phương", "Quân", "Quang", "Quỳnh", 
                            "Sơn", "Thảo", "Thiên", "Thiện", "Thúy", "Thuận", "Tùng", "Tú", "Tường", "Việt", "Vân", "Vinh", "Xuân"])
    gioiTinh = random.choice(["Nam", "Nữ"])
    return f"{ho} {lot} {ten}", gioiTinh
def randScore():
    score = random.randint(0, 10)
    if score != 10:
        score += random.choice([0.3, 0.5, 0.8])
    return score

def getClassName(soLopMoiKhoi, index):
    khoi = index // soLopMoiKhoi
    lop = index % soLopMoiKhoi + 1
    tenLop = f'{khoi+10}{"CBA"[khoi]}'
    if lop < 10:
        return f'{tenLop}0{lop}'
    else:
        return f'{tenLop}{lop}'
    

def create_Data(soLopMoiKhoi = 3, soHSMoiLop = 5, soHSCoAnhEm = 20, soGVMoiMon = 3, soGVDay2Mon = 5, soDocGia = 10, soSach = 15, soTacGia = 5, soNXB = 3):   
    dsLop, dsHS, dsPhong  = [], [], []
    tongSoLop = soLopMoiKhoi * 3
    for i in range(tongSoLop):
        tenLop = getClassName(soLopMoiKhoi, i)
        phong = Phong('Phong' + tenLop, ten = 'Phòng ' + tenLop)
        dsPhong.append(phong)
        lop = LopHoc(tenLop, ten = tenLop, phong = [phong])
        dsLop.append(lop)
        # Tạo ngẫu nhiên HS cho mỗi lớp
        for j in range(soHSMoiLop):
            ten, gt = createRandomInfo()
            hs = HocSinh(hoTen = ten, ngaySinh = createRandomDate(2000, 2000), gioiTinh = gt, hocLop = lop)
            dsHS.append(hs)
            # Tạo ngẫu nhiên 2 PH cho mỗi HS
            for k in range(2):
                ten, gt = createRandomInfo()
                nghe = random.choice(["Nông dân", "Công nhân", "Giáo viên", "Bác sĩ", "Kỹ sư", "Nhân viên văn phòng", "Chủ doanh nghiệp"])
                ph = PhuHuynh(hoTen = ten, ngaySinh = createRandomDate(1970, 1980), gioiTinh = gt, con = [hs], ngheNghiep = nghe)
        
    # Cho một số học sinh có chung phụ huynh
    random_items = random.sample(dsHS, soHSCoAnhEm)
    remaining_items = list(set(dsHS) - set(random_items))
    new_random_items = random.sample(remaining_items, soHSCoAnhEm)
    for hs, i in zip(random_items, range(soHSCoAnhEm)):
        for ph in hs.phuHuynh: destroy_entity(ph)
        hs.phuHuynh = []
        for ph in new_random_items[i].phuHuynh: 
            ph.con.append(hs)
            hs.phuHuynh.append(ph)


    dsGV, dsMonHoc, dsToChuc, dsChucVu = [], [], [], []

    # Tạo chức vụ tổ trưởng, tổ phó
    toTruong = ChucVu('cvToTruong', ten = 'Tổ trưởng', phuCap = 0.2)
    dsChucVu.append(toTruong)
    toPho = ChucVu('cvToPho', ten = 'Tổ phó', phuCap = 0.15)
    dsChucVu.append(toPho)
    giaoVien = ChucVu('cvGiaoVien', ten = 'Giáo viên', phuCap = 0)
    dsChucVu.append(giaoVien)
    # Tạo môn học
    dataMonHoc = [('Toan', 'Toán học', 5), ('NguVan', 'Ngữ văn', 3), ('HoaHoc', 'Hóa học', 3), ('LichSu', 'Lịch sử', 3), ('DiaLy', 'Địa lý', 5), 
                    ('SinhHoc', 'Sinh học', 2), ('TiengAnh', 'Tiếng Anh', 2), ('GDCD', 'GDCD', 3), ('CongNghe', 'Công nghệ', 2), ('TheDuc', 'Thể dục', 2)]
    for id, mon, st in dataMonHoc:
        mon_hoc = MonHoc(id, ten = mon, soTiet = st)
        dsMonHoc.append(mon_hoc)
        phong = Phong('Phong' + id, ten = 'Phòng ' + mon)
        dsPhong.append(phong)
        toChuyenMon = ToChuc('To' + id, ten = 'Tổ '+ mon, phong = [phong]) 
        dsToChuc.append(toChuyenMon)
        # Tạo ngẫu nhiên GV cho mỗi môn
        for j in range(soGVMoiMon):
            ten, gt = createRandomInfo()
            td = ['Đại học', 'Thạc sĩ'][random.randint(0,1)]
            gv = GiaoVien(hoTen = ten, ngaySinh = createRandomDate(1970, 1990), gioiTinh = gt, trinhDo = td, dayMon = [mon_hoc], toChuc = [toChuyenMon], heSoLuong = random.uniform(1, 9))
            if j == 0: gv.chucVu = [toTruong, giaoVien]
            elif j == 1: gv.chucVu = [toPho, giaoVien]   
            else: gv.chucVu = [giaoVien]         
            dsGV.append(gv)
        # Tạo điểm số cho từng HS
        for hs in dsHS:
            diem = DiemSo(hocSinh = hs, monHoc = mon_hoc, 
                            heSo1 = [randScore(),randScore(),randScore()], 
                            heSo2 = [randScore(),randScore()], 
                            heSo3 = [randScore()])
    # Chọn ngẫu nhiên các giáo viên làm tổ trưởng, tổ phó
    # Cho một số GV dạy 2 môn
    gvKhongChucVu = [gv for gv in dsGV if len(gv.chucVu) == 1]
    for gv in random.sample(gvKhongChucVu, soGVDay2Mon):
        monChuaDay = [mon for mon in dsMonHoc if mon not in gv.dayMon]
        mon = random.choice(monChuaDay)
        gv.dayMon.append(mon)
        to = [to for to in dsToChuc if mon.ten in to.ten][0]
        gv.toChuc.append(to)

    tongSoLop = soLopMoiKhoi * 3

    # Gán GVCN cho từng lớp
    dsGVCN = random.sample(dsGV, tongSoLop)
    for i in range(tongSoLop):
        dsGVCN[i].lopChuNhiem = dsLop[i]

    # Phân công giáo viên dạy môn học
    for mon in dsMonHoc:
        dsGVDayMon = [gv for gv in dsGV if mon in gv.dayMon]
        soLopMoiGV = len(dsLop) // len(dsGVDayMon)
        index = 0
        for gv in dsGVDayMon:
            for i in range(soLopMoiGV):
                tenLop = getClassName(soLopMoiKhoi, index)
                lop = [l for l in dsLop if l.ten == tenLop][0]
                gd = GiangDay(giaoVien = gv, monHoc = mon, lopHoc = lop)
                index += 1
        # Phân công giáo viên dạy môn học cho lớp còn lại
        for i in range(index, tongSoLop):
            tenLop = getClassName(soLopMoiKhoi, i)
            lop = [l for l in dsLop if l.ten == tenLop][0]
            gv = random.choice(dsGVDayMon)
            gd = GiangDay(giaoVien = gv, monHoc = mon, lopHoc = lop)


    dsNV = []

    dataNhanVien = [('BGH', 'Ban giám hiệu', 'Hiệu trưởng', 0.7, 1), ('BGH', 'Ban giám hiệu', 'Phó hiệu Trưởng', 0.5, 2), 
                    ('VP', 'Văn phòng', 'Bảo vệ', 0, 3), ('VP', 'Văn phòng', 'Phục vụ', 0, 2), ('VP', 'Văn phòng', 'Văn thư', 0.3, 1), ('VP', 'Văn phòng', 'Thủ quỹ', 0.3, 1), 
                    ('VP', 'Văn phòng', 'Kế toán', 0.5, 1), ('VP', 'Văn phòng', 'Thư viện', 0, 1), ('VP', 'Văn phòng', 'Thiết bị', 0.25, 2)]
    for id, toChuc, chucVu, phuCap, soNV in dataNhanVien:
        # Tạo tổ chức nếu chưa có
        if id not in [tc.name for tc in dsToChuc]:
            tc = ToChuc(id, ten = toChuc)
            dsToChuc.append(tc)
        else:
            tc = [tc for tc in dsToChuc if tc.name == id][0]
        # Tạo chức vụ nếu chưa có
        if chucVu not in [cv.ten for cv in dsChucVu]:
            cv = ChucVu(ten = chucVu, phuCap = phuCap)
            dsChucVu.append(cv)
        else:
            cv = [cv for cv in dsChucVu if cv.toChuc == tc and cv.ten == chucVu][0]
        # Tạo nhân viên
        for i in range(soNV):
            ten, gt = createRandomInfo()
            nv = NhanVien(hoTen = ten, ngaySinh = createRandomDate(1960, 1995), gioiTinh = gt, toChuc = [tc], chucVu = [cv], heSoLuong = random.uniform(1, 9))
            dsNV.append(nv)
            phong = Phong(ten = f'Phòng {cv.ten} {i+1}' if soNV > 1 else f'Phòng {cv.ten}')
            tc.phong.append(phong)
            dsPhong.append(phong)
    
    toTruong = [cv for cv in dsChucVu if cv.ten == 'Tổ trưởng'][0]
    toPho = [cv for cv in dsChucVu if cv.ten == 'Tổ phó'][0]

    # Cho kế toán làm tổ trưởng và văn thư làm tổ phó
    nv = [nv for nv in dsNV if nv.chucVu[0].ten == 'Kế toán'][0]
    nv.chucVu.append(toTruong)
    nv = [nv for nv in dsNV if nv.chucVu[0].ten == 'Văn thư'][0]
    nv.chucVu.append(toPho)

    # Tạo ngẫu nhiên tác giả
    dsTacGia = []
    for i in range(soTacGia):
        tg = TacGia(ten = f'Tác giả {i+1}')
        dsTacGia.append(tg)

    # Tạo ngẫu nhiên NXB
    dsNXB = []
    for i in range(soNXB):
        nxb = NhaXuatBan(ten = f'NXB {i+1}')
        dsNXB.append(nxb)
    # Tạo ngẫu nhiên thể loại sách
    dsTheLoai = []
    dsTenTheLoai = ["SGK", "Sách bài tập", "Tài liệu tham khảo", "Truyện tranh"]
    for theLoai in dsTenTheLoai:
        tl = TheLoai(ten = theLoai)
        dsTheLoai.append(tl)
    # Tạo ngẫu nhiên sách
    dsSach = []
    dsTenMonHoc = [mon.ten for mon in dsMonHoc]
    for i in range(soSach):
        ten = random.choice(dsTenTheLoai) + ' ' + random.choice(dsTenMonHoc)
        sach = Sach(ten = ten, tacGia = random.choice(dsTacGia), nhaXuatBan = random.choice(dsNXB), theLoai = random.choices(dsTheLoai,k=random.randint(1,2)), namXuatBan = random.randint(1920, 2021), giaTien = random.randint(1, 200)*1000)
        dsSach.append(sach)

    # Tạo ngẫu nhiên đọc giả
    dsDocGia = []
    dsMuonSach=[]
    nguoi = random.sample(dsGV+dsHS+dsNV, soDocGia)
    for i in range(soDocGia):
        ten, gt = createRandomInfo()
        docGia = DocGia(docGia = nguoi[i], ngayCap = createRandomDate(2022, 2023), ngayHetHan = createRandomDate(2024, 2025))
        dsDocGia.append(docGia)
        # Tạo ngẫu nhiên mượn sách
        soSachMuon = random.randint(1, 5)
        for j in range(soSachMuon):
            sach = random.choice(dsSach)
            muon = PhieuMuon(docGia = docGia, sachMuon = random.choices(dsSach, k=random.randint(1,3)), ngayMuon = createRandomFromDate('05/09/2021', '31/12/2021'), ngayTra = createRandomFromDate('01/01/2022', '15/05/2022'))
            dsMuonSach.append(muon)


    dsTenHoatDong = ['Học tập', 'Thể thao', 'Văn hóa', 'Nghệ thuật', 'Tình nguyện', 'Khoa học', 'Kỹ năng sống', 'Ngoại khóa']
    dsHoatDong = []
    for ten in dsTenHoatDong:
        hd = HoatDong(ten = ten, ngayBatDau = createRandomFromDate('05/09/2021', '31/12/2021'), ngayKetThuc = createRandomFromDate('01/01/2022', '15/05/2022'),
                    quanLy = random.choices(dsGV, k= random.randint(1, 3)),
                    thamGia = random.choices(dsHS, k= random.randint(2, 10)))
        dsHoatDong.append(hd)


    dsDiemDanh = []
    for hd in dsHoatDong:
        for hs in hd.thamGia:
            diemDanh = DiemDanh(hoatDong = hd, nguoi = hs, ngayGio = createDateTime(hd.ngayBatDau, random.randint(7, 9)), trangThai = random.choice(['Đúng giờ', 'Trễ', 'Vắng']))
            dsDiemDanh.append(diemDanh)