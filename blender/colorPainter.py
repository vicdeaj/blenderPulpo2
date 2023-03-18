import bpy
import os
import sys
# enable importing other files
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
os.chdir(dir)

#from snaphot import snapshot
from descarga_archivos import getDocumento
snapshot = getDocumento()

for sheet in snapshot:
#for sheet in ["TA"]:
    lista_archivos = snapshot[sheet]
    for archivo in lista_archivos:
        objeto = bpy.data.objects[archivo.id]
        if archivo.status == "En proceso":
            objeto.material_slots[0].material = bpy.data.materials['EnProceso']
        elif archivo.status == "Asignada":
            objeto.material_slots[0].material = bpy.data.materials['Asignada']
        elif archivo.status == "Terminada":
            objeto.material_slots[0].material = bpy.data.materials['Terminada']
        elif archivo.status == "null":
            objeto.material_slots[0].material = bpy.data.materials['Empty']
        