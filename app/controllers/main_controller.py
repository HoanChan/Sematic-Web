from models.model import onto, default_world
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
        return [lop.ten for lop in onto.LopHoc.instances()]
    
    def search_HS(self, tenHS, lop, ngaySinh, gioiTinh): 
        query_str = """
        PREFIX s: <http://hc.com/school#>
        SELECT ?hs
        WHERE {
            ?hs a s:HocSinh.
            ?hs s:hoTen ?hoTen.
            ?hs s:ngaySinh ?ngaySinh.
            ?hs s:gioiTinh ?gioiTinh.
            ?hs s:hocLop ?lop.
        """
        if tenHS: query_str += f'\n FILTER(REGEX(?hoTen, "{tenHS}","i")).'
        # if lop: query_str += '; :hocLop ?"' + lop + '"'
        # if ngaySinh: query_str += '; :ngaySinh ?"' + ngaySinh + '"'
        # if gioiTinh: query_str += '; :gioiTinh ?"' + gioiTinh + '"'
        query_str += '\n}'
        result = default_world.sparql(query_str)
        dsHS = []
        if result:
            dsHS = list(map(lambda hs: {'hoTen': hs[0].hoTen, 
                                        'hocLop': hs[0].hocLop.ten, 
                                        'ngaySinh': hs[0].ngaySinh, 
                                        'gioiTinh': hs[0].gioiTinh}, result))
        return dsHS