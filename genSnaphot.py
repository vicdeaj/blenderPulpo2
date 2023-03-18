print("""from dataclasses import dataclass
@dataclass
class Archivo:
    nombre:str
    id:str
    status:str""")
from blender.descarga_archivos import getDocumento
print("snapshot=",getDocumento())
