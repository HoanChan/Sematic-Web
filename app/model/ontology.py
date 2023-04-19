from owlready2 import *

class Data:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.onto = get_ontology("data/data.owl").load()
            cls._instance.create_database()
        return cls._instance

    def create_database(self):
        with self.onto:
            class Nguoi(Thing):
                pass

            class hoc_sinh(Nguoi):
                pass
            
            class giao_vien(Nguoi):
                pass
            
            class mon_hoc(Thing):
                pass
            
            class co_hoc_sinh(ObjectProperty):
                domain = [mon_hoc]
                range = [hoc_sinh]

            class co_giao_vien(ObjectProperty):
                domain = [mon_hoc]
                range = [giao_vien]

            class hoc_sinh_ten(DataProperty, FunctionalProperty):
                domain = [hoc_sinh]
                range = [str]

            class giao_vien_ten(DataProperty, FunctionalProperty):
                domain = [giao_vien]
                range = [str]

            class mon_hoc_ten(DataProperty, FunctionalProperty):
                domain = [mon_hoc]
                range = [str]

        self.onto.save(file="data/data.owl")