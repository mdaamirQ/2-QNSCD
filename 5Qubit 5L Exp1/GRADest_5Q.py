"""
Gradient Estimation
@author: mdaamirsohail
"""
import pennylane as qml
import scipy
from model_5qubit import *
from globalVars import *
from pennylane import numpy as np

### Gradient Estimation Device
'wires = nqubits + 1 ancilla qubit'
'shots = 1: to get measurement outcome'
devGrad = qml.device('lightning.qubit',wires = nqubits+1,shots = 1)

@qml.qnode(devGrad,interface='autograd')
def EstGrad(params,state,paramIdx):
    
    qml.QubitStateVector(state,wires=list(range(nqubits)))
    qml.Hadamard(wires = nqubits)
    
    lIdx, qIdx = divmod(paramIdx,nqubits)
   
    for iLayer in range(nlayers):
        if iLayer == lIdx:
            pIdx = sigma[qIdx,lIdx]
            
            # if qIdx == 0: V_op = pauli_op[str(pIdx)]
            # else: V_op = pI
            # for i_kron in range(1,nqubits):
            #     if qIdx == i_kron: temp = pauli_op[str(pIdx)]
            #     else: temp = pI

            #     V_op = np.kron(V_op,temp)
            V = V_dict[str(qIdx)+str(pIdx)]
            
            V = np.kron(scipy.linalg.expm(1j*np.pi*V/4),rho0) + np.kron(scipy.linalg.expm(-1j*np.pi*V/4),rho1)   
            V.requires_grad = False
            qml.QubitUnitary(V,wires=list(range(nqubits+1)))
            
        if iLayer == 0:
            ### QNN Layer - 1
            QNN_layer1(params)
        if iLayer == 1:
            ### QNN Layer - 2
            QNN_layer2(params)
        if iLayer == 2:
            ### QNN Layer - 3
            QNN_layer3(params)
        if iLayer == 3:
            ### QNN Layer - 4
            QNN_layer4(params)
        if iLayer == 4:
            ### QNN Layer - 5
            QNN_layer5(params)
        if iLayer == 5:
            ### QNN Layer - 6
            QNN_layer6(params)
    
    
    return qml.sample(op=qml.Hermitian(M,wires=list(range(nqubits)))),qml.sample(qml.PauliZ(nqubits))
