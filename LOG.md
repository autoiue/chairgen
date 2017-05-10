## Log file

#### Avancée au 8 mars

- Installation des librairies de machine learning sur l'ordinateur ENSADLAB dédié au Machine Learning : [Keras](https://keras.io/)
- Collection de 20 modèles de chaises ([collection](https://github.com/pr0csynth/chairgen/tree/master/data/preprocessed)) 
- Esquisse : chaise mixée ([VoxelMix](https://github.com/pr0csynth/chairgen/tree/master/tools/VoxelView))

![Modèle voxel d'une chaise](https://github.com/pr0csynth/chairgen/raw/master/results/images/Screenshot%20from%202017-02-22%2014-58-38.png)

![Esquisse de ce que pourrais donner un tel programme](https://github.com/pr0csynth/chairgen/raw/master/results/images/Screenshot%20from%202017-03-08%2013-41-32.png)

#### Avancée au 15 mars

- Visualiseur 3D pour les voxels : [VoxelView](https://github.com/pr0csynth/chairgen/tree/master/tools/VoxelView)
- Maîtrise de la mise en forme de données en tableaux multidimensionels (avec Keras + TensorFlow + Numpy)
- Premier résultat du programme de machine learning : je ne maitrise pas du tout cette technologie, je suis bloqué et ai commencé a faire appel à des experts
- Premier contact avec une directrice de laboratoire à l'INRIA, livre blanc de l'INRIA sur l'IA

![Premier résulat innatendu du programme](https://github.com/pr0csynth/chairgen/raw/master/results/images/Screenshot%20from%202017-03-09%2014-59-17.png)

#### Avancé au 22 mars

- Changement de stratégie pour la représentation de chaise (Voxels vs random points on surface) (50k points par modèle)
- Changement de stratégie pour le type de NN : à tester : autoencoders et Variational AutoEncoder ([VAE](https://github.com/pr0csynth/chairgen/blob/master/keras/20032017/chair_20032017.py))
- [Openscad à la rescousse pour la production de modèles STL imprimables à partir de voxels](https://github.com/pr0csynth/chairgen/blob/master/results/chair_SD.scad). (trois chaises imprimables/4 pour le 29) (28 minutes de rendu pour 15k points).

#### Avancé au 9 mai

La technologie des réseaux de neurone n'est pas facile à maîtriser. Je n'ai pas réussi a sortir un seul résultat viable. Avant même de buter sur le réseau de neurone ne lui-même, le problème se situe au niveau de la représentation des données volumétrique. Il n'existe pas à l'heure de solution fonctionnelle pour réprésenter des volumes de manière à ce qu'un réseau de neurone puisse efficacement utiliser ces données. De plus, les "fonctions" ou "layers" de réseau de neurone disponible publiquement ne supporte pas les données 3D ayant un grand "Z" : les images peuvent être considérées comme des données 3D, X et Y pour la position des pixels, Z pour RVB. Mais la grandeur de Z n'est jamais supérieure à 3. Dans le cas de données volumétriques, X, Y et Z sont de grandeur similaire. Il n'existe pas de "layer" pour ce cas de figure.

Il me semble donc plus intéressant de travailler sur la représentation des données volumétrique et les transition RÉEL > POLYGONAL > {format volumétrique} > POLYGONAL > RÉEL.

Un premier essai pour ce {format volumétrique} était de représenter sur une grille 3D la présence ou l'absence de matière (à la manière de Minecraft) : les voxels. Cette solution présente plusieurs inconvénients et pas énormément d'avantages.

 - Bien qu'existant en version manuelle, je n'ai pas pu trouver d'outil permettant de traiter de grande quantité de données (l'idée étant d'avoir ~1000 modèles 3D pour entraîner un réseau de neurone).
 - Plus on désire de resolution, plus on affine la grille. Hors comme on travaille en 3D, pour doubler la résolution, il faut multiplier par 8 (2^3) le nombre de donnée ( 32 x 32 x 32 = 8 x (16 x 16 x 16) ). Les calcul deviennent vite très longs.
- - Ce qui rend difficile le travaille des courbes, les reconstruction VOXEL > POLY ne sont pas "smooth". Le crénelage est inévitable. Ça peut être un style, mais je préfererais une technique me laissant le choix.
 - Le voxel sont codés en 0 ou 1, alors que  les réseau de neurone travaillent de 0 à 1. Il y a une perte de performance, aussi bien à l'affichage qu'au traitement.
 
Je suis donc plutôt parti sur une solution qui conserve les courbes quelque soit la résolution et qui en plus ne nécessite pas de modéles rigoureusement  "water tight" pour tirer des donnés de bonne qualité : le POINT CLOUD.
Le point cloud s'apparente au voxel, mais il les pas aligné sur une grille. La méthode utilisée pour générer ce POINT CLOUD est de placer un point sur la surface polygonales puis d'en placer successivement à une certaine distance prédéterminée, à un angle au hasard. On obtient une liste de points répartis de manière homogène et organique sur la surface. On obtiens alors un tableau en deux dimensions (index, coordonnées) de forme (nb_points, 3 ou 6) ce qui est plus proche de ce que peut gérer un réseau de neurone.

![Représentation en nuage de point](https://github.com/pr0csynth/chairgen/raw/master/results/images/Screenshot%20from%202017-05-10%2010-30-15.png)

On imagine ensuite que le réseau de neurone puisse ensuite travailler avec ce format de donner pour sortir des données du même format. Il se pose donc la question de la reconstruction d'un modèle polygonal pour un traitement ultérieur (impression, fraisage, ...). Il est possible d'utiliser la technique "classique" utilisée pour les scans 3D ou photogramétrie : la technique de reconstruction Poisson. Je n'ai pas eu de grand succès avec mais les formes et matières générées sont intéressantes.

![Reconstruction Poisson sur une assise](https://github.com/pr0csynth/chairgen/raw/master/results/images/Screenshot-from-2017-03-19-19-28-51.png)

Je me suis orienté vers un reconsctruction plus simple qui consiste à remplacer chaque point par une forme géométrique 3D unique. Selon les assymétrie de cet "atome", on obtiens plusieurs effets de matière dépendant de l'orientation des surfaces.

![Reconstruction simple sur une assise](https://github.com/pr0csynth/chairgen/raw/master/results/images/Screenshot%20from%202017-05-08%2023-08-49.png)


## Références
Ici soient des projets qui utilisent l'AI pour générer des formes, compositions, etc.

- [Livre blanc INRIA sur l'IA](https://www.inria.fr/actualite/actualites-inria/livre-blanc-sur-l-intelligence-artificielle)
- [Movie written by algorithm turns out to be hilarious and intense](https://arstechnica.com/the-multiverse/2016/06/an-ai-wrote-this-movie-and-its-strangely-moving/)
- [So. Algorithms Are Designing Chairs Now](https://www.wired.com/2016/10/elbo-chair-autodesk-algorithm/)
- [What Happens When Algorithms Design a Concert Hall? The Stunning Elbphilharmonie](https://www.wired.com/2017/01/happens-algorithms-design-concert-hall-stunning-elbphilharmonie/)
- [A gentle guide to machine learning](https://blog.monkeylearn.com/a-gentle-guide-to-machine-learning/)

Répertoires de chaises
- [We sit together](http://www.ensba-lyon.fr/horsmurs/1516/utopianbenches/)


<!-- faire des chaises de demain > comment s'assoient les gens demain ?
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

-->
