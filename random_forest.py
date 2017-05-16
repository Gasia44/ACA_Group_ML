from decision_tree import build_tree
from decision_tree import test
import random
import numpy as np

class RandomForest(object):
    """
    RandomForest a class, that represents Random Forests.

    :param num_trees: Number of trees in the random forest
    :param max_tree_depth: maximum depth for each of the trees in the forest.
    :param ratio_per_tree: ratio of points to use to train each of
        the trees.
    """
    def __init__(self, num_trees, max_tree_depth, ratio_per_tree=0.7):
        self.num_trees = num_trees
        self.max_tree_depth = max_tree_depth
        self.trees = []
        self.ratio_per_tree=ratio_per_tree

    def fit(self, data):
        for i in range(self.num_trees):
            select = list(range(len(data)))
            random.shuffle(select)
            select_train = np.array(select[0:int(len(data)*self.ratio_per_tree)])
    
            data_train = data[select_train, :]
    
            self.trees.append(build_tree(data_train))

    def predict(self, X):
        Y=[]
        for i in range(len(X)):
            y=[]
            conf=0
            for j in range(len(self.trees)):
                y.append(test(self.trees[j], X[i]))
            Ypred=max(set(y), key=y.count)
            conf=y.count(Ypred)*100/len(self.trees)
            Y.append([Ypred,conf])
        return Y
