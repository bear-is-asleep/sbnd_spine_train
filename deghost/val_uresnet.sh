#!/bin/bash
TRAIN_CFG=/lus/eagle/projects/neutrinoGPU/bearc/spine_train/deghost/uresnet_deghost_val.cfg
LOG_DIR=/lus/eagle/projects/neutrinoGPU/bearc/spine_weights/mpvmpr_v02/logs/deghost/default
FNAME=/lus/eagle/projects/neutrinoGPU/bearc/simulation/mpvmpr_v02/test/files.txt
PARSL_DIR=/lus/eagle/projects/neutrinoGPU/bearc/sbnd_parsl

workdir=/lus/eagle/projects/neutrinoGPU/bearc/spine_weights/mpvmpr_v02/val/deghost
#cores_per_worker=8
container=/lus/grand/projects/neutrinoGPU/software/spine_develop/larcv2_ub2204-cuda121-torch251-larndsim.sif

mkdir -p $workdir
cd $workdir
echo "Current directory: "
pwd
echo "Current files: "
ls

echo "Load singularity"
module use /soft/spack/gcc/0.6.1/install/modulefiles/Core
module load apptainer
set -e

echo "Find GPUs"
nvidia-smi
module use /soft/modulefiles 
module load conda
conda activate sbn
BESTCUDAS=$(python3 -c 'import gpustat;import numpy as np;stats=gpustat.GPUStatCollection.new_query();memory=np.array([gpu.memory_used for gpu in stats.gpus]);indices=np.argsort(memory)[:4];print(",".join(map(str, indices)))')
export CUDA_VISIBLE_DEVICES=$BESTCUDAS
echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
export OPENBLAS_NUM_THREADS=1
conda deactivate


# these lines replace hard-coded path in SPINE cfg files from github
# put the changes in a temporary copy
TMP_CFG=$(mktemp)
cp $TRAIN_CFG $TMP_CFG


echo "Config: $TMP_CFG"

singularity run -B /lus/eagle/ -B /lus/grand/ --nv $container <<EOL
    echo "Running in: "
    pwd

    #Find best GPU
    if [ -z "$CUDA_VISIBLE_DEVICES" ]; then
        export CUDA_VISIBLE_DEVICES=0,1,2,3
        echo "CUDA_VISIBLE_DEVICES not set, using 0,1,2,3"
    fi
    echo GPU Selected
    echo $CUDA_VISIBLE_DEVICES

    echo "Begin training"
    python /lus/eagle/projects/neutrinoGPU/bearc/spine/bin/run.py -c $TMP_CFG -S $FNAME
    echo "Training complete"

EOL