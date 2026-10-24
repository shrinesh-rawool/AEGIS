# AEGIS

### Risk-Aware Emergency Logistics & Route Intelligence

**Delivering the safest route when every road matters.**

AEGIS (*Adaptive Emergency Guidance & Intelligent Routing System*) is a
decision-support prototype for emergency logistics. It models a road
network, estimates road-closure risk under uncertain weather and traffic
conditions, explores alternative routes, and ranks candidate delivery
routes using a configurable balance of distance and safety risk.

> **Project status:** Academic prototype / simulation-based decision
> support. Real-time weather feeds, live traffic ingestion, and
> operational deployment are not assumed unless separately integrated
> and validated.

------------------------------------------------------------------------

## Contents

-   [Why AEGIS?](#why-aegis)
-   [Core capabilities](#core-capabilities)
-   [How it works](#how-it-works)
-   [System architecture](#system-architecture)
-   [Route scoring model](#route-scoring-model)
-   [Technology stack](#technology-stack)
-   [Repository structure](#repository-structure)
-   [Getting started](#getting-started)
-   [Input data](#input-data)
-   [Example output](#example-output)
-   [Assumptions and limitations](#assumptions-and-limitations)
-   [Possible extensions](#possible-extensions)
-   [Academic lab integration](#academic-lab-integration)
-   [Contributing](#contributing)
-   [License](#license)

## Why AEGIS?

During floods, landslides, severe weather, and other emergencies, the
shortest road may not be the safest or most reliable one. A blocked
corridor can delay medical supplies, food, water, and other critical
deliveries.

Conventional shortest-path routing focuses primarily on distance or
travel cost. AEGIS explores a broader decision: **which available route
offers a useful trade-off between distance and the probability of
disruption?**

The prototype combines graph algorithms, Bayesian inference, numerical
processing, statistical summaries, and a multi-criteria recommender in
one Python pipeline.

## Core capabilities

-   **Road-network representation:** Model depots, hospitals,
    intersections, and other facilities as graph nodes connected by road
    segments.
-   **Breadth-First Search (BFS):** Find a minimum-hop path in an
    unweighted graph.
-   **Depth-First Search (DFS):** Explore cycle-free candidate paths and
    possible detours.
-   **Bayesian hazard inference:** Estimate road-closure probabilities
    from modeled weather and traffic evidence using `pgmpy`.
-   **Distance-matrix processing:** Use NumPy for pairwise
    coordinate-distance calculations and related matrix operations.
-   **Travel-time statistics:** Use SciPy and Pandas to summarize
    travel-time variation and route data.
-   **Risk-aware ranking:** Compare candidate routes using a
    configurable penalty that accounts for normalized distance and
    cumulative closure risk.
-   **Dispatch manifest:** Present route candidates and their scores in
    a tabular format to support human decision-making.

## How it works

1.  **Load the network.** Read node and road-segment data from the files
    in `data/`.
2.  **Build the graph.** Represent facilities as vertices and road
    corridors as edges.
3.  **Explore candidate paths.** Use BFS for minimum-hop reachability
    and DFS to enumerate cycle-free alternatives within the configured
    network.
4.  **Estimate segment risk.** Use the Bayesian model to infer the
    probability of closure given available weather and traffic evidence.
5.  **Analyze distances and latency.** Process coordinate distances and
    any available travel-time observations.
6.  **Score candidate routes.** Aggregate segment risks and combine
    route risk with normalized distance.
7.  **Generate a dispatch manifest.** Sort candidate routes by penalty,
    with lower scores representing better trade-offs under the
    configured weights.

## System architecture

``` mermaid
flowchart TD
    A[Network nodes and road segments] --> B[Graph Engine]
    A --> C[Data Processor]
    D[Weather and traffic evidence] --> E[Bayesian Hazard Model]
    B --> F[Candidate Routes]
    C --> F
    E --> G[Segment Closure Probabilities]
    F --> H[Dispatch Recommender]
    G --> H
    H --> I[Ranked Dispatch Manifest]
```

### Main components

  -----------------------------------------------------------------------
  Component                           Responsibility
  ----------------------------------- -----------------------------------
  Graph Engine                        Network representation, BFS
                                      traversal, and DFS path exploration

  Bayesian Hazard Model               Conditional probability
                                      distributions and closure-risk
                                      inference

  Data Processor                      Coordinate-distance matrices,
                                      travel-time statistics, and tabular
                                      data

  Dispatch Recommender                Route reliability, penalty
                                      calculation, and candidate ranking

  Pipeline (`main.py`)                Coordinates the processing stages
                                      and displays results
  -----------------------------------------------------------------------

## Route scoring model

For a route (R) containing road segments (e_1, e_2, `\ldots`{=tex},
e_k), let (p_i) be the estimated probability that segment (e_i) is
closed.

### Compound route reliability

Under the simplifying assumption that segment-closure events are
independent:

\[
`\operatorname{Reliability}`{=tex}(R)=`\prod`{=tex}\_{i=1}\^{k}(1-p_i)
\]

The corresponding route failure risk is:

\[
`\operatorname{FailureRisk}`{=tex}(R)=1-`\operatorname{Reliability}`{=tex}(R)
\]

This estimates the probability that at least one segment is closed under
the independence assumption. If segment risks are correlated, a richer
model is needed.

### Multi-criteria penalty

\[ `\operatorname{Penalty}`{=tex}(R)=
w\_{`\mathrm{dist}`{=tex}}`\frac{D(R)}{D_{\max}}`{=tex}+
w\_{`\mathrm{risk}`{=tex}}`\operatorname{FailureRisk}`{=tex}(R) \]

Where:

-   (D(R)) is the total distance of route (R).
-   (D\_{`\max`{=tex}}) is the normalization value used for
    candidate-route distances.
-   (w\_{`\mathrm{dist}`{=tex}}) is the distance weight.
-   (w\_{`\mathrm{risk}`{=tex}}) is the risk weight.

Lower penalty values indicate a better score under the selected weights.
The weights express the relative importance of distance and risk; they
should be chosen deliberately and tested against representative
scenarios.

**Important:** This is a decision-support score, not a guarantee that a
route is safe. A route with a high closure probability may need to be
excluded outright rather than merely penalized.

## Technology stack

  Technology    Purpose
  ------------- -------------------------------------------------------
  Python 3.9+   Main implementation language
  NumPy         Numerical and matrix operations
  Pandas        Tabular data processing and reports
  SciPy         Statistical calculations
  pgmpy         Bayesian network modeling and probabilistic inference
  CSV           Portable input data format

## Repository structure

``` text
aegis-emergency-routing/
├── data/
│   ├── network_nodes.csv
│   └── routes.csv
├── src/
│   ├── __init__.py
│   ├── graph_engine.py
│   ├── risk_model.py
│   ├── data_processor.py
│   └── dispatch_recommender.py
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Getting started

### Requirements

-   Python 3.9 or newer
-   `pip`
-   Git (for cloning the repository)

### 1. Clone the repository

Replace `<your-username>` with your GitHub username:

``` bash
git clone https://github.com/<your-username>/aegis-emergency-routing.git
cd aegis-emergency-routing
```

### 2. Create a virtual environment

**Linux / macOS**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows Command Prompt**

``` bat
py -m venv .venv
.venv\Scripts\activate
```

**Windows PowerShell**

``` powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

``` bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `requirements.txt` has not been created yet, a starting set of
dependencies is:

``` text
numpy
pandas
scipy
pgmpy
```

Pin and test compatible versions before publishing a reproducible
release.

### 4. Run the pipeline

``` bash
python main.py
```

The expected output depends on the implementation and input data. The
intended pipeline reports distance-matrix information, graph
reachability and candidate paths, inferred closure risks, and a
route-ranking manifest.

## Input data

The prototype expects CSV data under `data/`. Keep column names
consistent with the implementation in `src/`.

### `network_nodes.csv`

A typical node dataset may contain:

  -----------------------------------------------------------------------
  Field                               Description
  ----------------------------------- -----------------------------------
  `node_id`                           Unique identifier for a hub or
                                      intersection

  `name`                              Human-readable facility or node
                                      name

  `latitude`                          Latitude coordinate, if
                                      coordinate-based distances are used

  `longitude`                         Longitude coordinate, if
                                      coordinate-based distances are used

  `facility_type`                     Optional type, such as depot,
                                      hospital, or relief center
  -----------------------------------------------------------------------

### `routes.csv`

A typical road-segment dataset may contain:

  -----------------------------------------------------------------------
  Field                               Description
  ----------------------------------- -----------------------------------
  `source`                            Starting node identifier

  `target`                            Destination node identifier

  `distance`                          Segment distance in the chosen unit

  `travel_time`                       Optional observed or estimated
                                      travel time

  `weather_severity`                  Weather evidence/state used by the
                                      risk model, if represented per
                                      segment

  `traffic_congestion`                Traffic evidence/state used by the
                                      risk model, if represented per
                                      segment
  -----------------------------------------------------------------------

These are illustrative schemas, not a substitute for checking the actual
column names expected by the code. Update this section as the
implementation's data contract becomes fixed. Avoid including private or
sensitive infrastructure data in a public repository.

## Example output

The final manifest can be presented as a table with fields such as:

  -----------------------------------------------------------------------------------------------------------
            Rank Route                         Distance     Estimated failure risk                    Penalty
  -------------- ----------- -------------------------- -------------------------- --------------------------
               1 Hub A →       Implementation-dependent   Implementation-dependent   Implementation-dependent
                 Junction C                                                        
                 → Hospital                                                        
                 D                                                                 

               2 Hub A →       Implementation-dependent   Implementation-dependent   Implementation-dependent
                 Junction B                                                        
                 → Hospital                                                        
                 D                                                                 
  -----------------------------------------------------------------------------------------------------------

The values above are placeholders to illustrate the report format, not
measured results. Replace them with actual output from a reproducible
test run before adding screenshots or performance claims to the
repository.

## Assumptions and limitations

-   **Input quality matters:** Risk estimates are only as reliable as
    the probabilities, evidence, and input data supplied to the model.
-   **BFS minimizes hops, not distance:** BFS finds a minimum-edge-count
    path in an unweighted graph. It does not by itself find the
    shortest-distance or safest route.
-   **DFS can grow rapidly:** Enumerating all simple paths can become
    expensive as the network grows. Use path limits or pruning for
    larger graphs.
-   **Independence assumption:** Multiplying segment reliabilities
    assumes independent closure events. Shared weather systems and
    correlated failures can violate this assumption.
-   **Statistical scope:** Standard deviation, standard error, and other
    latency summaries require suitable travel-time observations. They do
    not automatically provide a calibrated prediction interval.
-   **Normalization and weights matter:** Route rankings can change when
    distance normalization or utility weights change.
-   **No guaranteed real-time data:** Live traffic, weather, road
    closures, and emergency-service feeds must be integrated and
    validated separately.
-   **Human oversight is required:** The system is an academic
    decision-support prototype, not a certified emergency dispatch
    platform. Verify routes with authoritative sources before real-world
    use.

## Possible extensions

-   Add live weather, traffic, and road-closure feeds with clear source
    timestamps.
-   Include road-capacity, vehicle constraints, delivery priority, and
    supply-demand data.
-   Add hard constraints for known closures and unsafe corridors.
-   Compare risk-aware rankings with shortest-distance and minimum-hop
    baselines.
-   Evaluate results on synthetic disaster scenarios and report
    reproducible metrics.
-   Add a map-based visualization and a dispatcher dashboard.
-   Model correlated segment failures and uncertainty in the input
    probabilities.
-   Add unit tests, input validation, logging, and a reproducible
    environment.

## Academic lab integration

AEGIS brings together concepts from Artificial Intelligence & Machine
Learning laboratory coursework:

  Experiment      Concept applied
  --------------- -----------------------------------------------------
  Experiment 1    State-space representation and graph modeling
  Experiment 3    Bayesian network construction and inference
  Experiment 4    Depth-First Search and cycle-aware path exploration
  Experiment 5    Breadth-First Search and minimum-hop traversal
  Experiment 9    NumPy operations and distance matrices
  Experiment 10   SciPy statistical analysis
  Experiment 11   Pandas data analysis and tabular reporting
  Experiment 14   AI recommendation and multi-criteria scoring

The implementation and report should describe only the experiments and
functionality actually completed in the repository.

## Contributing

Contributions and improvements are welcome.

1.  Fork the repository.
2.  Create a feature branch.
3.  Keep changes focused and document any new assumptions.
4.  Add or update tests where possible.
5.  Open a pull request with a clear summary of the change.

For changes to risk scoring, include a small reproducible example
explaining how the new behavior affects route rankings.

## License

No license has been specified yet. Add a `LICENSE` file before inviting
reuse or contributions, and choose a license that matches how you want
the project to be used.
