from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

class HazardBayesianNetwork:
    def __init__(self):
        # Directed Acyclic Graph structure:
        # Weather -> LandslideRisk -> RoadClosure
        # TrafficCongestion -> RoadClosure
        self.model = DiscreteBayesianNetwork([
            ('WeatherSeverity', 'HazardRisk'),
            ('HazardRisk', 'RoadClosure'),
            ('TrafficCongestion', 'RoadClosure')
        ])
        self._build_cpds()
        self.infer = VariableElimination(self.model)

    def _build_cpds(self):
        # Weather: 0 = Clear, 1 = Severe Storm
        cpd_weather = TabularCPD(
            variable='WeatherSeverity', variable_card=2,
            values=[[0.75], [0.25]]
        )

        # Traffic: 0 = Low, 1 = Gridlock
        cpd_traffic = TabularCPD(
            variable='TrafficCongestion', variable_card=2,
            values=[[0.70], [0.30]]
        )

        # HazardRisk conditioned on Weather
        cpd_hazard = TabularCPD(
            variable='HazardRisk', variable_card=2,
            values=[[0.90, 0.20],   # Normal
                    [0.10, 0.80]],  # High hazard probability
            evidence=['WeatherSeverity'], evidence_card=[2]
        )

        # RoadClosure conditioned on HazardRisk and TrafficCongestion
        cpd_closure = TabularCPD(
            variable='RoadClosure', variable_card=2,
            values=[
                # High Hazard: [Low, High], Normal Hazard: [Low, High]
                [0.98, 0.70, 0.40, 0.05],  # P(Open)
                [0.02, 0.30, 0.60, 0.95]   # P(Blocked)
            ],
            evidence=['HazardRisk', 'TrafficCongestion'],
            evidence_card=[2, 2]
        )

        self.model.add_cpds(cpd_weather, cpd_traffic, cpd_hazard, cpd_closure)
        assert self.model.check_model()

    def query_closure_risk(self, weather_level: int, traffic_level: int) -> float:
        """Infers the marginal probability that a road is blocked."""
        result = self.infer.query(
            variables=['RoadClosure'],
            evidence={'WeatherSeverity': weather_level, 'TrafficCongestion': traffic_level},
            show_progress=False
        )
        # Returns P(RoadClosure = 1)
        return float(result.values[1])