'''
hash function
'''

from geo.segment import Segment
from geo.quadrant import Quadrant

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

def hacher(points, t):
    '''
    the first hash table, defined by h(p) = (int(p.x/t), int(p.y/t)) as in the subject
    requires an array of the considered points and the precision t
    returnes the hash table
    '''
    return {}

def ordered_segments(points):
    '''
    requires an array of the considered points
    returns an iterable of segments
    '''
    t = 1.0 #Il faut initialiser t à une valeur, ici j'ai choisi 1 mais ça aurait pu être n'importe quoi de positif.
    tables = hacher(points, t) #tables est un dictionnaire
    collisions = tables!={} or max(len([valeurs for valeurs in tables.values()]))>1
    # J'estime qu'il n'y a pas de collision quand chaque clé a au plus un élément ou que la liste est vide
    while collisions:
        t = t/2
        tables = {**tables, **hacher(points, t)}
