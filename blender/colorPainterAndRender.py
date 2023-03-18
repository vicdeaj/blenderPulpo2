import bpy
import os
import sys
# enable importing other files
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
os.chdir(dir)

def reset_materials():
    # Get a list of all materials in the scene
    materials = bpy.data.materials

    # Loop through the materials and remove each one
    for material in materials:
        bpy.data.materials.remove(material, do_unlink=True)

    # Create 4 materials and assign colors
    materials = []
    
    # index 0
    material1 = bpy.data.materials.new(name="EnProceso")
    material1.diffuse_color = (0.799, 0.373, 0.102, 1.0)
    materials.append(material1)
    
    # index 1
    material2 = bpy.data.materials.new(name="Asignada")
    material2.diffuse_color = (0.8, 0.006, 0.004, 1.0)
    materials.append(material2)
    
    # index 2
    material3 = bpy.data.materials.new(name="Terminada")
    material3.diffuse_color = (0.124, 0.8, 0.039, 1.0)
    materials.append(material3)
    
    # index 3
    material4 = bpy.data.materials.new(name="Empty")
    material4.diffuse_color = (0.346, 0.406, 0.800, 1.0)
    materials.append(material4)

    # index 4
    material5 = bpy.data.materials.new(name="Recibida")
    material5.diffuse_color = (1.0, 1.0, 1.0, 1.0)
    materials.append(material4)

    # Assign materials to all objects in scene
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            obj.data.materials.clear()
            obj.data.materials.append(material4)
    #        for i, material in enumerate(materials):
    #            obj.data.materials.append(material)
    #            obj.material_slots[i].material = material

reset_materials()

#from snaphot import snapshot
from descarga_archivos import getDocumento
snapshot = getDocumento()
print("Conseguido el documento")

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
        elif archivo.status == "Recibida":
            objeto.material_slots[0].material = bpy.data.materials['Recibida']

print("pinrtado")

# Set the output file path and format
render_output_path = "/tmp/output/image.png"

# Set the render engine and output resolution
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

# Set the number of samples to render
bpy.context.scene.cycles.samples = 100

# Render the scene
bpy.ops.render.render(write_still=True)

# Save the rendered image to the specified output path and format
bpy.data.images['Render Result'].save_render(filepath=render_output_path, 
                scene=bpy.context.scene )

print("terminado")
print(bpy.data.images)
