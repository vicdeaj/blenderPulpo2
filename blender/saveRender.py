import bpy
import os
import sys
# enable importing other files
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
os.chdir(dir)

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