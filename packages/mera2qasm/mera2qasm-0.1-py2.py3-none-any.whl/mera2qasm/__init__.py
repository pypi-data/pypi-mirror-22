# Author : Isaac H. Kim
# This code generates a random translationally invariant (n,D)-DMERA, and given
# a local observable, outputs the following data:
# 1) m' : Number of extra qubits
# 2) A sequence of quantum circuits,
# with the following convention:
# qreg data[m];
# qreg ancilla[m'];
# circuit 1
# circuit 2
# ...
# last circuit
# measure data in a certain basis

# It also outputs a cell array consisting of a list of SU(4)s of the (n,D)-DMERA.

# Important! We use the following convention.
# site : integer or a tuple of integers
# circuit : a list of sites
# Supp : a list of sites
# circuits : a list of circuit in a sequential order(in the Schrodinger picture). This is
#            different from the MATLAB convention, which is in the Heisenberg picture.
from scipy import sparse
import numpy as np
import random
import math
## Return True if circuit1 and circuit 2 commute. Return False otherwise.
def commute(circuit1, circuit2):
    if len(set(circuit1) & set(circuit2))==0:
        return True
    else:
        return False

import matplotlib.pyplot as plt
import matplotlib.patches as patches
## Draws the past causal cone of an observable supported on Supp.
## Verified.
def pcc_drawer(n,D,Supp):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    axes = plt.gca()
    axes.set_xlim([0, pow(2,n)+1])
    axes.set_ylim([0, n+1])
    pcc = pcc_mera2(n,D,Supp)
    for s in range(1,n+1):
        for d in range(1,D+1):
            mycircuits = circuits_dmera(n,D,s,d)
            # Make the rectangle objects
            rectangles = []
            for circuit in mycircuits:
                if circuit in pcc[(s,d)]:
                    rectangles.append(patches.Rectangle((circuit[0], s + d/D+0.05), max((circuit[1]-1)%pow(2,n) -(circuit[0]-1),0), 1/D-0.1,facecolor="red"))
                else:
                    rectangles.append(patches.Rectangle((circuit[0], s + d/D+0.05), max((circuit[1]-1)%pow(2,n) -(circuit[0]-1),0), 1/D-0.1,facecolor="blue"))
                    
            # Plot the rectangles
            for rectangle in rectangles:
                ax.add_patch(rectangle)
           
    plt.axis('off')
    fig.show()

    
## circuits_dmera : Outputs a set of circuits of a (n,D)-MERA on the (s,d)-th layer.
## Verified.
def circuits_dmera(n, D, s, d):
    if n < s:
        print('circuits_dmera Warning : scale range out of bound.')
    if D < d:
        print('circuits_dmera Warning : depth range out of bound.')
    circuits = []
    if d%2 == 0:
        for i in range(pow(2,n-s)):
            circuits.append([pow(2,s) * i % pow(2,n), (pow(2,s) * i + pow(2,s-1)) % pow(2,n)])
    else:
        for i in range(pow(2,n-s)):
            circuits.append([(pow(2,s)*i + pow(2,s-1)) % pow(2,n), (pow(2,s)*(i+1)) % pow(2,n)])
    return circuits

## Supp_update : Outputs a set of circuits that influence Supp, together with the enlarged support.
## Verified.
def Supp_update(circuits, Supp):
    relevant_circuits = []
    for circuit in circuits:
        # If the support of the circuit and Supp has a nontrivial intersection,
        # append the circuit to the list of relevant circuits, and update Supp accordingly.
        if len(set(circuit) & set(Supp)) != 0:
            relevant_circuits.append(circuit)
            Supp = list(set(circuit) | set(Supp))
    return relevant_circuits, Supp

## pcc_mera : Outputs an ordered list of the support of the two-qubit gates that lies in the
##           past causal cone of an operator supported on Supp.
## Verified.
def pcc_mera(n, D, Supp):
    circuits = []
    for s in range(1,n+1):
        for d in range(1,D+1):
            relevant_circuits, Supp = Supp_update(circuits_dmera(n,D,s,d), Supp)
            circuits = circuits + relevant_circuits
    # For the output, order in the Schrodinger picture.
    return circuits[::-1]

