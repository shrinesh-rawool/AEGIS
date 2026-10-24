from typing import List, Dict
import numpy as np

class DispatchRecommender:
    def __init__(self, risk_weight: float = 0.6, latency_weight: float = 0.4):
        self.w_risk = risk_weight
        self.w_dist = latency_weight

    def evaluate_and_rank_routes(
        self,
        candidate_paths: List[List[str]],
        edge_distances: Dict[tuple, float],
        segment_risks: Dict[tuple, float]
    ) -> List[Dict]:
        evaluations = []

        for path in candidate_paths:
            total_dist = 0.0
            survival_prob = 1.0  # Compound reliability: Product of (1 - P(Closure))

            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                dist = edge_distances.get((u, v), edge_distances.get((v, u), 50.0))
                risk = segment_risks.get((u, v), segment_risks.get((v, u), 0.05))

                total_dist += dist
                survival_prob *= (1.0 - risk)

            failure_prob = 1.0 - survival_prob
            evaluations.append({
                "path": " -> ".join(path),
                "hops": len(path) - 1,
                "total_distance_km": total_dist,
                "failure_risk": failure_prob,
                "reliability_score": survival_prob
            })

        if not evaluations:
            return []

        # Normalization
        max_dist = max(e["total_distance_km"] for e in evaluations) or 1.0
        
        for e in evaluations:
            normalized_dist = e["total_distance_km"] / max_dist
            # Utility penalty: Lower is better
            e["penalty_cost"] = (self.w_dist * normalized_dist) + (self.w_risk * e["failure_risk"])

        # Rank ascending by penalty cost
        return sorted(evaluations, key=lambda x: x["penalty_cost"])