import pandas as pd
from tabulate import tabulate

from src.graph_engine import LogisticsGraph
from src.risk_model import HazardBayesianNetwork
from src.data_processor import LogisticsDataEngine
from src.dispatch_recommender import DispatchRecommender

def main():
    print("=" * 65)
    print(" EMERGENCY LOGISTICS & SUPPLY CHAIN ROUTE OPTIMIZER")
    print("=" * 65)

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

    # 2. NumPy Distance Matrix (Exp 9)
    dist_matrix = LogisticsDataEngine.compute_distance_matrix(nodes, edges)
    print("\n[+] Pairwise Network Distance Matrix (Exp 9 - NumPy):")
    print(dist_matrix)

    # 3. Path Discovery via BFS & DFS (Exp 4 & 5)
    start_node = "Central_Hub"
    target_node = "Field_Hospital"

    bfs_path = network.bfs_shortest_hops(start_node, target_node)
    all_candidate_paths = network.dfs_all_paths(start_node, target_node)

    print(f"\n[+] BFS Hop-Optimal Route (Exp 5): {' -> '.join(bfs_path)}")
    print(f"[+] Total Non-Cyclic Alternate Routes Found (Exp 4 - DFS): {len(all_candidate_paths)}")

    # 4. Probabilistic Hazard Assessment (Exp 3 - Bayesian Net)
    bayes_net = HazardBayesianNetwork()
    
    # Environmental conditions: 0 = Low/Clear, 1 = High/Severe
    # Transit_Junction is currently experiencing severe weather and heavy traffic
    hazard_conditions = {
        ("Central_Hub", "Depot_North"): (0, 0),
        ("Central_Hub", "Depot_South"): (0, 0),
        ("Depot_North", "Transit_Junction"): (1, 1),  # High hazard profile
        ("Depot_South", "Transit_Junction"): (1, 0),
        ("Depot_North", "Field_Hospital"): (0, 0),
        ("Transit_Junction", "Field_Hospital"): (1, 1),
        ("Depot_South", "Field_Hospital"): (0, 1),
    }

    computed_segment_risks = {}
    for edge, (weather, traffic) in hazard_conditions.items():
        risk = bayes_net.query_closure_risk(weather, traffic)
        computed_segment_risks[edge] = risk

    # 5. Recommendation & Ranking (Exp 14)
    recommender = DispatchRecommender(risk_weight=0.7, latency_weight=0.3)
    ranked_plans = recommender.evaluate_and_rank_routes(
        all_candidate_paths, edges, computed_segment_risks
    )

    # 6. Tabular Delivery Manifest (Exp 11 - Pandas)
    results_df = pd.DataFrame(ranked_plans)
    print("\n[+] Final Route Recommendation Rankings (Exp 14 & Exp 11):")
    print(tabulate(results_df, headers="keys", tablefmt="fancy_grid", floatfmt=".4f"))

if __name__ == "__main__":
    main()