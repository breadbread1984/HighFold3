#!/usr/bin/python3

from absl import flags, app
import numpy as np
from Bio.PDB import PDBParser, Superimposer, MMCIFParser
from Bio.Align import PairwiseAligner
from Bio.SeqUtils import seq1  # �~M~U��~W��~M��~O�~H~W

FLAGS = flags.FLAGS

def add_options():
    flags.DEFINE_string('pred_cif', default = None, help = 'path to predicted cif')
    flags.DEFINE_string('ref_cif', default = None, help = 'path to reference cif')

def match_atom_pairs(ref_model, pred_model):
    """ref_model, pred_model 是 Model 对象"""
    ref_dict = {}
    
    # ref 构建字典：(chain_id, res_id, res_name) -> CA atom
    for chain in ref_model:
        for residue in chain:
            if residue.id[0] == ' ' and 'CA' in residue:  # 标准残基
                key = (chain.id, residue.id[1], residue.resname)
                ref_dict[key] = residue['CA']
    
    ref_ca, pred_ca = [], []
    for chain in pred_model:
        for residue in chain:
            if residue.id[0] == ' ' and 'CA' in residue:
                key = (chain.id, residue.id[1], residue.resname)
                if key in ref_dict:
                    ref_ca.append(ref_dict[key])
                    pred_ca.append(residue['CA'])
    
    print(f"Matched {len(ref_ca)} Cα pairs")
    return ref_ca, pred_ca

def main(unused_argv):

  parser = MMCIFParser(QUIET=True)
  ref_structure = parser.get_structure('ref', FLAGS.ref_cif)
  pred_structure = parser.get_structure('pred', FLAGS.pred_cif)
  ref_ca, pred_ca = match_atom_pairs(ref_structure[0], pred_structure[0])
  sup = Superimposer()
  sup.set_atoms(ref_ca, pred_ca)
  sup.apply(pred_ca)
  rmsd = sup.rms
  print(f"RMSD: {rmsd} Å")

if __name__ == "__main__":
    add_options()
    app.run(main)

