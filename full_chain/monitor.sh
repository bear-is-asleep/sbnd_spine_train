LOG_DIR=/lus/eagle/projects/neutrinoGPU/bearc/spine_weights/mpvmpr_v02/logs/full_chain/grappa_shower/default
PARSL_DIR=/home/bearc/sbnd_parsl

echo "Begin monitoring"

mkdir -p $LOG_DIR
rm -f $LOG_DIR/mon_log.json; touch /tmp/log && watch -n 30 -x bash -c "cp $LOG_DIR/mon_log.json /tmp/log; jq -s add <($PARSL_DIR/tools/spine_mon.sh) /tmp/log > /tmp/log2 && mv /tmp/log2 $LOG_DIR/mon_log.json"