# 2-QNSCD

## Supervised learning from quantum data using quantum natural stochastic pairwise coordinate descent (2-QNSCD) optimization algorithm.

**Authors:** Mohammad Aamir Sohail, Mohsen Heidari Khoozani, S. Sandeep Pradhan  
Journal: [npj Quantum Information](https://www.nature.com/articles/s41534-025-01047-4)

Date: July 2024 

arXiv ID: [2407.13858](https://arxiv.org/abs/2407.13858) (see arXiv for version details)

---

## Overview

This paper introduces a novel framework for optimizing variational quantum circuits by harnessing the intrinsic geometry of quantum state space. At its core, the work defines an ensemble-based quantum Fisher information metric (E-QFIM) that quantifies the sensitivity of a parameterized quantum circuit to changes in its parameters—without the need for full-state tomography. Leveraging this metric, the authors develop the Quantum Natural Stochastic Pairwise Coordinate Descent (2-QNSCD) algorithm, which updates only two randomly selected parameters per iteration using a sparse and unbiased estimator of the metric tensor. This approach dramatically reduces both the measurement overhead and computational cost typically associated with gradient-based methods for learning from quantum data.

The paper provides rigorous theoretical guarantees, including exponential convergence under mild assumptions, and demonstrates through extensive numerical experiments (e.g., on binary classification tasks) that 2-QNSCD converges faster compared to standard randomized stochastic gradient descent. 

<details>
  <summary> Major Contributions</summary>

- **Ensemble-Based Quantum Metric (E-QFIM):**  
  Introduces a new metric that measures the closeness between ensembles of pure states. This metric can be efficiently estimated without full tomography, overcoming the limitations of the Bures metric.

- **Sparse, Unbiased Estimator:**  
  Develop an efficient sequential measurement strategy using mid-circuit measurements to obtain a highly sparse and unbiased estimator of the E-QFIM. Only a constant number of measurements are needed per iteration.

- **Quantum Natural Stochastic Pairwise Coordinate Descent (2-QNSCD):**  
  Presents an optimization algorithm that updates only two randomly chosen parameters per iteration. This results in constant sample complexity and computational cost per iteration without requiring multiple copies of the quantum data.

- **Exponential Convergence Guarantee:**  
  Provides a theoretical analysis showing that 2-QNSCD achieves an exponential rate of convergence under mild assumptions. A new quadratic geometric information (QGI) inequality is introduced to generalize classical convergence criteria.

- **Empirical Validation:**  
  Demonstrates through experiments on a binary classification task that 2-QNSCD converges faster and more reliably than standard stochastic gradient descent, highlighting its robustness and data efficiency.


</details>

<details>
  <summary> Paper Structure</summary>

1. **Introduction:**  
   The motivation behind the method, challenges of variational quantum circuit optimization, and limitations of standard gradient descent methods.

2. **Background and Preliminaries:**  
   Overview of variational quantum algorithms, quantum state geometry (quantum geometric tensor, Fubini–Study metric), and existing optimization methods.

3. **The 2-QNSCD Algorithm:**  
   Detailed description of the algorithm’s design, update rules, and construction of the sparse metric tensor estimator.

4. **Convergence Analysis:**  
   Theoretical analysis demonstrating faster convergence and complexity benefits over randomized stochastic gradient descent.

5. **Numerical Experiments:**  
   Simulation results show faster convergence for different system sizes and PQC models.

6. **Conclusion and Future Work:**  
   Summary of benefits and discussion of potential research directions.

</details>

---

## Repository Structure

This repository is organized to facilitate running experiments on variational quantum circuits. Each experimental folder follows the naming convention:

**XQubit YL ExpZ**  
- **X**: Number of qubits used in the experiment  
- **Y**: Number of layers in the Parameterized Quantum Circuit (PQC)  
- **Z**: Experiment identifier (e.g., different initializations or PQC structures)

Below is an example structure for an experimental folder along with the top-level organization:

### Navigation

1. **/data_generation/**  
   Run the Jupyter notebook to generate a synthetic dataset for both the learning and testing phases. 

2. **/XQubit YL ExpZ/**  
   This folder contains the main code for a specific experiment:
   - **XQubit YL ExpZ.ipynb:**  
     Main Jupyter Notebook file covering both the learning and testing phases.
   - **EQFIMest_XQ.py:**  
     Computes the EQFIM estimate for the PQC used.
   - **GRADest_XQ.py:**  
     Computes the gradient estimate for the PQC used.
   - **model_Xqubit.py:**  
     Specifies all model parameters, including the number of parameters, number of qubits, PQC structure, and measurement observables.
   - **globalVars.py:**  
     Defines global variables that are used consistently across all experiments.

3. **/Figs/**  
   Contains high-resolution figures and plots generated during the experiments.

4. **/Beta 3Qubit 3L/**
   Contains files for illustrating the performance of 2-QNSCD for different regularization parameters. 

## Installation

1. **Requirements:**  
   - Python 3.11+  
   - Quantum simulation libraries (e.g., Qiskit, PennyLane)  
   - Standard libraries: NumPy, SciPy, matplotlib

2. **Setup:**  
   Clone the repository and install dependencies:
   ```bash
   git clone https://github.com/mdaamirQ/2-QNSCD.git
   cd 2-QNSCD
   pip install -r requirements.txt

---


## Citation

If you use or refer to this work in your research, please cite it as follows:

```bibtex
@article{sohail2025quantum,
  title={Quantum natural stochastic pairwise coordinate descent},
  author={Sohail, Mohammad Aamir and Heidari, Mohsen and Pradhan, S Sandeep},
  journal={npj Quantum Information},
  volume={11},
  number={1},
  pages={109},
  year={2025},
  publisher={Nature Publishing Group UK London}
}
