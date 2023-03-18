import bpy
import os
import sys

# enable importing other files
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
os.chdir(dir)

def delete_all():
    # Delete all objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # Delete all collections
    for collection in bpy.data.collections:
        bpy.data.collections.remove(collection)

EN_PROCESO = 0
ASIGNADA = 1
TERMINADA = 2
EMPTY = 3
def set_materials():
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

    # Assign materials to all objects in scene
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            obj.data.materials.clear()
            obj.data.materials.append(material4)
    #        for i, material in enumerate(materials):
    #            obj.data.materials.append(material)
    #            obj.material_slots[i].material = material


def distribute_coll(collection, axis):
    # Select the objects you want to distribute
    objs = collection.objects

    # Define the axis along which to distribute the objects (0=X, 1=Y, 2=Z)
#    axis = 0

    # Calculate the spacing between objects
    spacing = 0.50

    # Iterate over the objects and set their positions along the chosen axis
    for i, obj in enumerate(objs):
        pos = list(obj.location)
        pos[axis] = i * spacing
        obj.location = tuple(pos)

def distribute_nested_coll(collection, axis):
    # Define the axis along which to distribute the objects (0=X, 1=Y, 2=Z)
    
    subcolls = collection.children
    arrayObjs = [ x.all_objects for x in subcolls]
    
    # Calculate the spacing between objects
    spacing = 0.50
    
    # Iterate over the objects and set their positions along the chosen axis
    for i, objA in enumerate(arrayObjs):
        for obj in objA:
            pos = list(obj.location)
            pos[axis] = i * spacing
            obj.location = tuple(pos)

    
def most_repeated_element(lst):
    # Create a dictionary to count the occurrences of each element
    counts = {}
    for element in lst:
        if element.nombre in counts:
            counts[element.nombre] += 1
        else:
            counts[element.nombre] = 1

    # Find the element with the highest count
    max_count = 0
    max_element = None
    for element, count in counts.items():
        if count > max_count:
            max_count = count
            max_element = element

    return max_element, count

def center_origins_all():
    scene = bpy.context.scene

    mesh_obs = [o for o in scene.objects if o.type == 'MESH']

    if mesh_obs:
        bpy.ops.object.origin_set(
                {"object" : mesh_obs[0],
                "selected_objects" : mesh_obs,
                "selected_editable_objects" : mesh_obs,
                }
            )

def move_archivos_into_collection(listaArchivos, coll_target):
    
    # Loop through all objects
    for archivo in listaArchivos:
        ob =  bpy.data.objects[archivo.id]
        # Loop through all collections the obj is linked to
        for coll in ob.users_collection:
            # Unlink the object
            coll.objects.unlink(ob)

        # Link each object to the target collection
        coll_target.objects.link(ob)



from snaphot import snapshot

delete_all()
for sheet in snapshot:
#for sheet in ["TA"]:
    lista_archivos = snapshot[sheet]
        



    
    for archivo in lista_archivos:
        nombre = archivo.nombre[:-4] # sin .STL
        path = "../piezas_pulpo/" + sheet + "/" + nombre + ".stl"
        bpy.ops.import_mesh.stl(filepath=path, filter_glob="*.stl", global_scale=0.001)
        bpy.data.objects[nombre].name = archivo.id
        
    # move objects from sheet into a collection with its number, within a collection with the sheet name
    nRepeticiones = most_repeated_element(lista_archivos)[1]
    
    collectionRoot = bpy.data.collections.new(sheet)
    bpy.context.scene.collection.children.link(collectionRoot)
    # si solo uno se pone todo en la sheet y aban
    if nRepeticiones == 1:
        move_archivos_into_collection(lista_archivos, collectionRoot)
        distribute_coll(collectionRoot, 0)
        
    # sino hacemos subcolecciones
    elif nRepeticiones == 8:
        for index in range(nRepeticiones):
            coll = bpy.data.collections.new(str(index))
            collectionRoot.children.link(coll)
            
            listaParcial = lista_archivos[index::8]  
            move_archivos_into_collection(listaParcial, coll)
            distribute_coll(coll, 0)
            
        distribute_nested_coll(collectionRoot,2)
    else:
        raise Exception("Numero de repeticiones raro")
    
# distribuir
distribute_nested_coll(bpy.context.scene.collection, 1)
# centrar objetos
center_origins_all()

set_materials()