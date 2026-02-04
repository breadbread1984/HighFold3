#!/usr/bin/python3

from abc import ABC, abstractmethod
import json
from Bio.PDB import MMCIFParser
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
from alphafold3.common import folding_input
from alphafold3.constants import chemical_components

class Converter(ABC):
  @abstractmethod
  def process(self, input_file, seeds):
    raise NotImplementedError

class FASTA(Converter):
  def __init__(self,):
    pass
  def parse_fasta_to_sequence(self, fasta_file):
    sequences = {}
    with open(fasta_file) as f:
      seq_id = None
      seq_chunks = []
      for line in f:
        line = line.strip()
        if line.startswith(">"):
          if seq_id:
            sequences[seq_id] = "".join(seq_chunks)
          seq_id = line[1:].split()[0]  # 取>后第一个空格前作为id
          seq_chunks = []
        else:
          seq_chunks.append(line)
      if seq_id:
        sequences[seq_id] = "".join(seq_chunks)
    return sequences
  def create_alphafold3_input_json(self, sequences, modelSeeds=[1]):
    ids = list(sequences.keys())
    full_sequence = "".join([sequences[id_] for id_ in ids])
    json_obj = {
      "name": ids[0] if ids else "unknown",
      "sequences": [
        {
          "protein": {
            "id": ids,
            "sequence": full_sequence
           }
        }
      ],
      "modelSeeds": modelSeeds,
      "dialect": "alphafold3",
      "version": 1
    }
    return json_obj
  def process(self, input_file, seeds = [1]):
    sequences = self.parse_fasta_to_sequence(input_file)
    return self.create_alphafold3_input_json(sequences, modelSeeds = seeds)

class MMCIF(Converter):
  def __init__(self,):
    pass
  def process(self, input_file, seeds = [1]):
    with open(input_file, 'r') as f:
      mmcif_content = f.read()
    input_obj = folding_input.Input.from_mmcif(mmcif_content, chemical_components.Ccd(chemical_components._CCD_PICKLE_FILE))
    json_str = input_obj.to_json()
    return json.loads(json_str)
