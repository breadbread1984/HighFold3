#!/usr/bin/python3

from typing import List
import numpy as np

def calc_cyclic_matrix_af3(residue_index, head_to_tail = False, list_cid_ss: List = [], token_wise = False, signal_bug_fix = True):
  if head_to_tail:
    i = np.arange(residue_index.shape[0]) # i.shape = (n,)
    j0 = i
    d1 = i[:, None] - j0[None, :] # (i - j0).shape = (n, n)
    # distances with other elements in the next cycle
    j1 = i + residue_index.shape[0]
    d2 = i[:, None] - j1[None, :] # (i - j1).shape = (n, n)
    # distances with other elements in the last cycle
    j2 = i - residue_index.shape[0]
    d3 = i[:, None] - j2[None, :] # (i - j2).shape = (n, n)
    dists = np.stack([d1, d2, d3], axis = -1) # dists.shape = (n, n, 3)
    index = np.argmin(np.abs(dists), axis = -1, keepdims = True) # index.shape = (n, n, 1)
    signed_dists = np.squeeze(np.take_along_axis(dists, index, axis = -1), axis = -1) # signed_dists.shape = (n,n)
  else:
    left_residue_index = residue_index[:, None]
    right_residue_index = residue_index[None, :]
    signed_dists = left_residue_index - right_residue_index
  return signed_dists

if __name__ == "__main__":
  residue_index = np.arange(8)
  print(calc_cyclic_matrix_af3(residue_index, True))
  print(calc_cyclic_matrix_af3(residue_index, False))
