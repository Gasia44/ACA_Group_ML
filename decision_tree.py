import numpy as np
from collections import defaultdict
import operator


class DecisionNode(object):

    def __init__(self,
                 column=None,
                 value=None,
                 true_branch=None,
                 false_branch=None,
                 current_results=None,
                 is_leaf=False,
                 results=None):
        self.column = column
        self.value = value
        self.false_branch = false_branch
        self.true_branch = true_branch
        self.current_results = current_results
        self.is_leaf = is_leaf
        self.results = results

def dict_of_values(data):
    results = defaultdict(int)
    for row in data:
        r = row[0]
        results[r] += 1
    return dict(results)


def divide_data(data, feature_column, feature_val):
    data1 = [row for row in data if int(row[feature_column]) >= feature_val]
    data2 = [row for row in data if int(row[feature_column]) < feature_val]

    return data1, data2


def gini_impurity(data1, data2):
    N1=len(data1)
    N2=len(data2)

    p_k1=list(dict.values(dict_of_values(data1)))
    p_k2=list(dict.values(dict_of_values(data2)))

    gini1=0
    gini2=0
    for i in range(len(p_k1)):
        gini1=gini1+p_k1[i]*(N1-p_k1[i])/N1
    for i in range(len(p_k2)):
        gini2 = gini2 + p_k2[i] * (N2 - p_k2[i]) / N2

    return gini1+gini2


def build_tree(data, current_depth=0, max_depth=1e10):
    data=np.array(data)
    if len(data) == 0:
        return DecisionNode(is_leaf=True, results=data[0][0])

    if(current_depth == max_depth):
        return DecisionNode(current_results=dict_of_values(data),is_leaf=True,results=(max(dict_of_values(data).items(), key=operator.itemgetter(1))[0]))

    if(len(dict_of_values(data)) == 1):
        return DecisionNode(current_results=dict_of_values(data), is_leaf=True,results=list(dict_of_values(data).keys())[0])

    gfvd1d2 = []  # matrix of Gini, feature, variable
    for i in range(1,data.shape[1]):
        vars = set([row[i] for row in data])
        for var in vars:
            data1, data2 = divide_data(data, i, var)
            gfvd1d2.append([gini_impurity(data1, data2), i, var, data1, data2])

    best = [row for row in gfvd1d2 if row[0] == min(l[0] for l in gfvd1d2)][0]

    data1 = best[3]
    data2=best[4]


    #This calculates gini number for the data before dividing
    self_gini = gini_impurity(data, [])

    #if best_gini is no improvement from self_gini, we stop and return a node.

    if abs(self_gini - best[0]) < 1e-10:
        return DecisionNode(current_results=dict_of_values(data), is_leaf=True, results=(max(dict_of_values(data).items(), key=operator.itemgetter(1))[0]))
    else:
        t1 = build_tree(data1, current_depth=current_depth+1)
        t2 = build_tree(data2, current_depth=current_depth+1)

        return DecisionNode(best[1],best[2],t1,t2) #<---- FIX THIS


class DecisionTree(object):

    def __init__(self, max_tree_depth):
        self.max_depth = max_tree_depth

    def fit(self, data):
        self.tree=build_tree(data)


    def predict(self, data):
        Y=[]
        for i in range(len(data)):
            Y.append(test(self.tree, data[i]))
        return Y

def test(tree,a):
    if tree.is_leaf == True:
        return tree.results

    if a[tree.column] >= tree.value:
        return test(tree.true_branch, a)
    else:
        return test(tree.false_branch, a)

