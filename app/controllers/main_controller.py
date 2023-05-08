from models import onto, default_world, destroy_entity
from utils import toDate
class MainController:
    def get_HS(self):
        return onto.HocSinh.instances()

    def get_LopHoc(self):
        return onto.LopHoc.instances()

    def get_GiaoVien(self):
        return onto.GiaoVien.instances()
    
    def get_MonHoc(self):
        return onto.MonHoc.instances()
    def get_dsLop(self):
        return list(map(lambda lop:{'id':lop.iri.split('#')[1], 
                                    'ten':lop.ten},onto.LopHoc.instances()))
    
    def search_HS(self, hoTen, hocLop, ngaySinh, gioiTinh):
        query_str = """
        PREFIX s: <http://hc.com/school#>
        SELECT ?hs
        WHERE {
            ?hs a s:HocSinh.
        """
        if hoTen: query_str += '?hs s:hoTen ?hoTen.' + f'FILTER(REGEX(?hoTen, ".*{hoTen}.*","i")).'
        if hocLop: query_str += '?hs s:hocLop ?lop. ' + f'FILTER(STRENDS(STR(?lop), "#{hocLop}")).'
        if ngaySinh: query_str += f'?hs s:ngaySinh "{toDate(ngaySinh)}".'
        if gioiTinh: query_str += f'?hs s:gioiTinh "{gioiTinh}".'
        query_str += '}'
        # print(query_str)
        result = default_world.sparql(query_str)
        dsHS = []
        if result:
            dsHS = list(map(lambda hs: {'id': hs[0].iri.split('#')[1],
                                        'hoTen': hs[0].hoTen, 
                                        'hocLop': hs[0].hocLop.ten, 
                                        'ngaySinh': hs[0].ngaySinh, 
                                        'gioiTinh': hs[0].gioiTinh}, result))
        return dsHS
    def delete_HS(self, id):
        hs = onto.search_one(iri = f'*#{id}', type = onto.HocSinh)
        if hs:
            destroy_entity(hs)
            return True
        return False
    
    def get_HS(self, id):
        hs = onto.search_one(iri = f'*#{id}', type = onto.HocSinh)
        return hs
    
    def new_HS(self):
        hs = onto.HocSinh()
        return hs.iri.split('#')[1], hs
    
    def save_HS(self, id, hoTen, hocLop, ngaySinh, gioiTinh):
        print('save_HS', id, hoTen, hocLop, ngaySinh, gioiTinh)
        hs = onto.search_one(iri = f'*#{id}', type = onto.HocSinh)
        if hs:
            hs.hoTen = hoTen
            hs.hocLop = onto.search_one(iri = f'*#{hocLop}', type = onto.LopHoc)            
            hs.ngaySinh = toDate(ngaySinh)
            hs.gioiTinh = gioiTinh
            return True
        return False
