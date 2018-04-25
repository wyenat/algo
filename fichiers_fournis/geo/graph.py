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
            while len(self.points_degre_impair) != 0:
                segment = next(segments)
                if segment.coordinates[0] in self.points_degre_impair and segment.coordinates[1] in in self.points_degre_impair:
                    self.vertices[segment.coordinates[0]].append(segment)
                    self.vertices[segment.coordinates[1]].append(segment)
                    self.points_degre_impair.remove(segment.coordinates[0])
                    self.points_degre_impair.remove(segment.coordinates[1])
                compteur += 1
            print("On sort de la boucle en {} étapes".format(compteur))

    def quad_iter_impaire(self):
        '''
        return an iterator of all segments, sorted by increasing length, between all of the points having odd degrees
        '''
        pass


    def eulerian_cycle(self):
        """
        return eulerian cycle. precondition: all degrees are even.
        """
        """ Alors voilà l'idée : on part d'un point, et on tente d'établir un cycle depuis
        un point du graphe, et on suit à chaque fois le premier segment disponible par un interateur
        sur les segments, en le notant dans un tableau des segments utilisés :
        - s'il y en a plus de deux, on sauvegarde l'état des segments utilisés
        avant de faire ce choix, puis on prend le premier
        - s'il n'y en pas, on revient à l'état sauvagardé, et on place le choix qu'on avait fait en premier
        en dernier, puis on réapplique l'algorithme
        point = next(iter(self.vertices.keys()))
        used = []
        pt_restore = []
        compteur = 0
        nombre_passage = 0
        while compteur < self.nb_segment **3:
            dispo = self.iterateur_segments_non_utilises(point, used)
            if nombre_passage != 0:
                dispo[0], dispo[nombre_passage] = dispo[nombre_passage], dispo[0]
            if len(dispo) > 1:
                if point != pt_restore[-1]:
                    restore = used.copy()
                    pt_restore.append(Point(point.coordinates))
                    nombre_passage = 0
            if len(dispo) == 0:
                if len(used) == self.nb_segment:
                    return used
                point = pt_restore.pop()
                used = restore
                nombre_passage += 1
                continue
            used.append(Segment([point, dispo[0]]))
            point = dispo[0]
        print("Algo en n³, aucun intérêt ma louloute")"""

    def iterateur_segments_non_utilises(self, point, used):
        '''
        return all segment available from a point that haven't being used before
        '''
        pass