## Similar to pcc_mera. But the output format is different.
## It outputs a set of circuits in the past causal cone for each (s,d).
## Verified.
def pcc_mera2(n,D,Supp):
    circuits = {}
    for s in range(1,n+1):
        for d in range(1,D+1):
            relevant_circuits, Supp = Supp_update(circuits_dmera(n,D,s,d), Supp)
            circuits[(s,d)] = relevant_circuits
    return circuits
    

# site_removal : Removes
def site_removal(circuits):
    circuits_rev = circuits[::-1]
    sites_appeared = []
    sites_appeared_prev = []
    sites_remove = []

    for circuit in circuits_rev:
        sites_appeared = list(set(sites_appeared + circuit))
        sites_remove.append(list(set(sites_appeared) - set(sites_appeared_prev)))
        sites_appeared_prev = sites_appeared
    return sites_remove[::-1]

# pcc : Returns the circuit elements that influence the site.
def pcc(Supp, circuits):
    circuits_rev = circuits[::-1]
    circuits_rel = []
    for circuit in circuits_rev:
        if bool(set(circuit) & set(Supp)):
            circuits_rel.append(circuit)
            Supp = list(set(Supp) | set(circuit))
    return circuits_rel[::-1]

def ancestor(Supp, circuits):
    circuits_rev = circuits[::-1]
    for circuit in circuits_rev:
        if bool(set(circuit) & set(Supp)):
            Supp = list(set(Supp) | set(circuit))
    return Supp

# Circuit sequence that is optimal in terms of the number of necessary qubits.
def compress(circuits):
    circuits_optimized = []
    # List all the involved qubits.
    qubits = []
    for circuit in circuits:
        qubits = list(set(qubits) | set(circuit))
    qubits = list(qubits)

    # Repeat while there are qubits left.
    while bool(qubits):
        # Record the size of the ancestors
        number_of_ancestors={}
        for qubit in qubits:
            number_of_ancestors[qubit] = len(ancestor([qubit], circuits))

        # Find the qubit with the smallest number of ancestors,
        # which is deemed unworthy of being alive.
        qubit_unworthy = min(number_of_ancestors, key = number_of_ancestors.get)

        # List all the circuits that influence the unworthy qubits.
        circuits_unworthy = pcc([qubit_unworthy], circuits)
        # Add them to the optimized circuit
        circuits_optimized = circuits_optimized + circuits_unworthy
        # Add partial trace of the unworthy qubit in the optimized circuit
        circuits_optimized = circuits_optimized + [[qubit_unworthy]]
        # Remove the unworthy circuits from the original circuits
        for circuit in circuits_unworthy:
            circuits.remove(circuit)
        # Remove the unworthy qubit from the list of qubits
        qubits.remove(qubit_unworthy)
 
#    Supp=[]
#    for circuit in circuits_optimized:
#        if len(circuit)==2:
#            Supp = list(set(Supp) | set(circuit))
#        elif len(circuit)==1:
#            Supp = list(set(Supp) - set(circuit))
#        else:
#            print('Error: The length of the circuit element should be either 1 or 2.')
#        print('Support size=',len(Supp))
    return circuits_optimized

# Outputs a compressed circuit for the physical qubits
def compress_physical(circuits, MySupp):
    circuits_compressed = compress(circuits)

    # Compute the number of necessary auxiliary qubits.
    auxiliaryqubits = []
    for circuit in circuits:
        auxiliaryqubits = auxiliaryqubits + circuit
    howmanyauxiliaryqubits = len(set(auxiliaryqubits))
    
    # Compute the number of necessary physical qubits.
    Supp = []
    howmanyphysicalqubits = 0
    for circuit in circuits_compressed:
        if len(circuit)==2:
            Supp = list(set(Supp) | set(circuit))
            if len(Supp) > howmanyphysicalqubits:
                howmanyphysicalqubits = len(Supp)
        elif len(circuit)==1:
            Supp = list(set(Supp) - set(circuit))
        else:
            print('Error: The length of the circuit element should be either 1 or 2.')

    # Create an occupation table for the physical qubits. Initially none of the qubits
    # are occupied.
    occupied = [False] * howmanyphysicalqubits

    # Initialize an assignement dictionary for the auxiliary qubits.
    assignment = {}
    
    # Create an assignment dictionary.
    for circuit in circuits_compressed:
        if len(circuit)==2:
            # If the input is a two-qubit gate, we should assign a physical qubit to the new
            # auxiliary qubits.
            for site in circuit:
                # If an auxiliary qubit is not assigned to a physical qubit, assign an
                # unoccupied physical qubit.
                if not (site in assignment.keys()):
                    physicalqubit_unoccupied = occupied.index(False)
                    assignment[site] = physicalqubit_unoccupied
                    occupied[physicalqubit_unoccupied] = True
                    
        if len(circuit)==1:
            # If the input is a partial trace of a single qubit, we should label the corresponding
            # physical qubit as unoccupied.
            occupied[assignment[circuit[0]]] = False

    # Rewrite the circuit/Support in terms of the operations on the physical qubits.
    circuits_physical = []
    for circuit in circuits_compressed:
        circuits_physical.append([assignment[x] for x in circuit])
    Supp_physical = [assignment[site] for site in MySupp]
    return circuits_physical, Supp_physical

