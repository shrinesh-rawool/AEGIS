import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple

class LogisticsDataEngine:
    def __init__(self, routes_df: pd.DataFrame):
        self.df = routes_df

    @staticmethod
    def compute_distance_matrix(nodes: List[str], edges: Dict[Tuple[str, str], float]) -> np.ndarray:
        """Exp 9: NumPy 2D array representation of pairwise network distances."""
        n = len(nodes)
        node_to_idx = {name: i for i, name in enumerate(nodes)}
        matrix = np.full((n, n), np.inf)
        np.fill_diagonal(matrix, 0.0)

        for (u, v), dist in edges.items():
            if u in node_to_idx and v in node_to_idx:
                i, j = node_to_idx[u], node_to_idx[v]
                matrix[i, j] = dist
                matrix[j, i] = dist

        return matrix

    @staticmethod
    def calculate_travel_time_variance(samples: List[float]) -> Tuple[float, float]:
        """Exp 10: SciPy statistical confidence interval and dispersion metrics."""
        arr = np.array(samples)
        variance = float(stats.variation(arr))  # Coefficient of variation
        sem = float(stats.sem(arr)) if len(arr) > 1 else 0.0
        return variance, sem

    def build_shipment_summary(self, dispatch_manifest: List[dict]) -> pd.DataFrame:
        """Exp 11: Pandas operations for supply allocation records."""
        manifest_df = pd.DataFrame(dispatch_manifest)
        return manifest_df.sort_values(by="priority_score", ascending=False)