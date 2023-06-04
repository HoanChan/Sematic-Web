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
    return list(map(lambda lop:{'id':lop.iri.split('#')[1], 
                                'ten':lop.ten},onto.LopHoc.instances()))
