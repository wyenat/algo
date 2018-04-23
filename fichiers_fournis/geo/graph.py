"""
graph structure
"""
from itertools import chain, combinations
from geo.quadrant import Quadrant
from geo.union import UnionFind
from geo.segment import Segment
from geo.hash import ordered_segments

class Graph:
    """
    create a graph from given set of segments.
    each endpoint is a vertex, each segment an edge.
    """
    def __init__(self, segments):
        self.vertices = dict()
        for segment in segments:
            for point in segment.endpoints:
                if point not in self.vertices:
                    self.vertices[point] = []
                self.vertices[point].append(segment)
        self.connexes = self.composantes_connexes([key for key in self.vertices.keys()]) # A CHANGER

    def bounding_quadrant(self):
        """
        return min quadrant containing underlying objects.
        """
        quadrant = Quadrant.empty_quadrant(2)
        for point in self.vertices:
            quadrant.add_point(point)
        return quadrant

    def svg_content(self):
        """
        svg for tycat.
        """
        edges = (e for (p, edges) in self.vertices.items() for e in edges if e.endpoints[0] == p)
        return "\n".join(c.svg_content() for c in chain(self.vertices.keys(), edges))

    ''' Pseudo code 1 : pour cette fonction :
    Entrées : G : Graphe
    soit C l’ensemble des composantes connexes de G;
    pour chaque segment (p 1 , p 2 )donné par l’itérateur faire
        si p 1 et p 2 appartiennent à deux composantes différentes alors
            ajouter (p 1 , p 2 ) aux arètes de G;
            fusionner les deux composantes correspondantes de C;
        fin
        si |C| = 1 alors
            retourner
        fin
    fin '''

    def reconnect(self, hash_points):
        """
        greedily add edges until graph is fully connected.
        if hash_points is true then use hashed segments iterator
        else use quadratic segments iterator.
        """
        if hash_points: #Cas du pseudo code 1
            for segment in ordered_segments(self.vertices):
                #Je ne sais pas comment faire cette ligne :
                #si p 1 et p 2 appartiennent à deux composantes différentes alors
                pass
        else:
            point_relais = self.connexes.parents.keys()[0]
            for parent in self.connexes.parents.keys():
                if parent is not point_relais:
                    self.connexes.union(parent, point_relais)
                    segment = Segment([parent, point_relais])
                    self.vertices[point_relais].append(segment)
                    self.vertices[parent].append(segment)

    def even_degrees(self, hash_points):
        """
        greedily add edges until all degrees are even.
        if hash_points is true then use hashed segments iterator
        else use quadratic segments iterator.
        """
        pass

    def eulerian_cycle(self):
        """
        return eulerian cycle. precondition: all degrees are even.
        """
        pass

    def composantes_connexes(self, points):
        """
        calcule les composantes connexes et crée les classes dans l'union-find
        """
        connexes = UnionFind(points)
        for point in connexes.parents.keys():
            for p in [[point2 for point2 in bout if bout!=point] for bout in self.vertices[points].endpoints]:
                connexes.union(point, p) #Passage linéaire (suppression des élements de l'iterateur une fois traités)
        return connexes