def kronm(Q,x):
    m = x.shape[1]
    k = len(Q)
    R = np.zeros([1,k])
    C = [0]*k
    comp = [True]*k

    for i in range(k):
        if Q[i].size == 1:
            comp[i] = False
            R[i] = Q[i]
            C[i] = Q[i]
        else:
            R[i],C[i] = Q[i].shape
    xsiz = C+[m]

    if comp[0]:
        x = Q[0] @ np.reshape([C[0], np.prod(xsiz) / C[0]], order='F').copy()
        xsiz[0] = R[0]

    if k>0 and m==1:
        if comp[k]:
            x = x.reshape([np.prod(xsiz)/C[k], C[k]], order = 'F').copy() @ Q[k].T.conj()
            xsiz[k] = R[k]
        loopTo = k-1
    else:
        loopTo = k

    if k>1 or m>1:
        x = x.reshape(xsiz, order = 'F')
        for i in range(1, loopTo+1):
            if comp[i]:
                perm = [n for n in range(k+1)]
                dims.remove(i)
                perm = [i] + perm
                Xmat = np.transpose(x,perm).reshape([C[i], np.prod(xsiz)/C[i]] , order='F').copy()
                Xmat = Q[i] @ Xmat
                xsiz[i] = R[i]

                iperm = list(np.argsort(list(perm)))
                x = np.transpose(Xmat.reshape([R[i]] + [xsiz[n] for n in dims[1:k]]), iperm).copy()
    x = x.reshape([np.prod(R),m], order='F')
    return x

# Permutes the subsystems according to perm
# Verified
def syspermute(rho, perm):
    n=len(rho)
    qubits = int(np.log2(n))
    perm = [qubits-i-1 for i in reversed(perm)]
    perm = perm + [qubits+i for i in perm]
    return np.transpose(rho.reshape([2] * qubits *2, order='F'),perm).reshape([n,n], order='F')

# Applies a CNOT gate from the control to the target qubit
# Verified
def CX(rho, control, target):
    dim = len(rho)
    perm = [n for n in range(int(np.log2(dim)))]
    perm.remove(control)
    perm.remove(target)
    perm = [control] + [target] + perm
    iperm=list(np.argsort(list(perm)))
    rho_permuted = syspermute(rho, iperm)
    CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    CNOT_e = sparse.kron(CNOT, sparse.eye(dim/4))
    rho_pc = CNOT_e @ rho_permuted @ CNOT_e
    return syspermute(rho_pc,perm)

# Creates a random n x n unitary matrix.
# Verified
def randU(n):
    X = (np.random.randn(n,n) + 1j * np.random.randn(n,n))/np.sqrt(2)
    Q, R = np.linalg.qr(X)
    R = np.diag(np.diag(R) / abs(np.diag(R)))
    return Q @ R

# Creates a random n x n Hermitian matrix.
# Verified
def randH(n):
    H = 2*(np.random.randn(n,n) + 1j * np.random.randn(n,n)) - (1+1j) * np.ones((n,n))
    return H + H.T.conj()

# Creates a random n x n density matrix.
# Verified
def randRho(n):
    p=randH(n)
    return (p @ p) / np.trace(p @ p)

# Apply a single-qubit gate U to the indexed qubit
# Verified
def singleQ(U,rho,index):
    dim = len(rho)
    dim_former = pow(2,index)
    dim_latter = dim / 2 / dim_former
    U_e =  sparse.kron(sparse.kron(sparse.eye(dim_former), U), sparse.eye(dim_latter))
    return U_e @ rho @ U_e.T.conj()
    
