# batch_render_thumbnails.py

import os
import sys
import subprocess


this_file = os.path.realpath(__file__)
this_path = os.path.dirname(this_file)
render_thumbnail = os.path.join(this_path, "render_thumbnail.py")

def batch_render_thumbnails(asset_dir):
    for folder, subfolders, files in os.walk(asset_dir):
        for f in files:
            if f.endswith(".blend"):
                blend_file = os.path.join(folder, f)
                subprocess.run(["blender", "-b", blend_file, "-P", render_thumbnail])


if __name__ == "__main__":
    batch_render_thumbnails(sys.argv[1])