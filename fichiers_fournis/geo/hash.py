from geo.segment import Segment
from geo.quadrant import Quadrant
from math import floor
TAILLE_ENVIRONNEMENT = 1

def construire_hashage(points, precision):
    """
    construit la structure de 4 tables de hashage
    """
    structure = [{},{},{},{}]
    borne = floor(TAILLE_ENVIRONNEMENT/precision)
    for i in range(-borne, borne):
        for j in range(-borne, borne):
            structure[0][(i,j)] = []
            structure[1][(i,j)] = []
            structure[2][(i,j)] = []
            structure[3][(i,j)] = []
    for point in points:
        c0, c1, c2, c3 = hacher(point, precision)
        structure[0][c0].append(point)
        structure[1][c1].append(point)
        structure[2][c2].append(point)
        structure[3][c3].append(point)
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

def collision(structure):
    """
    Teste s'il y a des collisions au sein des tables de meilleure précision
    """
    for table in structure[0:4]:
        for cellule in table.keys():
            if len(table[cellule]) > 1:
                return True
    return False

def ordered_segments(points):
    """
    Itère sur les segments envisageables de plus en plus grands
    """
    t = 1
    structure = construire_hashage(points, t)
    while(collision(structure)):
        t = t/2
        structure = construire_hashage(points, t) + structure
    for i in range(0, len(structure)//4):
        tabl = structure[4*i : 4*i + 4]
        liste_points = [val[0] for val in list(tabl[0].values()) + list(tabl[1].values()) + list(tabl[2].values()) + list(tabl[3].values()) if val != []]
        for j in range(0, len(liste_points)):
            for k in range(j+1, len(liste_points)):
                seg = Segment([liste_points[j], liste_points[k]])
                yield seg
