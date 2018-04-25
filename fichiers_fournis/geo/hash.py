'''
hash function
'''

from geo.segment import Segment
from geo.quadrant import Quadrant
from math import floor

TAILLE_ENVIRONNEMENT = 10

''' Le pseudo code à produire est le suivant, dans la fonction ordered_segments :
Entrées : points considérés
Sorties : itérateur sur des segments
t ← précision de départ;
tables ← {hasher(points, t)};
tant que deux points sont en collision dans les dernières tables faire
    t ← t/2;
    tables ← tables ∪ {hasher(points, t)};
fin
pour chaque jeu de tables, des dernières, aux premières faire
    pour chaque table parmi les 4 du jeu faire
        pour chaque clef faire
            pour chaque combinaison de valeurs associées à la clef faire
                proposer le segment;
            fin
        fin
    fin
fin
'''

def construire_hashage(points, t):
    """
    construit à partir de l'itérateur des points et d'une précision donnée
    le mappage spatial: tableau de 4 tables de hashage dont les clés sont le
    coin haut-gauche, et les valeurs les vecteurs de points contenus dans la cellule
    """
    structure = [{}, {}, {}, {}]
    borne_cellule = floor(TAILLE_ENVIRONNEMENT/t)
    for i in range(-borne_cellule, borne_cellule):
        for j in range(-borne_cellule, borne_cellule):
            structure[0][(i, j)] = []
            structure[1][(i, j)] = []
            structure[2][(i, j)] = []
            structure[3][(i, j)] = []
    for point in points:
        cells = hacher(point, t)
        structure[0][cells[0]].append(point)
        structure[1][cells[1]].append(point)
        structure[2][cells[2]].append(point)
        structure[3][cells[3]].append(point)
    return structure


def hacher(point, t):
    '''
    renvoie les cellules correspondantes au point
    '''
    px, py = point.coordinates
    cellule1 = (floor(px/t), floor(py/t))
    cellule2 = (floor((px + t/2)/t), floor(py/t))
    cellule3 = (floor(px/t), floor((py + t/2)/t))
    cellule4 = (floor((px + t/2)/t), floor((py + t/2)/t))
    return (cellule1, cellule2, cellule3, cellule4)

def collisions(structure):
    """
    Determine si les 4 dernières tables de la structure contiennent des collisions
    """
    for table in structure[-5:-1]:
        for key in table.keys():
            if len(table[key]) > 1:
                return False
    return True

def produit_cartesien(liste1, liste2):
    """
    renvoie le produit cartesien de 2 listes
    """
    produit = []
    for element in liste1:
        for flement in liste2:
            produit.append([element, flement])
    return produit

def ordered_segments(points_consideres):
    '''
    requires an array of the considered points
    returns an iterable of segments
    '''
    t = 1

    tables = construire_hashage(points_consideres, t)
    while collisions(tables):
        t = t/2
        tables = tables + construire_hashage(points_consideres, t)
    for i in range(0, (len(tables)//4)):
        tables_considerees = tables[-4*i - 4 : -4*i - 1]
        print(tables_considerees)
        liste_points = [point for point in tables_considerees[0].values()] + [point for point in tables_considerees[1].values()] + [point for point in tables_considerees[2].values()] + [point for point in tables_considerees[3].values()]
        for couple in produit_cartesien(liste_points, liste_points):
            if couple[0] != couple[1]:
                print(couple)
                yield Segment(couple)
