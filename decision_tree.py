import numpy as np
from collections import defaultdict
import operator

filename = 'SPECTF.dat'
data = np.loadtxt(filename, delimiter=',')
X = data[:, 1:]
y = np.array([data[:, 0]]).T
n, d = X.shape


class DecisionNode(object):
    """
        README
        DecisionNode is a building block for Decision Trees.
        DecisionNode is a class representing a node in our decision tree
        
        :param column: Columne of features corresponding to division
        :param value: Value of feature that divide data
        :param true_branch: Param of class DecisionNode corresponding to next block if condition is True
        :param false_branch: Param of class DecisionNode corresponding to next block if condition is False
        :param current_results: Dictionary corresponding to quantity of classes on current block
        :param is_leaf: True, if we have only one class on that block
        :param results: Dominant class on that block

            the trees.
    """
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
    """
        param data: a 2D Python list representing the data. Last column of data is Y.
        return: returns a python dictionary showing how many times each value appears in Y
    
        for example 
        data = [[1,'yes'],[1,'no'],[1,'yes'],[1,'yes']]
        dict_of_values(data)
        should return {'yes' : 3, 'no' :1}
    """

    results = defaultdict(int)
    for row in data:
        r = row[0]
        results[r] += 1
    return dict(results)


def divide_data(data, feature_column, feature_val):
    '''
        this function takes the data and divides it in two parts by a line. A line
        is defined by the feature we are considering (feature_column) and the target 
        value. The function returns a tuple (data1, data2) which are the desired parts of the data.
        For int or float types of the value, data1 have all the data with values >= feature_val
        in the corresponding column and data2 should have rest.
        For string types, data1 should have all data with values == feature val and data2 should 
        have the rest.
    
        :param data: a 2D Python list representing the data. Last column of data is Y.
        :param feature_column: an integer index of the feature/column.
        :param feature_val: can be int, float, or string
        :return: a tuple of two 2D python lists
    '''
    data1 = [row for row in data if int(row[feature_column]) >= feature_val]
    data2 = [row for row in data if int(row[feature_column]) < feature_val]

    return data1, data2


def gini_impurity(data1, data2):
    """
    Given two 2D lists of compute their gini_impurity index. 
    Remember that last column of the data lists is the Y
    Lets assume y1 is y of data1 and y2 is y of data2.
    gini_impurity shows how diverse the values in y1 and y2 are.
    gini impurity is given by 

    N1*sum(p_k1 * (1-p_k1)) + N2*sum(p_k2 * (1-p_k2))

    where N1 is number of points in data1
    p_k1 is fraction of points that have y value of k in data1
    same for N2 and p_k2


    :param data1: A 2D python list
    :param data2: A 2D python list
    :return: a number - gini_impurity 
    """

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
    """
        build_tree is a recursive function.
        What it does in the general case is:
        1: find the best feature and value of the feature to divide the data into
        two parts
        2: divide data into two parts with best feature, say data1 and data2
            recursively call build_tree on data1 and data2. this should give as two 
            trees say t1 and t2. Then the resulting tree should be 
            DecisionNode(...... true_branch=t1, false_branch=t2) 
    
        In case all the points in the data have same Y we should not split any more, and return that node
        For this function we will give you some of the code so its not too hard for you ;)
    
        :param data: param data: A 2D python list
        :param current_depth: an integer. This is used if we want to limit the numbr of layers in the
            tree
        :param max_depth: an integer - the maximal depth of the representing
        :return: an object of class DecisionNode

    """

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
    """
    DecisionTree class, that represents one Decision Tree

    :param max_tree_depth: maximum depth for this tree.
    """

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
    '''
    Test our data 'a' on 'tree' decision tree
    :param tree: A class DecisionNode
    :param a: Dataset
    :return: Result
    '''
    if tree.is_leaf == True:
        return tree.results

    if a[tree.column] >= tree.value:
        return test(tree.true_branch, a)
    else:
        return test(tree.false_branch, a)

