import warnings
# 1. Suppress upstream third-party deprecation warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import pandas as pd
from tabulate import tabulate

from src.graph_engine import LogisticsGraph
from src.risk_model import HazardBayesianNetwork
from src.data_processor import LogisticsDataEngine
from src.dispatch_recommender import DispatchRecommender

def main():
    terminal_width = 80
    print("\n" + "=" * terminal_width)
    print(" 🚨 EMERGENCY LOGISTICS & SUPPLY CHAIN ROUTE OPTIMIZER")
    print("=" * terminal_width + "\n")

    # 1. Initialize Network Topology (Exp 1)
    nodes = ["Central_Hub", "Depot_North", "Depot_South", "Transit_Junction", "Field_Hospital"]
    network = LogisticsGraph()
    for n in nodes:
        network.add_node(n)

    edges = {
        ("Central_Hub", "Depot_North"): 45.0,
        ("Central_Hub", "Depot_South"): 35.0,
        ("Depot_North", "Transit_Junction"): 25.0,
        ("Depot_South", "Transit_Junction"): 40.0,
        ("Depot_North", "Field_Hospital"): 85.0,
        ("Transit_Junction", "Field_Hospital"): 30.0,
        ("Depot_South", "Field_Hospital"): 95.0,
    }

    for (u, v), dist in edges.items():
        network.add_edge(u, v, dist)

    # 2. Distance Matrix as a labeled DataFrame instead of a raw array (Exp 9)
    dist_matrix = LogisticsDataEngine.compute_distance_matrix(nodes, edges)
    # Shorten node labels for a clean, compact terminal print
    short_labels = ["Hub", "D_North", "D_South", "Transit", "Hospital"]
    dist_df = pd.DataFrame(dist_matrix, index=short_labels, columns=short_labels)

    print("┌── [1] PAIRWISE DISTANCE MATRIX (Exp 9 - NumPy/Pandas)")
    print(tabulate(dist_df, headers="keys", tablefmt="rounded_outline", floatfmt=".1f"))
    print()

    # 3. Path Discovery (Exp 4 & 5)
    start_node = "Central_Hub"
    target_node = "Field_Hospital"

    bfs_path = network.bfs_shortest_hops(start_node, target_node)
    all_candidate_paths = network.dfs_all_paths(start_node, target_node)

    print("┌── [2] GRAPH SEARCH & CONNECTIVITY (Exp 4 & Exp 5)")
    print(f"│ • BFS Hop-Optimal Route : {' ➔ '.join(bfs_path)} ({len(bfs_path)-1} hops)")
    print(f"│ • Total Detours Evaluated: {len(all_candidate_paths)} non-cyclic paths discovered via DFS")
    print("└" + "─" * 55 + "\n")

    # 4. Probabilistic Hazard Assessment (Exp 3)
    bayes_net = HazardBayesianNetwork()
    hazard_conditions = {
        ("Central_Hub", "Depot_North"): (0, 0),
        ("Central_Hub", "Depot_South"): (0, 0),
        ("Depot_North", "Transit_Junction"): (1, 1),
        ("Depot_South", "Transit_Junction"): (1, 0),
        ("Depot_North", "Field_Hospital"): (0, 0),
        ("Transit_Junction", "Field_Hospital"): (1, 1),
        ("Depot_South", "Field_Hospital"): (0, 1),
    }

    computed_segment_risks = {
        edge: bayes_net.query_closure_risk(w, t)
        for edge, (w, t) in hazard_conditions.items()
    }

    # 5. Recommendation & Ranking (Exp 14)
    recommender = DispatchRecommender(risk_weight=0.7, latency_weight=0.3)
    ranked_plans = recommender.evaluate_and_rank_routes(
        all_candidate_paths, edges, computed_segment_risks
    )

    # 6. Clean Table Formatting
    display_rows = []
    for rank, plan in enumerate(ranked_plans, start=1):
        # Shorten node names for readability in narrow terminals
        clean_path = (
            plan["path"]
            .replace("Central_Hub", "Hub")
            .replace("Depot_North", "D.North")
            .replace("Depot_South", "D.South")
            .replace("Transit_Junction", "Transit")
            .replace("Field_Hospital", "Hospital")
            .replace(" -> ", " ➔ ")
        )
        display_rows.append({
            "Rank": f"#{rank}",
            "Recommended Route": clean_path,
            "Hops": plan["hops"],
            "Distance": f"{plan['total_distance_km']:.0f} km",
            "Failure Risk": f"{plan['failure_risk'] * 100:.1f}%",
            "Reliability": f"{plan['reliability_score'] * 100:.1f}%",
            "Penalty Score": f"{plan['penalty_cost']:.3f}"
        })

    print("┌── [3] FINAL DISPATCH RECOMMENDATION RANKINGS (Exp 14)")
    print(tabulate(display_rows, headers="keys", tablefmt="rounded_outline", stralign="center"))
    print("\n✔ Optimization complete. Safest route selected based on risk vs. latency.\n")

if __name__ == "__main__":
    main()
