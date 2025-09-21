import math
import os
from dataclasses import dataclass
from typing import List, Tuple

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


@dataclass
class WSParams:
    num_nodes: int = 1000
    lattice_k: int = 10  # total degree in the initial ring (k neighbors in total)
    num_trials: int = 20
    p_values: np.ndarray = np.logspace(-4, 0, 20)


def compute_metrics_for_p(num_nodes: int, k_total_degree: int, p: float, num_trials: int) -> Tuple[float, float]:
    """
    Returns average characteristic path length L and average clustering coefficient C
    across num_trials Watts–Strogatz graphs with given parameters.

    networkx.watts_strogatz_graph expects k to be the total degree in the ring lattice,
    and it must be even. The original paper reports k = 10 (average degree per node).
    """
    if k_total_degree % 2 != 0:
        raise ValueError("k_total_degree must be even for watts_strogatz_graph")

    lengths: List[float] = []
    clusterings: List[float] = []

    for _ in range(num_trials):
        g = nx.watts_strogatz_graph(n=num_nodes, k=k_total_degree, p=p)

        # Characteristic path length: average shortest path length over the connected graph.
        # WS graphs at the parameters of interest are connected with high probability.
        if nx.is_connected(g):
            L = nx.average_shortest_path_length(g)
        else:
            # If disconnected (rare), fallback to the largest connected component.
            gcc = max((g.subgraph(c) for c in nx.connected_components(g)), key=len)
            L = nx.average_shortest_path_length(gcc)

        C = nx.average_clustering(g)

        lengths.append(L)
        clusterings.append(C)

    return float(np.mean(lengths)), float(np.mean(clusterings))


def run_experiment(params: WSParams, out_dir: str) -> pd.DataFrame:
    os.makedirs(out_dir, exist_ok=True)

    results = []

    # Compute baseline at p = 0 for normalization
    L0, C0 = compute_metrics_for_p(
        num_nodes=params.num_nodes, k_total_degree=params.lattice_k, p=0.0, num_trials=params.num_trials
    )

    for p in params.p_values:
        Lp, Cp = compute_metrics_for_p(
            num_nodes=params.num_nodes, k_total_degree=params.lattice_k, p=float(p), num_trials=params.num_trials
        )
        results.append({
            "p": float(p),
            "L": Lp,
            "C": Cp,
            "L_over_L0": Lp / L0,
            "C_over_C0": Cp / C0,
        })

    df = pd.DataFrame(results)

    csv_path = os.path.join(out_dir, "ws_results.csv")
    df.to_csv(csv_path, index=False)

    # Plot analogous to Watts–Strogatz Figure 2
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.semilogx(df["p"], df["L_over_L0"], "o", label="L(p) / L(0)")
    ax.semilogx(df["p"], df["C_over_C0"], "s", mfc="none", label="C(p) / C(0)")

    ax.set_xlabel("p")
    ax.set_ylim(0, 1.05)
    ax.set_xlim(min(params.p_values), 1)
    ax.legend()
    ax.set_title("Watts–Strogatz: normalized L and C vs p (n=1000, k=10)")
    fig.tight_layout()

    fig_path = os.path.join(out_dir, "ws_LC_vs_p.png")
    fig.savefig(fig_path, dpi=160)
    plt.close(fig)

    return df


def main() -> None:
    out_dir = os.path.join(os.path.dirname(__file__), "out")
    params = WSParams()
    run_experiment(params, out_dir)


if __name__ == "__main__":
    main()


