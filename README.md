# Dynamic Coverage Control for Port Area Surveillance

[![Thesis PDF](https://img.shields.io/badge/Thesis-PDF-red.svg)](TESI_REPORT/Tesi_Necerini_Ivan.pdf)

## Overview

This repository contains the implementation and experimental results of my bachelor's thesis on **Dynamic Coverage Control** for autonomous agent coordination in port area surveillance. The project addresses the challenge of optimizing multiple drone agents to effectively monitor moving maritime targets (vessels) within a defined surveillance area.

The work implements three progressive algorithm versions that improve coverage performance through gradient ascent optimization, Brownian motion, and repulsive potential fields to prevent agent clustering.

## Problem Statement

The core objective is to maximize the **total coverage index** of moving targets by dynamically positioning autonomous agents (drones) in a 2D surveillance area. Each agent has:
- A limited sensing radius `r`
- Peak sensing quality `mp` that decreases with distance
- The ability to move based on gradient calculations

Key challenges include:
- Maintaining minimum coverage thresholds for all targets
- Adapting to dynamic target trajectories
- Preventing agent collisions and clustering
- Optimizing computational efficiency for real-time applications

## Methodology

### Coverage Index Calculation

For each target `j` and agent `i`, the coverage index at time `t` is:

$$E_{ij}(t) = \begin{cases} 
\frac{m_p}{r^4} \cdot (d_{ij}^2 - r^2)^2 & \text{if } d_{ij} \leq r \\
0 & \text{otherwise}
\end{cases}$$

where $d_{ij}$ is the Euclidean distance between agent `i` and target `j`.

The total coverage index incorporates a sigmoid function to enforce minimum coverage requirements:

$$E(t) = \sum_{j=1}^{N} \frac{\tanh(E_j(t) - E^*) + 1}{2}$$

### Algorithm Versions

#### Version 1: Gradient Ascent
Basic implementation using finite difference method to compute gradients:

```
p_i(t+1) = p_i(t) + ε · ∇E(t)
```

- **ε**: Step size parameter controlling agent velocity
- **∇E(t)**: Gradient of total coverage index w.r.t. agent positions

#### Version 2: Brownian Motion
Adds stochastic exploration to avoid local optima:

```
p_i(t+1) = p_i(t) + ε · ∇E(t) + m_i(t)
```

- **m_i(t)**: Brownian motion term with Gaussian distribution N(0, σ²)

#### Version 3: Repulsive Potential
Introduces inter-agent repulsion to distribute agents optimally:

```
p_i(t+1) = p_i(t) + ε · ∇E(t) + η_i(t)
```

- **η_i(t)**: Repulsive potential preventing agents from clustering
- **δ**: Minimum safe distance between agents

## Repository Structure

```
.
├── main.py                          # Main execution script
├── gradient.py                      # Gradient computation (finite differences)
├── coverageIndices.py               # Coverage metrics calculation
├── initialCoverageIndices.py        # Initial state coverage evaluation
├── createTheSetOfAgents.py          # Agent initialization and positioning
├── createTheSetOfTargets.py         # Target trajectory generation from dataset
├── plotMergeFunctions.py            # Visualization utilities
├── testTotalCoverageIndex.py        # Performance analysis tools
├── dataset.pkl                      # Maritime trajectory dataset
├── v1/
│   └── coverageAlgorithmV1.py       # Version 1: Basic gradient ascent
├── v2/
│   ├── coverageAlgorithmV2.py       # Version 2: With Brownian motion
│   └── brownianMotion.py            # Stochastic motion generation
├── v3/
│   ├── coverageAlgorithmV3.py       # Version 3: With repulsive potential
│   └── repulsivePotential.py        # Inter-agent repulsion computation
├── Images/                          # Generated plots and visualizations
└── TESI_REPORT/                     # Thesis document and LaTeX sources
```

## Installation

### Prerequisites

- Python 3.8+
- NumPy
- PyTorch
- Matplotlib

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/Dynamic_Coverage_Control_Area_Portuale_Tesi_Necerini.git
cd Dynamic_Coverage_Control_Area_Portuale_Tesi_Necerini

# Install dependencies
pip install numpy torch matplotlib
```

## Usage

### Basic Execution

Run the main simulation with default parameters:

```bash
python main.py
```

### Configuration Parameters

Key parameters can be modified in [main.py](main.py):

| Parameter | Default | Description |
|-----------|---------|-------------|
| `numTargets` | 10 | Number of vessel trajectories to track |
| `numAgents` | 4 | Number of drone agents |
| `duration` | 150 | Simulation duration (seconds) |
| `r` | 150 | Agent sensing radius |
| `mp` | 1 | Peak sensing quality |
| `epsilon` | 150 | Gradient ascent step size |
| `lowerboundIndex` | 1 | Minimum acceptable coverage (E*) |
| `delta` | 30 | Minimum inter-agent distance (V3) |
| `h` | 1e-10 | Finite difference sensitivity |

### Output

The simulation generates:
- **Console Output**: Coverage indices at t=0 and t=final for each version
- **Visualizations** (saved in `Images/`):
  - `selectedTrajectories.png`: Input target trajectories
  - `initialAgentPositions.png`: Initial drone positions
  - `trajectoriesWithAgentStartPoints.png`: Combined view
  - `finalTrajectoriesV1.png`, `V2`, `V3`: Algorithm results
  - `V1_totalCoverageIndexOverTime.png`: Performance evolution
  - `finalSetWithRadius.png`: Final configuration with sensing radii

## Results

Experimental results demonstrate:

1. **Version 1**: Baseline performance with consistent coverage improvement
2. **Version 2**: Enhanced exploration in complex scenarios but increased variability
3. **Version 3**: Best overall performance with optimal agent distribution and collision avoidance

All versions successfully maintain coverage indices above the minimum threshold E* = 1.0 for the majority of targets.

## Theoretical Background

This work builds upon:
- **Multi-agent coordination theory**
- **Coverage control optimization** (Cortes et al.)
- **Gradient-based control** for autonomous systems
- **Potential field methods** in robotics

Key references available in the [thesis document](TESI_REPORT/Tesi_Necerini_Ivan.pdf).

## Future Work

- Real-time implementation on embedded systems
- Integration with actual UAV platforms
- Adaptive parameter tuning using machine learning
- Extension to 3D surveillance scenarios
- Obstacle avoidance in complex environments

## Author

**Ivan Necerini**  
Bachelor's Thesis in Control Engineering  
University of Florence, 2024

## License

This project is part of academic research. For usage inquiries, please contact the author.

---

*For detailed mathematical formulations, experimental results, and complete analysis, please refer to the [full thesis document](TESI_REPORT/Tesi_Necerini_Ivan.pdf).*
