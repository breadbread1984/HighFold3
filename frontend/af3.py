#!/usr/bin/python3

from os import mkdir, environ
from os.path import abspath, dirname, exists, join, splitext, isdir, basename
import tempfile
import json
import subprocess
from converter import MMCIF, FASTA

class AF3(object):
  def __init__(self, model_dir, input_dir, output_dir, public_databases = '../public_databases'):
    self.model_dir = abspath(model_dir)
    assert exists(join(self.model_dir, 'af3.bin')), 'alphafold3 pretrained model not exists!'
    self.input_dir = input_dir
    self.output_dir = output_dir
    self.public_databases = abspath(public_databases)
  def predict(self, input_file, seeds = [1], gpu_id = 0):
    assert exists(self.input_dir) and isdir(self.input_dir)
    assert exists(self.output_dir) and isdir(self.output_dir)
    stem, ext = splitext(input_file)
    if ext == '.fasta':
      converter = FASTA()
    elif ext == '.cif':
      converter = MMCIF()
    else:
      raise Exception('unknown file format!')
    json_content = converter.process(input_file, seeds = seeds)
    input_name = None
    with tempfile.NamedTemporaryFile(mode = 'w', suffix = '.json', dir = self.input_dir) as f:
      f.write(json.dumps(json_content, indent = 2, ensure_ascii = False))
      f.flush()
      env = environ.copy()
      env.update({
        'CUDA_VISIBLE_DEVICES': str(gpu_id)
      })
      proc = subprocess.Popen(
        [
          "uv",
          "run",
          "python",
          "run_alphafold.py",
          f"--json_path={join(self.input_dir, basename(f.name))}",
          f"--output_dir={join(self.output_dir, str(gpu_id))}",
          f"--model_dir={self.model_dir}",
          f"--db_dir={self.public_databases}"
        ],
        env = env,
        cwd = "/app/highfold",
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
        text = True,
        bufsize = 1,
        universal_newlines = True
      )
      try:
        while True:
          output = proc.stdout.readline()
          if output == '' and proc.poll() is not None:
            break
          if output:
            yield output.strip()
      except:
        proc.kill()

if __name__ == "__main__":
  af3 = AF3()
