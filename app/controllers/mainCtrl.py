from models import onto

def get_HS():
    return onto.HocSinh.instances()

def get_LopHoc():
    return onto.LopHoc.instances()

def get_GiaoVien():
    return onto.GiaoVien.instances()

def get_MonHoc():
    return onto.MonHoc.instances()

def get_dsLop():
    return [{'id':lop.name, 'ten':lop.ten} for lop in onto.LopHoc.instances()]

def get_dsToChuc(includeClass = False):
    if includeClass:
        return [{'id': tc.name, 'ten': tc.ten} for tc in onto.ToChuc.instances()]
    else:
        lsLop = onto.LopHoc.instances()
        return [{'id': tc.name, 'ten': tc.ten} for tc in onto.ToChuc.instances() if tc not in lsLop]