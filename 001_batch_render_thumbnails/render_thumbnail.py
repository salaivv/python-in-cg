# render_thumbnail.py

import bpy
from bpy import context
from mathutils import Vector


def render_thumbnail():
    '''Render thumbnail'''

    # Setup render settings
    scene = context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    scene.render.resolution_x = 1024
    scene.render.resolution_y = 1024
    scene.render.film_transparent = True
    scene.cycles.film_transparent_glass = True
    scene.cycles.use_denoising = True
    scene.cycles.denoiser = 'OPENIMAGEDENOISE'
    scene.cycles.samples = 128
    scene.view_settings.exposure = -0.5

    # Setup environment
    bpy.ops.world.new()
    scene.world = bpy.data.worlds[-1]
    scene.world.use_nodes = True
    world_node_tree = scene.world.node_tree
    world_node_tree.nodes.new(type="ShaderNodeTexSky")
    sky = world_node_tree.nodes[-1]
    sky.sun_intensity = 0
    bg = world_node_tree.nodes["Background"]
    bg.inputs["Strength"].default_value = 1
    world_node_tree.links.new(sky.outputs['Color'], bg.inputs['Color'])

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Add a camera at an oblique angle
    bpy.ops.object.camera_add(location=(1.9898, -1.8648, 1.6388),
                              rotation=(1.110029, 0, 0.8150688))
    scene.camera = context.active_object
    cam = context.active_object

    # Select all objects except camera
    for obj in bpy.data.objects:
        if obj.type != 'CAMERA':
            obj.select_set(state=True)

    # Set camera to view the selected objects
    bpy.ops.view3d.camera_to_view_selected()
    
    # Move camera along local Z axis backwards to create
    # some padding around the object in view
    vec = Vector((0.0, 0.0, 0.75))
    inv = cam.matrix_world.copy()
    inv.invert()
    vec_rot = vec @ inv
    cam.location += vec_rot

    # Render out the thumbnail
    thumbnail_path = bpy.data.filepath[:-6] + '_thumb.png'

    bpy.ops.render.render()
    bpy.data.images["Render Result"].save_render(filepath=thumbnail_path)


if __name__ == "__main__":
    render_thumbnail()
