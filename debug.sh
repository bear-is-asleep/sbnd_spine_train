#!/bin/bash

ALLOCATION="neutrinoGPU"
FILESYSTEM="home:grand:eagle"

qsub -I -l select=1 -l walltime=0:30:00 -q debug \
        -A "${ALLOCATION}" -l filesystems="${FILESYSTEM}"