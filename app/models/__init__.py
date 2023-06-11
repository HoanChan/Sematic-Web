from .model import *
from .rulers import *
from owlready2 import *
onto = get_ontology("app/data/education.owl").load()
rulers.apply_rules(onto)
# rulers.startSyncPellet(onto)
# rulers.startSyncHermiT(onto)