import numpy as np
import math
import random


def sigmoid(s):
    return 1/(1+math.exp(-s))


def normalized_gradient(X, Y, Xnorms, beta):
    '''
    Calculate gradient of sigmoid Log Loss Function
    :param X: 1d array. Features with ones
    :param Y: scalar integer. Labels (-1,1)
    :param Xnorms: 1d array. Mean values of features by columns
    :param beta: 1d array. Weights
    :return: 1d array
    '''

    X=np.array(X)

    grad = Y*X * (1-sigmoid(Y*(beta.T.dot(X))))/Xnorms

    return grad


def gradient_descent(X, Y, max_steps=20):
    '''
    Make stochastic gradient descend
    :param X: 2d array. Features withowt ones
    :param Y: 1d array. Labels (-1,1)
    :param max_steps: Integer. namber of listing whole data
    :return: 1d array. Weights
    '''
    X=np.array(X)
    X=np.column_stack((np.ones(X.shape[0]),X))

    def norm(a):
        a=np.array(a)
        return math.sqrt(a.T.dot(a))

    def Xnorm(a):  #a is an m*n matrix, return is nD vector where element 'i' is the average of all m elements in 'i'th column
        a=np.array(a)
        norms=np.zeros(a.shape[1])
        if len(a.shape) != 1:
            for i in range(a.shape[1]):
                norms[i] = np.sum([a[j,i] for j in range(a.shape[0])])/a.shape[0]
        else:
            for i in range(a.shape[1]):
                norms[i] = a[i]
        return norms

    
    
    for i in range(len(Y)):
        if Y[i]==0:
            Y[i]=-1
    X = np.array(X)
    Xnorms=Xnorm(X)

    beta = np.zeros(X.shape[1])
    for s in range(max_steps):
        r = list(range(X.shape[0] - 1))
        random.shuffle(r)
        for f in r:
            grad=normalized_gradient(X[f], Y[f],Xnorms, beta)
            beta = beta + grad/(X.shape[0]*0.5)

    return beta
