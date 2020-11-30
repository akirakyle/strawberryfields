# Copyright 2020 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Gaussian operations"""

import numpy as np


def chop_in_blocks(m, idtodelete):
    """
    Splits a (symmetric) matrix into 3 blocks, A, B, C
    Blocks A and B are diagonal blocks and C is the offdiagonal block
    idtodelete specifies which indices go into B.
    """
    A = np.copy(m)
    A = np.delete(A, idtodelete, axis=0)
    A = np.delete(A, idtodelete, axis=1)
    B = np.delete(m[:, idtodelete], idtodelete, axis=0)
    C = np.empty((len(idtodelete), (len(idtodelete))))
    for localindex, globalindex in enumerate(idtodelete):
        for localindex1, globalindex1 in enumerate(idtodelete):
            C[localindex, localindex1] = m[globalindex, globalindex1]
    return (A, B, C)

def chop_in_blocks_multi(m, idtodelete):
    """
    Splits an array of (symmetric) matrices each into 3 blocks, A, B, C
    Blocks A and C are diagonal blocks and B is the offdiagonal block
    idtodelete specifies which indices go into C.
    """
    A = np.copy(m)
    A = np.delete(A, idtodelete, axis=1)
    A = np.delete(A, idtodelete, axis=2)
    B = np.delete(m[:,:, idtodelete], idtodelete, axis=1)
    C = m[:,idtodelete,:][:,:,idtodelete]
    return (A, B, C)


def chop_in_blocks_vector(v, idtodelete):
    """
    Splits a vector into two vectors, where idtodelete specifies
    which elements go into vb
    """
    idtokeep = list(set(np.arange(len(v))) - set(idtodelete))
    va = v[idtokeep]
    vb = v[idtodelete]
    return (va, vb)

def chop_in_blocks_vector_multi(v, idtodelete):
    """
    Splits a vector into two vectors, where idtodelete specifies
    which elements go into vb
    """
    idtokeep = list(set(np.arange(len(v[0]))) - set(idtodelete))
    va = v[:,idtokeep]
    vb = v[:,idtodelete]
    return (va, vb)


def reassemble(A, idtodelete):
    """
    Puts the matrix A inside a larger matrix of dimensions
    dim(A)+len(idtodelete)
    The empty space are filled with zeros (offdiagonal) and ones (diagonals)
    """
    ntot = len(A) + len(idtodelete)
    ind = set(np.arange(ntot)) - set(idtodelete)
    newmat = np.zeros((ntot, ntot))
    for i, i1 in enumerate(ind):
        for j, j1 in enumerate(ind):
            newmat[i1, j1] = A[i, j]

    for i in idtodelete:
        newmat[i, i] = 1.0
    return newmat

def reassemble_multi(A, idtodelete):
    """
    Puts the matrices A inside larger matrices of dimensions
    dim(A)+len(idtodelete)
    The empty space are filled with zeros (offdiagonal) and ones (diagonals)
    """
    nweights = len(A[:,0,0])
    ntot = len(A[0]) + len(idtodelete)
    ind = list(set(np.arange(ntot)) - set(idtodelete))
    newmat = np.tile(np.eye(ntot,dtype=complex),(nweights,1,1))
    newmat[np.ix_(np.arange(newmat.shape[0],dtype=int),ind,ind)] = A
    return newmat


def reassemble_vector(va, idtodelete):
    r"""Creates a vector with zeros indices idtodelete
    and everywhere else it puts the entries of va
    """
    ntot = len(va) + len(idtodelete)
    ind = set(np.arange(ntot)) - set(idtodelete)
    newv = np.zeros(ntot)
    for j, j1 in enumerate(ind):
        newv[j1] = va[j]
    return newv

def reassemble_vector_multi(va, idtodelete):
    r"""Creates a vector with zeros indices idtodelete
    and everywhere else it puts the entries of va
    """
    nweights = len(va[:,0])
    ntot = len(va[0]) + len(idtodelete)
    ind = list(set(np.arange(ntot)) - set(idtodelete))
    newv = np.zeros((nweights,ntot),dtype=complex)
    newv[:,ind] = va
    return newv
