# 2-QNSCD

## Supervised learning from quantum data using quantum natural stochastic pairwise coordinate descent (2-QNSCD) optimization algorithm.

**Authors:** Mohammad Aamir Sohail, Mohsen Heidari Khoozani, S. Sandeep Pradhan  
**arXiv ID:** [2407.13858](https://arxiv.org/abs/2407.13858)  
**Date:** July 2024 (see arXiv for version details)

---

## Overview

This paper introduces the **Quantum Natural Stochastic Pairwise Coordinate Descent (2-QNSCD)** optimization method, a novel algorithm for training parameterized quantum circuits within variational quantum algorithms (VQAs). Variational quantum algorithms are among the most promising approaches for near-term quantum computing, but standard gradient-based methods face challenges due to measurement noise and the no-cloning principle. This work addresses these issues by leveraging the natural geometry of quantum state space and updating only selected coordinate pairs in each iteration, thereby reducing computational overhead and sample complexity.


<details>
  <summary> Key Contributions</summary>

- **Novel Optimization Strategy:**  
  Introduces a quantum natural gradient method that exploits the curved geometry of the quantum state space via a novel ensemble-based quantum information metric tensor.

- **Pairwise Coordinate Updates:**  
  Instead of computing full gradients, the algorithm updates only a pair of coordinates per iteration, significantly reducing the computational and sampling burden.

- **Sparse Unbiased Estimator:**  
  Develops a highly sparse, unbiased estimator for the quantum metric tensor using a quantum circuit whose gate complexity is comparable (Θ(1) times) to that of the parameterized circuit. This approach relies on single-shot quantum measurements, avoiding the need for multiple copies of quantum data.

- **Theoretical & Numerical Validation:**  
  Provides rigorous exponential convergence guarantees and extensive numerical experiments that show improved convergence speed, robustness against measurement noise, and scalability to larger quantum systems.

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
   Run the jupyter notebook to generate a synthetic dataset for both the learning and testing phases. 

2. **/XQubit YL ExpZ/**  
   This folder contains the main code for a specific experiment:
   - **XQubit YL ExpZ.ipynb:**  
     Open this Jupyter Notebook to run the full experiment, covering both the learning and testing phases.
   - **EQFIMest_XQ.py:**  
     Computes the EQFIM estimate for the PQC used.
   - **GRADest_XQ.py:**  
     Computes the gradient estimate for the PQC used.
   - **model_Xqubit.py:**  
     Specifies all model parameters including the number of parameters, number of qubits, PQC structure, and measurement observables.
   - **globalVars.py:**  
     Contains global variables used consistently across all experiments.

3. **/Figs/**  
   Contains high-resolution figures and plots generated during the experiments.

4. **/Beta 3Qubit 3L/**
   Contains file for illustrating the performance of 2-QNSCD for different regularization parameters. 

---


## Citation

If you use or refer to this work in your research, please cite it as follows:

```bibtex
@article{sohail2024quantum,
  title={Quantum Natural Stochastic Pairwise Coordinate Descent},
  author={Sohail, Mohammad Aamir and Khoozani, Mohsen Heidari and Pradhan, S. Sandeep},
  journal={arXiv preprint arXiv:2407.13858},
  year={2024}
}
