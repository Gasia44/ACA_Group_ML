import numpy as np
import math
import random


def sigmoid(s):
    return 1/(1+math.exp(-s))


def normalized_gradient(X, Y, Xnorms, beta, l):

    X=np.array(X)

    grad = np.zeros(X.size)
    for i in range(X.size):
        grad[i] = Y*X[i] * (1-sigmoid(Y*(beta.T.dot(X))))/Xnorms[i]

    return grad


def gradient_descent(X, Y, epsilon, l=1, step_size=1e-4, max_steps=100):
    
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
    for s in range(max_steps*10):
        r = list(range(X.shape[0] - 1))
        random.shuffle(r)
        for f in r:
            grad=normalized_gradient(X[f], Y[f],Xnorms, beta, l)
            beta[0] = beta[0] + grad[0]
            for i in range(1,X.shape[1]):
                beta[i] = beta[i] + (step_size) * grad[i] / X.shape[0]

    return beta
