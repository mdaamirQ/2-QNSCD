"""
Model parameters
@author: mdaamirsohail
"""
import pennylane as qml
from pennylane import numpy as np
###############################################################
'Model properties'
nqubits = 3
dim = 2**nqubits
nlayers = 3
nparams = nqubits*nlayers
###############################################################
'Measurement operators'
M_p1 = np.zeros((dim,dim))
M_m1 = np.zeros((dim,dim))

for M_idx in range(dim): 
    binary_str = bin(M_idx)[2:].zfill(nqubits) # creates a binary string of length nqubits
    if binary_str.count('1') % 2 == 0:  # Check if the number of 1's is even
        M_p1[M_idx,M_idx] = 1
    else: 
        M_m1[M_idx,M_idx] = 1
    # if M_idx % 2 == 0:  
    #     M_p1[M_idx,M_idx] = 1
    # else: 
    #     M_m1[M_idx,M_idx] = 1


'Measurement Observable'
M = M_p1 - M_m1
###############################################################
'Quantum Neural Network'
'Notation: X-gate = 0, Y-gate = 1, Z-gate = 2'
sigma = np.array([[1,1,1],\
                  [1,1,1],\
                  [1,1,1]], requires_grad = False)

def QNN_layer1(params):
    # U1(theta0, theta1): Parametrized layer 1
    qml.RY(params[0], wires=0)
    qml.RY(params[1], wires=1)
    qml.RY(params[2], wires=2)
    # V1: non-parametrized gates
    qml.CNOT(wires=[0, 1])
    qml.CNOT(wires=[1, 2])

def QNN_layer2(params):
    # U2(theta2, theta3): Parametrized layer 2
    qml.RY(params[3], wires=0)
    qml.RY(params[4], wires=1)
    qml.RY(params[5], wires=2)
    # V2: non-parametrized gates
    qml.CNOT(wires=[0, 1])
    qml.CNOT(wires=[1, 2])

def QNN_layer3(params):
    # U3(theta4, theta5): Parametrized layer 4
    qml.RY(params[6], wires=0)
    qml.RY(params[7], wires=1)
    qml.RY(params[8], wires=2)
    # V3: non-parametrized gates
    qml.CNOT(wires=[0, 1])
    qml.CNOT(wires=[1, 2])
    
def QNN(params,state): 
    qml.QubitStateVector(state, wires = list(range(nqubits))) 
    QNN_layer1(params)
    QNN_layer2(params)
    QNN_layer3(params)

###############################################################
'Binary Loss Function'
def loss(y,yhat):
    if y == yhat:
        return 0
    else:
        return 1
###############################################################
'Per-Sample Expected Loss'
# Measurement operators
obsM_p1 = qml.Hermitian(M_p1,wires = list(range(nqubits))) 
obsM_m1 = qml.Hermitian(M_m1,wires = list(range(nqubits))) 

opt_dev = qml.device("lightning.qubit",wires=nqubits)
@qml.qnode(opt_dev,interface = 'autograd')
def Meas_p1(params,state):
    QNN(params,state)
    return qml.expval(obsM_p1)

@qml.qnode(opt_dev,interface = 'autograd')
def Meas_m1(params,state):
    QNN(params,state)
    return qml.expval(obsM_m1)

def ps_expLoss(params,state,label):
    loss_p1 = loss(label,+1)
    loss_m1 = loss(label,-1)
    
    Prob_p1 = Meas_p1(params,state)
    Prob_m2 = Meas_m1(params,state)
    
    expLoss = loss_p1*Prob_p1 + loss_m1*Prob_m2
    return expLoss
    
# random_state = np.random.rand(dim)
# random_state = random_state /np.linalg.norm(random_state)
# qml.draw_mpl(QNN)(np.zeros(nparams),random_state)