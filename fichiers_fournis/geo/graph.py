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
        self.connexes = None

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
            self.connexes = self.composantes_connexes()
            representant = self.connexes.iter_repr()
            point_relais = next(representant) #A améliorer c complexité caca
            segments_tries = self.rajouter_segments()
            compteur = 0
            while self.connexes.size != 1:
                if self.connexes.find(segments_tries[compteur].endpoints[0]) != self.connexes.find(segments_tries[compteur].endpoints[1]):
                    self.connexes.union(segments_tries[compteur].endpoints[0], segments_tries[compteur].endpoints[1])
                    self.vertices[segments_tries[compteur].endpoints[0]].append(segments_tries[compteur])
                    self.vertices[segments_tries[compteur].endpoints[1]].append(segments_tries[compteur])
                compteur += 1

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

    def composantes_connexes(self):
        """
        calcule les composantes connexes et crée les classes dans l'union-find
        """
        points = [key for key in self.vertices.keys()]
        connexes = UnionFind(points)
        for point in points:
            for p in [[bout for bout in segment.endpoints if bout!=point] for segment in self.vertices[point]]:
                connexes.union(point, p[0])
        return connexes

    def rajouter_segments(self):
        '''
        return the shortest segments needed to connect all the composantes_connexes
        '''
        partie_connexe = {}
        segments = []
        for representant in self.connexes.iter_repr():
            if representant not in partie_connexe:
                partie_connexe[representant] = [representant]
            for element in self.connexes.parents.keys():
                if self.connexes.parents[element] == representant:
                    partie_connexe[representant].append(element)
        deja_passe = []
        for representant in partie_connexe:
            deja_passe.append(representant)
            for element in partie_connexe[representant]:
                for autre_representant in partie_connexe:
                    if autre_representant in deja_passe:
                        continue
                    for flement in partie_connexe[autre_representant]:
                        segments.append(Segment([element, flement]))
        return sorted(segments, key= lambda seg: seg.length())
