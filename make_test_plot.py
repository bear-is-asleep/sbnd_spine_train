import glob
import numpy as np
import pandas as pd
#import matplotlib as mpl
#from matplotlib import pyplot as plt

TOO_MANY_VOXELS = 5e5

#mpl.rcParams.update({'font.size': 18})
#mpl.rcParams.update({'figure.autolayout': True})

# file_names = np.sort(glob.glob('/sdf/data/neutrino/icarus/sim/mpvmpr_v3/merge_files/train_*_counts.txt'))
# file_names = np.sort(glob.glob('/sdf/data/neutrino/icarus/sim/mpvmpr_v3/merge_files/test_*_counts.txt'))
file_names = np.sort(glob.glob('/lus/eagle/projects/neutrinoGPU/bearc/simulation/mpvmpr_v02/train/larcv_mpvmpr_*_counts.txt'))
# file_names = np.sort(glob.glob('/sdf/data/neutrino/icarus/sim/mpvmpr_v4/merge_files/test_*_counts.txt'))
# print(file_names)
# file_names = np.sort(glob.glob('/sdf/data/neutrino/icarus/sim/mpvmpr_v1/test_*_counts.txt'))
df = pd.concat([pd.read_csv(fname) for fname in file_names], ignore_index=True)
print(df)
# df = pd.read_csv('voxel_counts_icarus_localized_test.txt')
skip_event_list = np.where(df.num_sp > TOO_MANY_VOXELS)[0] # Cut for MPVMPR v02
of = open('sbnd_mpvmpr_v02_train_skip_event_list.txt', 'w')

of.write(','.join([str(e) for e in skip_event_list]))
of.close()

# fig, ax1 = plt.subplots(figsize=(9,6))
# # n, x, __ = plt.hist(df.num_sp, range=[0,6e6], bins=100, histtype='step', linewidth=2)
# n, x, __ = plt.hist(df.num_sp, range=[0,1e6], bins=100, histtype='step', linewidth=2)
# # n, x, __ = plt.hist(df.num_sp, range=[0,1e5], bins=100, histtype='step', linewidth=2)

# xc = (x[:-1]+x[1:])/2
# cumsum = np.cumsum(n)/len(df)
# ax2 = ax1.twinx()
# ax2.set_ylim([0,1])
# ax2.plot(xc, cumsum, 'o-', linewidth=2)

# for v in [0.9, 0.95]:#, 0.99]:
#     print(v)
#     l = np.where(cumsum > v)[0][0]-1
#     ax2.plot([xc[l], xc[l]], [0, 1], label=f'${(v*100):0.1f}\,\%:\,\,{xc[l]:.2e}$')
# ax2.legend()

# ax1.grid()
# ax1.set_xlabel('Number of voxels')
print('Max number:', np.max(df.num_sp), '(entry:', np.argmax(df.num_sp), '\b)')
#plt.show()