# Apply a depolarizing noise on the indexed qubit with noise rate p.
# Verified
def depolarizing(rho,index,p):
    dim = len(rho)
    dim_former = pow(2,index)
    dim_latter = dim / 2 / dim_former

    X = np.array([[0,1],[1,0]])
    Y = np.array([[0,-1j],[1j,0]])
    Z = np.array([[1,0],[0,-1]])

    X_e =  sparse.kron(sparse.kron(sparse.eye(dim_former), X), sparse.eye(dim_latter))
    Y_e =  sparse.kron(sparse.kron(sparse.eye(dim_former), Y), sparse.eye(dim_latter))
    Z_e =  sparse.kron(sparse.kron(sparse.eye(dim_former), Z), sparse.eye(dim_latter))

    return (1-p) * rho + (p/3) * (X_e @ rho @ X_e + Y_e @ rho @ Y_e + Z_e @ rho @ Z_e) 

# Apply partial trace on the indexed qubit
# Verified
def partial_trace(rho, index):
    dim = len(rho)
    dim_former = pow(2,index)
    dim_latter = dim / 2 / dim_former
    
    unitvectors=np.identity(2)
    v1 = sparse.kron(sparse.kron(sparse.eye(dim_former), unitvectors[0,:]), sparse.eye(dim_latter))
    v2 = sparse.kron(sparse.kron(sparse.eye(dim_former), unitvectors[1,:]), sparse.eye(dim_latter))
    return v1 @ rho @ v1.T.conj() + v2 @ rho @ v2.T.conj() 

# Reset the indexed qubit
# Verified
def reset(rho, index):
    dim = len(rho)
    dim_former = pow(2,index)
    dim_latter = dim / 2 / dim_former

    unitvectors = np.identity(2)
    p1 = sparse.kron(sparse.kron(sparse.eye(dim_former), np.outer(unitvectors[0,:].T, unitvectors[0,:])), sparse.eye(dim_latter))
    p2 = sparse.kron(sparse.kron(sparse.eye(dim_former), np.outer(unitvectors[0,:].T, unitvectors[1,:])), sparse.eye(dim_latter))
    return p1 @ rho @ p1.T + p2 @ rho @ p2.T

def noise_study(n,D,Supp,p,samples):
    deviations = [noise_simulation(n,D,Supp,p) for i in range(samples)]
    return deviations

# Returns the trace distance between the reduced density matrix
def noise_simulation(n,D,Supp,p,q):
    MySupp = Supp
    circuits = pcc_mera(n,D,Supp)
    circuits_optimized, Supp_physical = compress_physical(circuits, Supp)
    circuits_rev = circuits_optimized[::-1]
    for site in Supp_physical:
        circuits_rev.remove([site])
    circuits_optimized = circuits_rev[::-1]
    dim = pow(2,max(max(circuits_optimized))+1)
    tempvector = np.zeros((dim,1))
    tempvector[0] = 1.0
    rho = np.outer(tempvector, tempvector)
    rho_e = np.outer(tempvector, tempvector)
    for circuit in circuits_optimized:
        if len(circuit)==1:
            print('Reset', circuit)
            rho = reset(rho, circuit[0])
            rho_e = depolarizing(reset(rho_e, circuit[0]), circuit[0], p)
        else:
            print('Two-qubit gate', circuit)
            Us=[randU(2) for n in range(8)]

            rho = singleQ(Us[0], rho, circuit[0])
            rho = singleQ(Us[1], rho, circuit[1])
            rho = CX(rho, circuit[0], circuit[1])
            rho = singleQ(Us[2], rho, circuit[0])
            rho = singleQ(Us[3], rho, circuit[1])
            rho = CX(rho, circuit[0], circuit[1])
            rho = singleQ(Us[4], rho, circuit[0])
            rho = singleQ(Us[5], rho, circuit[1])
            rho = CX(rho, circuit[0], circuit[1])
            rho = singleQ(Us[6], rho, circuit[0])
            rho = singleQ(Us[7], rho, circuit[1])

            rho_e = depolarizing(singleQ(Us[0], rho_e, circuit[0]),circuit[0],p)
            rho_e = depolarizing(singleQ(Us[1], rho_e, circuit[1]),circuit[1],p)
            rho_e = depolarizing(depolarizing(CX(rho_e, circuit[0], circuit[1]), circuit[0], q), circuit[1],q)
            rho_e = depolarizing(singleQ(Us[2], rho_e, circuit[0]),circuit[0],p)
            rho_e = depolarizing(singleQ(Us[3], rho_e, circuit[1]),circuit[1],p)
            rho_e = depolarizing(depolarizing(CX(rho_e, circuit[0], circuit[1]), circuit[0], q), circuit[1],q)
            rho_e = depolarizing(singleQ(Us[4], rho_e, circuit[0]),circuit[0],p)
            rho_e = depolarizing(singleQ(Us[5], rho_e, circuit[1]),circuit[1],p)
            rho_e = depolarizing(depolarizing(CX(rho_e, circuit[0], circuit[1]), circuit[0], q), circuit[1],q)
            rho_e = depolarizing(singleQ(Us[6], rho_e, circuit[0]),circuit[0],p)
            rho_e = depolarizing(singleQ(Us[7], rho_e, circuit[1]),circuit[1],p)
       
            # Currently we are only applying CNOT. We need to change it so that we apply
            # an arbitrary SU(4).
    # Currently we are getting the output density matrix over excessive number of qubits.
    # We need to change it so that we only get the relevant qubits.
    print('Support:', Supp_physical)
    delta = rho - rho_e
    myrange = max(max(circuits_optimized))        
    return sum(abs(np.linalg.eigvals(rho - rho_e)))

