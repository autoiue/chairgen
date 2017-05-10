# chairgen

Generate chairs using machine learning

## Why

ChairGen est ma première approche des technologies d'intelligence artificielle pour le design est la création, le but étant de concevoir un objet de A-Z avec l'intelligence artificielle puis de le produire ou de le faire produire.
En corrélation avec les témoignages des professionnels, cette expérience me permettra de déterminer quel est le processus nécéssaires à la mise en place de cette technologie.

## Tools

You will find tools scripts in the `tools` folder. They are used to convert data in differents formats to process it. 

| world to polygons | polygones to point cloud | generator | point cloud to polygons | polygons to real world |
|:-----------------:|--------------------------|-----------|-------------------------|------------------------|
|                   | MeshLabImport            | `../keras/*`  | MeshLabExport           | [Cura](https://ultimaker.com/en/products/cura-software)                |
|                   |                | VoxelMix, VoxelView  |        `voxels.scad`       |                        |