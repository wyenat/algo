"""
union find structure.
fast version, see https://fr.wikipedia.org/wiki/Union-find
"""
class UnionFind:
    """
    store a set of items with equivalence relations.
    an equivalence class is identified by the class representant.
    you can find the representant of any item using "find" and
    fuse two classes together using "union".
    """
    #pylint: disable = dangerous-default-value
    def __init__(self, items=[]):
        self.parents = dict()
        self.ranks = dict()
        self.size = 0
        for item in items:
            self.add(item)

    def add(self, item):
        """
        add a new element
        """
        self.parents[item] = item
        self.ranks[item] = 0
        self.size += 1

    def find(self, item):
        """
        return who is representing the class of given item.
        """
        if self.parents[item] != item:
            self.parents[item] = self.find(self.parents[item])
        return self.parents[item]

    def union(self, item1, item2):
        """
        put item1 and item2 in same equivalence class.
        """
        root1 = self.find(item1)
        root2 = self.find(item2)
        rank1 = self.ranks[root1]
        rank2 = self.ranks[root2]
        if root1 != root2:
            self.size -= 1
            if rank1 < rank2:
                self.parents[root1] = root2
            else:
                self.parents[root2] = root1
                if rank1 == rank2:
                    self.ranks[root1] += 1

    def __len__(self):
        """
        return how many different groups we have
        """
        return self.size
