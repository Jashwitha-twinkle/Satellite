from sklearn.neighbors import KDTree
import numpy as np

class SpatialIndex:

    def __init__(self, positions):

        # 🚨 handle empty input
        if positions is None or len(positions) == 0:
            self.positions = np.empty((0, 3))
            self.tree = None
            return

        self.positions = np.array(positions)

        # 🚨 ensure correct shape
        if self.positions.ndim == 1:
            self.positions = self.positions.reshape(1, -1)

        # 🚨 must have at least 2 points to form pairs
        if len(self.positions) < 2:
            self.tree = None
            return

        self.tree = KDTree(self.positions)


    def query_neighbors(self, radius):

        # 🚨 no tree → no pairs
        if self.tree is None:
            return []

        neighbors = self.tree.query_radius(self.positions, r=radius)

        pairs = []

        for i, neigh in enumerate(neighbors):
            for j in neigh:

                # avoid duplicates and self-pairs
                if j <= i:
                    continue

                pairs.append((i, j))

        return pairs