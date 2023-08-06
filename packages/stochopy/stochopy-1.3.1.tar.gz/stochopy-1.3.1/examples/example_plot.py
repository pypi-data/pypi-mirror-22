# -*- coding: utf-8 -*-

"""
This example shows how to compute a traveltime grid using an Eikonal solver
and to plot it.

Author: Keurfon Luu <keurfon.luu@mines-paristech.fr>
License: MIT
"""

import sys
sys.path.append("../")
import matplotlib.pyplot as plt
try:
    from stochopy import Evolutionary, BenchmarkFunction
except ImportError:
    import sys
    sys.path.append("../")
    from stochopy import Evolutionary, BenchmarkFunction


if __name__ == "__main__":
    # Parameters
    func = "rastrigin"
    
    # Initialize function
    bf = BenchmarkFunction(func, n_dim = 2)
    
    # Initialize solver
    ea = Evolutionary(**bf.get(), popsize = 5, max_iter = 200)
    
    # Solve
    xopt, gfit = ea.optimize(solver = "cpso", snap = True)
    
    # Plot in 3D
    ax1 = bf.plot(figsize = (8, 6), projection = "3d")
    ax1.view_init(azim = -45, elev = 74)
    plt.show()
    
    # Save figure
    plt.savefig("%s.png" % func)