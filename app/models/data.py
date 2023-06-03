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

def createRandomJob():
    return random.choice(["Nông dân", "Công nhân", "Giáo viên", "Bác sĩ", "Kỹ sư", "Nhân viên văn phòng", "Chủ doanh nghiệp"])

def createRandomInfo():
    ho = random.choice(["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Lương", "Mai", "Trương", "Tạ", "Đào", 
                            "Đoàn", "Đinh", "Lâm", "Phùng", "Đoàn", "Bành", "Quách", "Thái", "Tô", "Tôn", "Tăng"])
    nam_lot =  random.choice(['Văn', 'Bảo', 'Anh', 'Quý', 'Hữu', 'Đình', 'Minh', 'Quốc'])
    nu_lot =  random.choice(['Thị', 'Hồng', 'Thanh', 'Thu', 'Mai', 'Hoài', 'Ngọc', 'Kim'])
    ten = random.choice(["An", "Bình", "Cường", "Dũng", "Hải", "Hiền", "Hoàng", "Hùng", "Khánh", "Linh", "Long", "Minh", "Nam", "Ngọc", "Nhật", "Phương", "Quân", "Quang", "Quỳnh", 
                            "Sơn", "Thảo", "Thiên", "Thiện", "Thúy", "Thuận", "Tùng", "Tú", "Tường", "Việt", "Vân", "Vinh", "Xuân"])
    gioiTinh = random.choice(["Nam", "Nữ"])
    lot = nam_lot if gioiTinh == "Nam" else nu_lot
    return f"{ho} {lot} {ten}", gioiTinh

def randScore(diemTB):
    score = round(random.gauss(diemTB, 2.5), 0)
    if score < 0: score = 0
    if score > 10: score = 10
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
    

def create_Data(soLopMoiKhoi = 3, soHSMoiLop = 5, soHSCoAnhEm = 20, soGVMoiMon = 3, soGVDay2Mon = 5):   
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
            ten, gt = createRandomInfo()
            hs.cha = Cha(hoTen = ten, ngaySinh = createRandomDate(1970, 1980), gioiTinh = "Nam", ngheNghiep = createRandomJob())
            ten, gt = createRandomInfo()
            hs.me = Me(hoTen = ten, ngaySinh = createRandomDate(1970, 1980), gioiTinh = "Nữ",  ngheNghiep = createRandomJob())
        
    # Cho một số học sinh có chung phụ huynh
    random_items = random.sample(dsHS, soHSCoAnhEm)
    remaining_items = list(set(dsHS) - set(random_items))
    new_random_items = random.sample(remaining_items, soHSCoAnhEm)
    for hs1, hs2 in zip(random_items, new_random_items):
        destroy_entity(hs1.cha)
        destroy_entity(hs1.me)
        hs1.cha = hs2.cha
        hs1.me = hs2.me

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
            gv = GiaoVien(hoTen = ten, ngaySinh = createRandomDate(1970, 1990), gioiTinh = gt, trinhDo = td, dayMon = [mon_hoc], toChuc = [toChuyenMon], heSoLuong = round(random.uniform(1, 9),1))
            if j == 0: gv.chucVu = [toTruong, giaoVien]
            elif j == 1: gv.chucVu = [toPho, giaoVien]   
            else: gv.chucVu = [giaoVien]         
            dsGV.append(gv)

    # Tính điểm trung bình tất cả các môn của từng HS
    for hs in dsHS:
        # Tạo điểm số cho từng HS
        tb = random.randint(3, 10)
        for mon_hoc in dsMonHoc:
            hs1 = [randScore(tb),randScore(tb),randScore(tb)]
            hs2 = [randScore(tb)]
            hs3 = [randScore(tb)]
            diemTB = round((sum(hs1) + sum(hs2)*2 + sum(hs3)*3) / (len(hs1) + len(hs2)*2 + len(hs3)*3),2)
            diem = DiemSo(hocSinh = hs, monHoc = mon_hoc, heSo1 = hs1, heSo2 = hs2, heSo3 = hs3, diemTB = diemTB)
        hs.diemTB = round(sum(d.diemTB for d in hs.diemSo) / len(hs.diemSo),2)
        # Tính hạnh kiểm
        if hs.diemTB >= 6.5: hs.hanhKiem = random.choice(['Tốt','Khá'])
        elif hs.diemTB >= 5: hs.hanhKiem = random.choice(['Khá','Trung bình'])
        else: hs.hanhKiem = random.choice(['Trung bình','Yếu'])

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
            nv = NhanVien(hoTen = ten, ngaySinh = createRandomDate(1960, 1995), gioiTinh = gt, toChuc = [tc], chucVu = [cv], heSoLuong = round(random.uniform(1, 9),1))
            dsNV.append(nv)
            phong = Phong(ten = f'Phòng {cv.ten} {i+1}' if soNV > 1 else f'Phòng {cv.ten}')
            tc.phong.append(phong)
            dsPhong.append(phong)
            nv.phongLamViec = [phong]
    
    # Cho kế toán làm tổ trưởng và văn thư làm tổ phó
    nv = [nv for nv in dsNV if nv.chucVu[0].ten == 'Kế toán'][0]
    nv.chucVu.append(toTruong)
    nv = [nv for nv in dsNV if nv.chucVu[0].ten == 'Văn thư'][0]
    nv.chucVu.append(toPho)

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
            diemDanh = DiemDanh(hoatDong = hd, nguoi = hs, ngayGio = createDateTime(hd.ngayBatDau, random.randint(7, 9)), trangThai = random.choice(['Có mặt', 'Vắng']))
            dsDiemDanh.append(diemDanh)