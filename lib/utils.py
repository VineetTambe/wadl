import numpy as np
# import numpy.random as rand
# import numpy.linalg as la



def l1(a, b):
    # returns the L1 norm of two vectors that are tuples
    return sum(abs((np.array(a) - np.array(b))))

def rot2D(theta):
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array([[c, -s],
                     [s, c]])

def array2ListTuples(A):
    R, C = A.shape
    return [tuple(A[i,:]) for i in range(R)]


def sub2ind(cord, grid):
    # returns the linear index on the square index
    return cord[0] + grid[0]*cord[1]


def ind2sub(idx, grid):
    # returns the coordinate from the linear index
    return np.unravel_index(idx, grid, order="F")
