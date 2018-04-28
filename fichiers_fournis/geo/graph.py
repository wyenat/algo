"""
graph structure
"""
from itertools import chain, combinations
from geo.quadrant import Quadrant
from geo.union import UnionFind
from geo.segment import Segment
from geo.point import Point
from geo.hash import ordered_segments
from geo.tycat import tycat
from time import sleep

class Graph:
    """
    create a graph from given set of segments.
    each endpoint is a vertex, each segment an edge.
    """
    def __init__(self, segments):
        self.vertices = dict()
        self.nb_segment = len(segments)
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

    def reconnect(self, hash_points):
        """
        greedily add edges until graph is fully connected.
        if hash_points is true then use hashed segments iterator
        else use quadratic segments iterator.
        """
        self.connexes = self.composantes_connexes()
        if hash_points: #Cas du pseudo code 1
            for segment in ordered_segments([key for key in self.vertices.keys()]):
                if self.connexes.size == 1:
                    break
                elif self.connexes.find(segment.endpoints[0]) != self.connexes.find(segment.endpoints[1]):
                    self.connexes.union(segment.endpoints[0], segment.endpoints[1])
                    self.vertices[segment.endpoints[0]].append(segment)
                    self.vertices[segment.endpoints[1]].append(segment)
                    self.nb_segment += 1
        else:
            segments_tries = self.rajouter_segments()
            compteur = 0
            while self.connexes.size != 1:
                if self.connexes.find(segments_tries[compteur].endpoints[0]) != self.connexes.find(segments_tries[compteur].endpoints[1]):
                    self.connexes.union(segments_tries[compteur].endpoints[0], segments_tries[compteur].endpoints[1])
                    self.vertices[segments_tries[compteur].endpoints[0]].append(segments_tries[compteur])
                    self.vertices[segments_tries[compteur].endpoints[1]].append(segments_tries[compteur])
                    self.nb_segment +=1
                compteur += 1

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


    def even_degrees(self, hash_points):
        """
        greedily add edges until all degrees are even.
        if hash_points is true then use hashed segments iterator
        else use quadratic segments iterator.
        """
        if hash_points:
            return
        else:
            self.points_degre_impair = [point for point in self.vertices.keys() if len(self.vertices[point])%2]
            segments = self.quad_iter_impaire()
            compteur = 0
            while len(self.points_degre_impair) > 0 and compteur < len(segments):
                segment = segments[compteur]
                if (segment.endpoints[0] in self.points_degre_impair):
                    if (segment.endpoints[1] in self.points_degre_impair):
                        if segment.endpoints[0] != segment.endpoints[1]:
                            self.vertices[segment.endpoints[0]].append(segment)
                            self.vertices[segment.endpoints[1]].append(segment)
                            self.points_degre_impair.remove(segment.endpoints[0])
                            self.points_degre_impair.remove(segment.endpoints[1])
                            self.nb_segment += 1
                compteur += 1
            if len(self.points_degre_impair) == 2:
                #Il faut encore tracer le segment entre les 2 derniers points
                p1 = self.points_degre_impair[0]
                p2 = self.points_degre_impair[1]
                segment = Segment([p1, p2])
                self.vertices[p1].append(segment)
                self.vertices[p2].append(segment)
                self.points_degre_impair.remove(p1)
                self.points_degre_impair.remove(p2)
                self.nb_segment += 1
            self.points_degre_impair = [point for point in self.vertices.keys() if len(self.vertices[point])%2]
            print("Le graphe ne contient que des degrés pairs : {}".format(self.has_even_degrees()))

    def quad_iter_impaire(self):
        '''
        return an iterator of all segments, sorted by increasing length, between all of the points having odd degrees
        '''
        segments_concernes = []
        n = len(self.points_degre_impair)
        for i in range(n-1):
            for j in range(i,n-1):
                segments_concernes.append(Segment([self.points_degre_impair[i],self.points_degre_impair[j]]))
        return sorted(segments_concernes, key=lambda seg: seg.length())

    def has_even_degrees(self):
        """
        return a boolean that states if the graphs contains only points with even degrees
        """
        nombre = len([point for point in self.vertices.keys() if len(self.vertices[point])%2])
        return nombre == 0

    def eulerian_cycle(self):
        """
        return eulerian_cycle
        """
        for point in self.vertices.keys():
            premier_point = point
            break
        graphe = self.create_eulerian(premier_point)
        segments = []
        for i in range(len(graphe)-1):
            segments.append(Segment([graphe[i], graphe[i+1]]))
        print("Chaque segment est parcouru une unique fois : {}".format(len(segments)==self.nb_segment))
        return segments

    def create_eulerian(self, point):
        """
        return eulerian_cycle
        """
        if point in self.vertices.keys():
            voisins = [segment.endpoint_not(point) for segment in self.vertices[point]]
        else:
            return []
        if len(voisins)==0:
            return [point]
        else:
            cycle = self.cycle_quelconque(point)
            Liste = []
            for punto in cycle:
                Liste= Liste + self.create_eulerian(punto)
            return Liste


    def cycle_quelconque(self, point):
        """
        return a cycle that originates from point
        """
        origine = point.copy()
        cycle = [point]
        segment = self.vertices[point].pop(0)
        point = segment.endpoint_not(point)
        self.vertices[point].remove(segment)
        while point != origine:
            cycle.append(point)
            if len(self.vertices[point]) == 0:
                point = origine
                continue
            segment = self.vertices[point].pop(0)
            point = segment.endpoint_not(point)
            self.vertices[point].remove(segment)
        cycle.append(point)
        return [points for points in cycle]
