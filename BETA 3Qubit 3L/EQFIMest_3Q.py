"""
E-QFIM Estimation
@author: mdaamirsohail
"""
import pennylane as qml
import scipy
from model_3qubit import *
from globalVars import *
from pennylane import numpy as np

EQFIMdev = qml.device('lightning.qubit',wires=nqubits,shots=1)
EQFIMdev_state = qml.device('lightning.qubit',wires=nqubits,shots=None)

@qml.qnode(EQFIMdev_state,interface='autograd')
def state_priorMeas(params,state,paramIdx):
    qml.QubitStateVector(state, wires = list(range(nqubits))) 
    
    lIdx, qIdx = divmod(paramIdx,nqubits)
    
    for iLayer in range(nlayers):
        if iLayer == lIdx:
            return qml.state()
        
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
            ### QNN Layer - 3
            QNN_layer4(params)
        if iLayer == 4:
            ### QNN Layer - 3
            QNN_layer5(params)
    
@qml.qnode(EQFIMdev,interface='autograd')
def OpSample(params,state,paramIdx):
    qml.QubitStateVector(state, wires = list(range(nqubits))) 
    
    lIdx, qIdx = divmod(paramIdx,nqubits)
    
    for iLayer in range(nlayers):
        if iLayer == lIdx:
            pIdx = sigma[qIdx,lIdx]
            if pIdx == 0:
                return qml.sample(qml.PauliX(qIdx))
            if pIdx == 1:
                return qml.sample(qml.PauliY(qIdx))
            if pIdx == 2:
                return qml.sample(qml.PauliZ(qIdx))
        
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
            ### QNN Layer - 3
            QNN_layer4(params)
        if iLayer == 4:
            ### QNN Layer - 3
            QNN_layer5(params)
    
@qml.qnode(EQFIMdev,interface='autograd')
def Cond_OpSample(params,priorS,priorState,paramIdx):
    
    lIdx0, qIdx0 = divmod(paramIdx[0],nqubits)
    lIdx1, qIdx1 = divmod(paramIdx[1],nqubits)
    
    pIdx0 = sigma[qIdx0,lIdx0]
    pIdx1 = sigma[qIdx1,lIdx1]

    if priorS == +1: Proj_temp = Proj_dict_p1[str(qIdx0)+str(pIdx0)]
    if priorS == -1: Proj_temp = Proj_dict_m1[str(qIdx0)+str(pIdx0)]

    Proj_temp.requires_grad = False
    
    pm_state = np.matmul(Proj_temp,priorState)
    pm_state = pm_state/np.linalg.norm(pm_state)
    qml.QubitStateVector(pm_state,wires=list(range(nqubits)))
    
    ### 
    l_Batch = np.linspace(lIdx0,lIdx1,lIdx1-lIdx0,endpoint=False,requires_grad=False) 
    for iLayer in l_Batch:
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
            ### QNN Layer - 3
            QNN_layer4(params)
        if iLayer == 4:
            ### QNN Layer - 3
            QNN_layer5(params)
        
    if pIdx1 == 0:
        return qml.sample(qml.PauliX(qIdx1))
    if pIdx1 == 1:
        return qml.sample(qml.PauliY(qIdx1))
    if pIdx1 == 2:
        return qml.sample(qml.PauliZ(qIdx1))
    
def Est_EQFIM(params,paramIdx,Qsamples,Beta):
    # PhiF: samples to construct the estimate
    # No. of phiF = 4R = 2*nTrails
    # paramIdx: list of length 2
    R = 1
    
    nTrails = 2*R
    U = []
    V = []
    W = []
    for itr in range(nTrails):
        phiF = Qsamples[:,2*itr:2*(itr+1)]
        
        V.append(OpSample(params,phiF[:,1],paramIdx[1]))
        
        ### Finding estimate for anti-commutator
        temp_U = OpSample(params,phiF[:,0],paramIdx[0])
        U.append(temp_U)
        
        ### Getting state prior to the measurement. 
        temp_state = state_priorMeas(params,phiF[:,0],paramIdx[0])
        W.append(Cond_OpSample(params,temp_U,temp_state,paramIdx))
        
    estF = np.zeros((2,2))
    estF[0,0] = (1-np.dot(sum(U[0:R]),sum(U[R:nTrails]))/(R**2))/(4*nparams-4)+Beta*(nparams-2)/nparams
    estF[1,1] = (1-np.dot(sum(V[0:R]),sum(V[R:nTrails]))/(R**2))/(4*nparams-4)+Beta*(nparams-2)/nparams
    UW = [a*b for a,b in zip(U,W)]
    estF[0,1] = 0.25*(sum(UW)/nTrails - (sum(U)*sum(V))/(nTrails**2))
    estF[1,0] = estF[0,1]
    estF.requires_grad = False
    return estF
