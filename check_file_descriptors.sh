#!/bin/bash -l

PIDS=`ps aux | grep bearc | awk '{print $2}'`

#check time of day
echo "Time of day: `date`"

huge_pids=()

TOT_FD=0
for i in ${PIDS}; do
    #echo "PID: $i"
    NFD=`ls -1 /proc/$i/fd | wc -l`
    echo "$NFD fds:"
    ps $i | tail -n 1
    TOT_FD=$((TOT_FD + NFD))
    if [ $NFD -gt 1000 ]; then
        huge_pids+=($i)
    fi
done

for i in ${huge_pids[@]}; do
    echo "PID: $i"
    ls -la /proc/$i/fd
    #strace -e trace=open,close -p $i -c
    #lsof -p $i
done

echo "Total file descriptors: $TOT_FD"