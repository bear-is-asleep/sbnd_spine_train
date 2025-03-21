#PBS -l walltime=01:00:00
#PBS -l select=1:ncpus=32
#PBS -o /lus/eagle/projects/neutrinoGPU/bearc/spine_weights/mpvmpr_v02/logs/full_chain/uresnet_ppn/default/val_uresnet_ppn_full.stdout
#PBS -e /lus/eagle/projects/neutrinoGPU/bearc/spine_weights/mpvmpr_v02/logs/full_chain/uresnet_ppn/default/val_uresnet_ppn_full.stderr
#PBS -l filesystems=home:grand:eagle
#PBS -q debug
#PBS -A neutrinoGPU

NNODES=1
RUNDIR=/lus/eagle/projects/neutrinoGPU/bearc/spine_train/full_chain/uresnet_ppn

#Clean error and out logs
if [ -f /lus/eagle/projects/neutrinoGPU/bearc/spine_weights/mpvmpr_v02/logs/full_chain/uresnet_ppn/default/val_uresnet_ppn_full.stderr ]; then
    truncate -s 0 /lus/eagle/projects/neutrinoGPU/bearc/spine_weights/mpvmpr_v02/logs/full_chain/uresnet_ppn/default/val_uresnet_ppn_full.stderr
fi
if [ -f /lus/eagle/projects/neutrinoGPU/bearc/spine_weights/mpvmpr_v02/logs/full_chain/uresnet_ppn/default/val_uresnet_ppn_full.stdout ]; then
    truncate -s 0 /lus/eagle/projects/neutrinoGPU/bearc/spine_weights/mpvmpr_v02/logs/full_chain/uresnet_ppn/default/val_uresnet_ppn_full.stdout
fi

cd $RUNDIR
mpiexec --cpu-bind none -n $NNODES --hostfile $PBS_NODEFILE --depth=32 --ppn 1 ./uresnet_ppn_val_full_chain.sh 
