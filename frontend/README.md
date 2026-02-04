# Introduction

this project implements a frontend for Alphafold3. it serves as a task launcher, a status monitor and a result visualizer

# Usage

## Install prerequisite packages

```shell
cd <src_root>/frontend
sudo apt install zstd docker.io docker-compose-v2 docker-buildx
python3 -m pip install -r requirements.txt
```

## Download prerequisite data

```shell
cd <src_root>
bash prepare.sh
```

## Download pretrained AF3 model

1. apply for pretrained model file **af3.bin.zst** [here](forms.gle/svvpY4u2jsHEwWYS6)

2. unzip and place the model with the following command

```shell
zstd -d af3.bin.zst
mkdir <src_root>/pretrained
mv af3.bin <src_root>/pretrained
```

## Launch service

```shell
cd <src_root>/frontend
python3 main.py [--num_gpus <number of gpus>]
```

visit service with **localhost:8084**
