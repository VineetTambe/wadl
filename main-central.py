
import warnings as warn
import os
import sys
import time
# math
import numpy as np
import numpy.linalg as la
import numpy.random as rand
import cvxpy as cvx
from gurobipy import *
# plot
import matplotlib.pyplot as plt
# lib
from lib.agent import Agent
from lib.config import Config
# from lib.utils import *


def solve_oneshot(config):
    # make objects
    colors = ['b', 'g', 'r', 'm']
    agents = [Agent(id, config, color=color) for id, color in zip(range(1), colors)]

    # init optimization problem data
    obj = []
    cnts = []

    # fill problems
    for agent in agents:
        agent.stage(obj, cnts)

    prob = cvx.Problem(cvx.Minimize(cvx.sum(obj)), cnts)
    prob.solve(solver=cvx.GUROBI,
               verbose=True,
               MIPGap=5e-2,
               MIPGapAbs=5e-2)
    # print("solving")
    # prob.solve(solver=cvx.ECOS_BB,
    #            verbose=True,
    #            mi_max_iters=10,
    #            mi_abs_eps=1e-3,
    #            mi_rel_eps=1e-2)
    print(prob.status)

    # parse solutions
    for agent in agents:
        agent.makeTrajectory()


    return agents

def main(outdir):
    config = Config("small")
    # config.writeInfo(outdir)


    agents = solve_oneshot(config)

    fig, ax = plt.subplots()
    print("agents")
    for agent in agents:
        print(agent.trajectory)
        agent.plot(ax)

    plt.show()

    return 0

if __name__ == '__main__':
    outdir = "tests/test1"
    main(outdir)