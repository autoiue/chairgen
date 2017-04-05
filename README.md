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

## Log file

#### Avancée au 8 mars

- Installation des librairies de machine learning sur l'ordinateur ENSADLAB dédié au Machine Learning
- Collection de 20 modèles de chaises (collection)
- Esquisse : chaise mixée (code Processing)
![Modèle voxel d'une chaise](/home/procsynth/LOCALDEV/CyberChair/results/images/Screenshot from 2017-02-22 14-58-38.png)

![Esquisse de ce que pourrais donner un tel programme](/home/procsynth/LOCALDEV/CyberChair/results/images/Screenshot from 2017-03-08 13-41-32.png)

#### Avancée au 15 mars

- Visualiseur 3D pour les voxels
- Maîtrise de la mise en forme de données en tableaux multidimensionels (avec Keras + TensorFlow + Numpy)
- Premier résultat du programme de machine learning : je ne maitrise pas du tout cette technologie, je suis bloqué et ai commencé a faire appel à des experts
- Premier contact avec une directrice de laboratoire à l'INRIA, livre blanc de l'INRIA sur l'IA

![Premier résulat innatendu du programme](/home/procsynth/LOCALDEV/CyberChair/results/images/Screenshot from 2017-03-09 14-59-17.png)

#### Avancé au 22 mars

- Changement de stratégie pour la représentation de chaise (Voxels vs random points on surface) (65k points par modèle)
- Changement de stratégie pour le type de NN : à tester : autoencoders et Variational AutoEncoder (VAE)
- Openscad à la rescousse pour la production de modèles STL imprimables à partir de voxels. (trois chaises imprimables/4 pour le 29) (28 minutes de rendu pour 15k points).


## Références
Ici soient des projets qui utilisent l'AI pour générer des formes, compositions, etc.

- [Livre blanc INRIA sur l'IA](https://www.inria.fr/actualite/actualites-inria/livre-blanc-sur-l-intelligence-artificielle)
- [Movie written by algorithm turns out to be hilarious and intense](https://arstechnica.com/the-multiverse/2016/06/an-ai-wrote-this-movie-and-its-strangely-moving/)
- [So. Algorithms Are Designing Chairs Now](https://www.wired.com/2016/10/elbo-chair-autodesk-algorithm/)
- [What Happens When Algorithms Design a Concert Hall? The Stunning Elbphilharmonie](https://www.wired.com/2017/01/happens-algorithms-design-concert-hall-stunning-elbphilharmonie/)
- [A gentle guide to machine learning](https://blog.monkeylearn.com/a-gentle-guide-to-machine-learning/)

Répertoires de chaises
- [We sit together](http://www.ensba-lyon.fr/horsmurs/1516/utopianbenches/)


faire des chaises de demain > comment s'assoient les gens demain ?
quelles entrées ? Sources  ? Morpho, modes de vies, lien avec l'hommes, quelques données pour l'homme ?

Alexandra Midale (introduction au design)
Katarine Beesher

Comment accompagner un chamengment de société

lister what it take to make a chair ?

nom, non > utiliser le verbe

commetn moins s'assoir ? Comment la machine peut répondre à cette question, make sense of data, analyse ?

le ML pour quel usage dans le design ? la création ?
quel vision pour le ML ?


revenir sur l'intention de départ transition du travail

décrire le futur ? Faire le premir pas, vers le futur ,maitriser le chemin comment, abbérations ? vers un monde idéal