"""
Global Variables
@author: mdaamirsohail
"""
from pennylane import numpy as np
from model_4qubit import nqubits

sq2 = np.sqrt(2)

ket0 = np.array([[1],[0]])
rho0 = np.matmul(ket0,ket0.conj().T)

ket1 = np.array([[0],[1]])
rho1 = np.matmul(ket1,ket1.conj().T)

ketp = np.array([[1],[1]])/sq2
rhop = np.matmul(ketp,ketp.conj().T)

ketm = np.array([[1],[-1]])/sq2
rhom = np.matmul(ketm,ketm.conj().T)

ketip = np.array([[1],[1j]])/sq2
rhoip = np.matmul(ketip,ketip.conj().T)

ketim = np.array([[1],[-1j]])/sq2
rhoim = np.matmul(ketim,ketim.conj().T)

pI = np.array([[1,0],\
              [0,1]])
pX = np.array([[0,1],\
              [1,0]]) 
pY = np.array([[0,-1j],\
              [1j,0]]) 
pZ = np.array([[1,0],\
              [0,-1]]) 

'Notation'
pauli_op = {'0':pX, '1':pY, '2':pZ}

### Used in Gradient Estimation
### Nomenclature: V_op[ab] -> a: qubit idx, b: Pauli idx
V_dict = {}
for pIdx in range(3): #over Pauli operators
    for qIdx in range(nqubits): #over Qubit Index
        if qIdx == 0: V_op = pauli_op[str(pIdx)]
        else: V_op = pI
        for i_kron in range(1,nqubits):
            if qIdx == i_kron: temp = pauli_op[str(pIdx)]
            else: temp = pI
            
            V_op = np.kron(V_op,temp)

        V_dict[str(qIdx)+str(pIdx)] = V_op
        
### Used in EQFIM estimation
### Nomenclature: rho_ab -> a: qubit idx, b: Pauli idx
pBasis_p1 = {'0':rhop,'1':rhoip,'2':rho0}
pBasis_m1 = {'0':rhom,'1':rhoim,'2':rho1}
Proj_dict_p1 = {}
for pIdx0 in range(3):
    for qIdx0 in range(nqubits):
        if qIdx0 == 0: Proj = pBasis_p1[str(pIdx0)]
        else: Proj = pI
        for i_kron in range(1,nqubits):
            if qIdx0 == i_kron: temp = pBasis_p1[str(pIdx0)]
            else: temp = pI
            Proj = np.kron(Proj,temp)
        
        Proj_dict_p1[str(qIdx0)+str(pIdx0)] = Proj

Proj_dict_m1 = {}
for pIdx0 in range(3):
    for qIdx0 in range(nqubits):
        if qIdx0 == 0: Proj = pBasis_m1[str(pIdx0)]
        else: Proj = pI
        for i_kron in range(1,nqubits):
            if qIdx0 == i_kron: temp = pBasis_m1[str(pIdx0)]
            else: temp = pI
            Proj = np.kron(Proj,temp)
        
        Proj_dict_m1[str(qIdx0)+str(pIdx0)] = Proj
             
                