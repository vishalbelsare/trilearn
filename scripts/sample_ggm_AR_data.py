import json

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import networkx as nx
from networkx.readwrite import json_graph

import chordal_learning.graph.graph as glib
import chordal_learning.distributions.g_intra_class as gic


matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.unicode'] = True
matplotlib.rc('xtick', labelsize=8)
matplotlib.rc('ytick', labelsize=8)


def main(n_dim, n_samples, correlation, variance, max_bandwidth,
         graph_filename, output_directory, seed):
    if seed:
        np.random.seed(seed)
    adjmat = np.zeros(n_dim*n_dim, dtype=int).reshape((n_dim, n_dim))
    bandwidth = 1
    s2 = variance
    rho = correlation
    for i in range(n_dim):
        b = np.random.choice([-1, 0, 1], 1, p=np.array([1, 1, 1])/3.0)[0]
        bandwidth = max(bandwidth + b, 1)
        bandwidth = min(bandwidth, n_dim - i - 1)
        bandwidth = min(bandwidth, max_bandwidth)

        for j in range(bandwidth):
            adjmat[i, i + j + 1] = 1
            adjmat[i + j + 1, i] = 1

    graph = nx.from_numpy_matrix(adjmat)
    directory = output_directory

    graph_filename_json = directory+"/AR1-"+str(max_bandwidth)+"_p_"+str(n_dim)+".json"

    with open(graph_filename_json, 'w') as outfile:
        js_graph = json_graph.node_link_data(graph)
        json.dump(js_graph, outfile)

    for node in graph.nodes():
        graph.node[node] = {"label": node+1}


    graph_filename_plot = directory+"/AR1-"+str(max_bandwidth)+"_p_"+str(n_dim)+".eps"
    glib.plot(graph, graph_filename_plot,
              layout="fdp")

    graph_filename_adjmat_plot = directory+"/AR1-"+str(max_bandwidth)+"_p_"+str(n_dim)+"_adjmat.eps"

    plt.clf()
    mask = np.zeros_like(adjmat)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        sns.heatmap(adjmat, mask=mask, annot=False,
                    cmap="Blues",
                    xticklabels=range(1, n_dim+1),
                    yticklabels=range(1, n_dim+1),
                    vmin=0.0, vmax=1.0, square=True,
                    cbar=False)
        plt.xticks(rotation=90)
        plt.yticks(rotation=0)
        plt.savefig(graph_filename_adjmat_plot,
                    format="eps", bbox_inches='tight', dpi=300)

    c = gic.cov_matrix(graph, rho, s2)
    X = np.random.multivariate_normal(np.zeros(n_dim), c, n_samples)

    data_filename = directory+"/AR1-"+str(max_bandwidth)+"_p_"+str(n_dim)+"_sigma2_"+str(s2) + \
                    "_rho_"+str(rho)+"_n_"+str(n_samples)+".csv"
    np.savetxt(data_filename, X, delimiter=',')

    precmat_filename = directory+"/AR1-"+str(max_bandwidth)+"_p_"+str(n_dim)+"_sigma2_"+str(s2) + \
                       "_rho_"+str(rho)+"_omega.txt"
    np.savetxt(precmat_filename, c.I, delimiter=',')


    precmat_filename_plot = directory+"/AR1-"+str(max_bandwidth)+"_p_"+str(n_dim) + \
                            "_sigma2_"+str(s2) + \
                            "_rho_"+str(rho)+"_omega.eps"
    plt.clf()
    mask = np.zeros_like(c.I)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        sns.heatmap(c.I, mask=mask, annot=False,
                    cmap="Blues",
                    xticklabels=range(1, n_dim+1),
                    yticklabels=range(1, n_dim+1),
                    vmin=0.0, vmax=1.0, square=True,
                    cbar=False)
        plt.xticks(rotation=90)
        plt.yticks(rotation=0)
        plt.savefig(precmat_filename_plot,
                    format="eps", bbox_inches='tight', dpi=300)

    print "wrote files"
    print graph_filename_json + "\n" + \
          graph_filename_plot + "\n" + \
          graph_filename_adjmat_plot + "\n" + \
          data_filename + "\n" +\
          precmat_filename + "\n" + \
          precmat_filename_plot
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Samples a graph intra-class model with randomly varying bandwidth. "
                                                 "Samples data from the same model.")
    parser.add_argument(
        '-p', '--n_dim',
        type=int, required=True,
        help="The sample dimension"
    )
    parser.add_argument(
        '-n', '--n_samples',
        type=int, required=True,
        help="Number of samples"
    )
    parser.add_argument(
        '-r', '--correlation',
        type=float, required=True,
        help="Correlation coefficient"
    )
    parser.add_argument(
        '-v', '--variance',
        type=float, required=True,
        help="Variance"
    )
    parser.add_argument(
        '-g', '--graph_filename',
        required=False,
        help="Graph filename"
    )
    parser.add_argument(
        '-b', '--max_bandwidth',
        required=True, type=int,
        help="Maximum bandwidth"
    )
    parser.add_argument(
        '-o', '--output_directory',
        required=False,
        default="."
    )
    parser.add_argument(
        '-s', '--seed',
        type=int, required=False, default=None
    )

    args = parser.parse_args()
    main(**args.__dict__)