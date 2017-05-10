# chairgen

Generate chairs using machine learning

## Why

ChairGen est ma première approche des technologies d'intelligence artificielle pour le design est la création, le but étant de concevoir un objet de A-Z avec l'intelligence artificielle puis de le produire ou de le faire produire.
En corrélation avec les témoignages des professionnels, cette expérience me permettra de déterminer quel est le processus nécéssaires à la mise en place de cette technologie.

## Workflow

You will find tools scripts in the `tools` folder. They are used to convert data in differents formats to process it. 

| world to polygons | polygones to point cloud | generator | point cloud to polygons | polygons to real world |
|:-----------------:|--------------------------|-----------|-------------------------|------------------------|
|[Photoscan](http://www.agisoft.com/)| `ToPointCloud_MeshLab/import.py` | all files in `keras/`  | `ToPoly_Scad/export.py` | [Cura](https://ultimaker.com/en/products/cura-software), etc. |
|                   |       VoxelView,         |  VoxelMix  |         |                        |

### ToPointCloud_MeshLab/import.py

This script will recursively find every compatible polygonal files in an input folder to convert it to point cloud files.


    usage: import.py [-h] [-s SCRIPT] [-v] [-S] -i [INPUT] -o [OUTPUT]

    -h : print help message
    -s : script to apply (default: "import_poisson.mlx", 50000 points)
    -v : verbose (without it it will fail silently)
    -S : sort points


This script require Python 3 and Meshlab.

### ToPoly_Scad/export.py

This script will recursively find every `.yxz` files in an input folder to convert it to `.scad`.

    usage: export.py [-h] [-s SCRIPT] -i [INPUT] -o [OUTPUT]

    -h : print help message
    -s : script to apply (default: "voxels.scad"), this file should contain at least "module atom(x, y, z){}"
    

This script require Python 3 (not OpenScad).
