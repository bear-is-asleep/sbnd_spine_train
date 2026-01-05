# SBND SPINE Train (Polaris)

This repository contains the code for training the SBND SPINE model on Polaris.

## Preparing

### Hadding

Files should be hadded together, such that they are each 50 GB, this is optimial for loading and batching. Additionally, the files should be split into test/train folders. An example file structure is:

```
test/larcv_mpvmpr_0000.root
test/larcv_mpvmpr_0001.root
test/larcv_mpvmpr_0002.root
...

train/larcv_mpvmpr_0000.root
train/larcv_mpvmpr_0001.root
train/larcv_mpvmpr_0002.root
...

```

### "skip_files_list:"

Some files have a very large number of ghost points which causes CNN trainings to fail. We observe that events in the highest percentile can be removed without impacting performance. To find these events, you first must count the number of voxels in each event. This is done using `test_batchsize_deghost.py`, where you provide a file list. Then you can make a histogram to find the number of events and set a cutoff maximum voxel size in `make_test_plot.py`. This should result in a file that you pass to the `skip_entry_list` parameter under `io: loader: dataset`.

### Debug
To run the training script locally do `. debug.sh`. This will start an interactive job with 1 node, 4GPUs, 64 cores, and up to 1 hour walltime. You can launch a training script by sourcing any of the `.sh` files in the directories. For example, UResNet PPN training can be launched by sourcing `spine_train/uresnet_ppn/train_uresnet_ppn.sh`. You can monitor the job by running the `monitor.sh` script in the same directory. You have to ssh into the node that the job is running on to monitor the job.

[sbnd_parl](https://github.com/SBN-ALCF/sbnd_parsl/tree/main) is used to parse the `mon_log.json` file to produce a summary of the resource usage. See [plot_spine_node_log.py](https://github.com/SBN-ALCF/sbnd_parsl/blob/main/tools/plot_spine_node_log.py) for more details.

### Submit job
Submit a job by doing `qsub <script_name>_qsub.sh`. For example, to submit the UResNet PPN training job, do `qsub spine_train/uresnet_ppn/train_uresnet_ppn_qsub.sh`. Once training is done, you can submit the validation script by doing `qsub spine_train/uresnet_ppn/val_uresnet_ppn_qsub.sh`.

### Full chain
Full chain transfer trains using labels from the previous stage. So you must select the previous stage's validation results to select the best set of weights for the model.

Once this is done, replace the weights in each `.cfg` file in the `full_chain` directory with the new weights. Transfer training happens in order: `graph_spice`, `uresnet_ppn`, [`grappa_shower`, `grappa_track`], and `grappa_inter`.

#### v02 Example results

Deghosting:
![deghost_acc](./v02_figures/deghost_accuracy.png)
![deghost_loss](./v02_figures/deghost_loss.png)
![deghost_resources](./v02_figures/deghost_resource_usage.png)

UResNet Sem.:
![uresnet_ppn_acc](./v02_figures/uresnet_ppn_accuracy.png)
![uresnet_ppn_loss](./v02_figures/uresnet_ppn_loss.png)
![uresnet_transfer_loss](./v02_figures/uresnet_transfer_loss.png)
![uresnet_transfer_acc](./v02_figures/uresnet_transfer_accuracy.png)
![uresnet_ppn_resources](./v02_figures/uresnet_ppn_resource_usage.png)

UResNet PPN:
![ppn_loss](./v02_figures/ppn_transfer_loss.png)

Graph SPICE:
![graph_spice_acc](./v02_figures/graph_spice_accuracy.png)
![graph_spice_loss](./v02_figures/graph_spice_loss.png)
![graph_spice_transfer_loss](./v02_figures/graph_spice_transfer_loss.png)
![graph_spice_transfer_acc](./v02_figures/graph_spice_transfer_accuracy.png)
![graph_spice_resources](./v02_figures/graph_spice_resource_usage.png)

Grappa Shower:
![grappa_shower_acc](./v02_figures/grappa_shower_accuracy.png)
![grappa_shower_loss](./v02_figures/grappa_shower_loss.png)
![grappa_shower_transfer_loss](./v02_figures/grappa_shower_transfer_loss.png)
![grappa_shower_transfer_acc](./v02_figures/grappa_shower_transfer_accuracy.png)
![grappa_shower_resources](./v02_figures/grappa_shower_resource_usage.png)

Grappa Track:
![grappa_track_acc](./v02_figures/grappa_track_accuracy.png)
![grappa_track_loss](./v02_figures/grappa_track_loss.png)
![grappa_track_transfer_loss](./v02_figures/grappa_track_transfer_loss.png)
![grappa_track_transfer_acc](./v02_figures/grappa_track_transfer_accuracy.png)
![grappa_track_resources](./v02_figures/grappa_track_resource_usage.png)

Grappa Inter:
![grappa_inter_acc](./v02_figures/grappa_inter_accuracy.png)
![grappa_inter_loss](./v02_figures/grappa_inter_loss.png)
![grappa_inter_transfer_loss](./v02_figures/grappa_inter_transfer_loss.png)
![grappa_inter_transfer_acc](./v02_figures/grappa_inter_transfer_accuracy.png)
![grappa_inter_resources](./v02_figures/grappa_inter_resource_usage.png)
