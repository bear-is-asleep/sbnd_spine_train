#PBS -l walltime=23:59:59
#PBS -l select=1:ncpus=32
#PBS -o /lus/eagle/projects/neutrinoGPU/bearc/spine_weights/mpvmpr_v02/logs/full_chain/graph_spice/default/train_graph_spice_full.stdout
#PBS -e /lus/eagle/projects/neutrinoGPU/bearc/spine_weights/mpvmpr_v02/logs/full_chain/graph_spice/default/train_graph_spice_full.stderr
#PBS -l filesystems=home:grand:eagle
#PBS -q preemptable
#PBS -A neutrinoGPU

NNODES=1
RUNDIR=/lus/eagle/projects/neutrinoGPU/bearc/spine_train/full_chain

#Clean error and out logs
if [ -f /lus/eagle/projects/neutrinoGPU/bearc/spine_weights/mpvmpr_v02/logs/full_chain/graph_spice/default/train_graph_spice_full.stderr ]; then
    truncate -s 0 /lus/eagle/projects/neutrinoGPU/bearc/spine_weights/mpvmpr_v02/logs/full_chain/graph_spice/default/train_graph_spice_full.stderr
fi
if [ -f /lus/eagle/projects/neutrinoGPU/bearc/spine_weights/mpvmpr_v02/logs/full_chain/graph_spice/default/train_graph_spice_full.stdout ]; then
    truncate -s 0 /lus/eagle/projects/neutrinoGPU/bearc/spine_weights/mpvmpr_v02/logs/full_chain/graph_spice/default/train_graph_spice_full.stdout
fi

cd $RUNDIR
mpiexec --cpu-bind none -n $NNODES --hostfile $PBS_NODEFILE --depth=32 --ppn 1 ./graph_spice_train_full_chain.sh 
