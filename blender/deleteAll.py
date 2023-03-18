import bpy

# Delete all objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Delete all collections
for collection in bpy.data.collections:
    bpy.data.collections.remove(collection)