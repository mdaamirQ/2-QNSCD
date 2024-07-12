"""
Model parameters
@author: mdaamirsohail
"""
import pennylane as qml
from pennylane import numpy as np

'Model properties'
nqubits = 6
dim = 2**nqubits
nlayers = 8
nparams = nqubits*nlayers

'Measurement operators'
M_p1 = np.zeros((dim,dim))
M_m1 = np.zeros((dim,dim))

for M_idx in range(dim): 
    # binary_str = bin(M_idx)[2:].zfill(nqubits) # creates a binary string of length nqubits
    # if binary_str.count('1') % 2 == 0:  # Check if the number of 1's is even
    #     M_p1[M_idx,M_idx] = 1
    # else: 
    #     M_m1[M_idx,M_idx] = 1
    if M_idx % 2 == 0:  
        M_p1[M_idx,M_idx] = 1
    else: 
        M_m1[M_idx,M_idx] = 1


'Measurement Observable'
M = M_p1 - M_m1

'Quantum Neural Network'
'Notation: X-gate = 0, Y-gate = 1, Z-gate = 2'
sigma = np.array([[1,2,1,2,1,2,1,2],\
                  [1,2,1,2,1,2,1,2],\
                  [1,2,1,2,1,2,1,2],\
                  [1,2,1,2,1,2,1,2],\
                  [1,2,1,2,1,2,1,2],\
                  [1,2,1,2,1,2,1,2],\
                  [1,2,1,2,1,2,1,2],\
                  [1,2,1,2,1,2,1,2],\
                  [1,2,1,2,1,2,1,2],\
                  [1,2,1,2,1,2,1,2]], requires_grad = False)

def QNN_layer1(params):
    for itr in range(nqubits):
        qml.RY(params[itr], wires=itr)
    
def QNN_layer2(params):
    for itr in range(nqubits):
        qml.RZ(params[itr+nqubits], wires=itr)
            
def QNN_layer3(params):
    for itr in range(nqubits):
        qml.RY(params[itr+2*nqubits], wires=itr)
        
def QNN_layer4(params):
    for itr in range(nqubits):
        qml.RZ(params[itr+3*nqubits], wires=itr)
        
    qml.CNOT(wires=[0, 1])
    qml.CNOT(wires=[2, 3])
    qml.CNOT(wires=[4, 5])    
    qml.CNOT(wires=[1, 2])
    qml.CNOT(wires=[3, 4])
    qml.CNOT(wires=[5, 0])
    
def QNN_layer5(params):
    # U2(theta2, theta3): Parametrized layer 2
    for itr in range(nqubits):
        qml.RY(params[itr+4*nqubits], wires=itr)
    
def QNN_layer6(params):
    for itr in range(nqubits):
        qml.RZ(params[itr+5*nqubits], wires=itr)

def QNN_layer7(params):
    # U2(theta2, theta3): Parametrized layer 2
    for itr in range(nqubits):
        qml.RY(params[itr+6*nqubits], wires=itr)

def QNN_layer8(params):
    # U2(theta2, theta3): Parametrized layer 2
    for itr in range(nqubits):
        qml.RZ(params[itr+7*nqubits], wires=itr)
    
def QNN(params,state): 
    qml.QubitStateVector(state, wires = list(range(nqubits))) 
    QNN_layer1(params)
    QNN_layer2(params)
    QNN_layer3(params)
    QNN_layer4(params)
    QNN_layer5(params)
    QNN_layer6(params)
    QNN_layer7(params)
    QNN_layer8(params)

'Binary Loss Function'
def loss(y,yhat):
    if y == yhat:
        return 0
    else:
        return 1

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