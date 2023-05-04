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
    
    def search_HS(self, hoTen, hocLop, ngaySinh, gioiTinh):
        query_str = """
        PREFIX s: <http://hc.com/school#>
        SELECT ?hs
        WHERE {
            ?hs a s:HocSinh.
        """
        if hoTen: query_str += '?hs s:hoTen ?hoTen.' + f'FILTER(REGEX(?hoTen, ".*{hoTen}.*","i")).'
        if hocLop: query_str += '?hs s:hocLop ?lop. ?lop s:ten ?tenLop.' + f'FILTER(REGEX(?tenLop, ".*{hocLop}.*","i")).'
        if ngaySinh: 
            dateParts = ngaySinh.split("-")
            if len(dateParts) == 3: # Xủ lý ngày tháng năm do bên js giởi lên có dạng yyyy-mm-dd
                ngaySinh = dateParts[2] + '/' + dateParts[1] + '/' + dateParts[0]
            query_str += f'?hs s:ngaySinh "{ngaySinh}".'
        if gioiTinh: query_str += f'?hs s:gioiTinh "{gioiTinh}".'
        query_str += '}'
        print(query_str)
        result = default_world.sparql(query_str)
        dsHS = []
        if result:
            dsHS = list(map(lambda hs: {'id': hs[0].iri.split('#')[1],
                                        'hoTen': hs[0].hoTen, 
                                        'hocLop': hs[0].hocLop.ten, 
                                        'ngaySinh': hs[0].ngaySinh, 
                                        'gioiTinh': hs[0].gioiTinh}, result))
        return dsHS