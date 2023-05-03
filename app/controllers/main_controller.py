import models.model as model

class MainController:
    def get_HS(self):
        return model.onto.HocSinh.instances()

    def get_LopHoc(self):
        return model.onto.LopHoc.instances()

    def get_GiaoVien(self):
        return model.onto.GiaoVien.instances()
    
    def get_MonHoc(self):
        return model.onto.MonHoc.instances()
    