# Generates a random (n,D)-DMERA and returns the quantum circuit that measures the observable
# lying on the support.
def mera2qasm(n,D,Supp,outfilename):
    MySupp=Supp
    circuits = pcc_mera(n,D,Supp)
    circuits_optimized, Supp = compress_physical(circuits, Supp)
    # Remove the last partial trace of the sites in Supp.
    circuits_rev = circuits_optimized[::-1]
    for site in Supp:
        circuits_rev.remove([site])
    circuits_optimized = circuits_rev[::-1]

    numberoffaultlocations = 0 
    for circuit in circuits_optimized:
        if len(circuit)==2:
            numberoffaultlocations = numberoffaultlocations + 24
    
    with open(outfilename +'.qasm', 'w') as script:
        script.write('// This is Isaac Kim\'s randomly generated QASM code.\n')
        script.write('// This is a quantum circuit that computes an observable supported on ' +str(MySupp)+' over a ('+str(n)+','+str(D)+')-DMERA.\n')
        script.write('// Total number of physical qubits is '+str(max(max(circuits_optimized))+1) +'.\n')
        script.write('// Total number of fault locations is roughly '+str(numberoffaultlocations)+'.\n' )
        script.write('IBMQASM 2.0;\n')
        script.write('qreg q['+str(max(max(circuits_optimized)) + 1)+'];\n')
        script.write('creg out['+str(len(Supp))+'];\n')
        for circuit in circuits_optimized:
            if len(circuit)==1:
                script.write('reset q'+str(circuit)+';\n')
            elif len(circuit)==2:
                # Generate 24 random parameters.
                thetas = [random.random() * 4 * math.pi for n in range(24)]
                for n in range(3):
                    script.write('U('+str(thetas[6*n])+','+str(thetas[6*n+1])+','+str(thetas[6*n+2])+') q['+str(circuit[0])+'];\n')
                    script.write('U('+str(thetas[6*n+3])+','+str(thetas[6*n+4])+','+str(thetas[6*n+5])+') q['+str(circuit[1])+'];\n')
                    script.write('CX q['+str(circuit[0])+'], q['+str(circuit[1])+'];\n')
                script.write('U('+str(thetas[18])+','+str(thetas[19])+','+str(thetas[20])+') q['+str(circuit[0])+'];\n')
                script.write('U('+str(thetas[21])+','+str(thetas[22])+','+str(thetas[23])+') q['+str(circuit[1])+'];\n')
        for site in Supp:
            script.write('measure q['+str(site)+'] -> c['+str(Supp.index(site))+'];\n')
         
def mera2qasms(n,D,Supp):
    for n in range(100):
        mera2qasm(n,D,Supp,'mera2qasm'+str(n))
    

    
