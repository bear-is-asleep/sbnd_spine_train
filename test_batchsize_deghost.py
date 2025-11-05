import ROOT
import os
import larcv
import pathlib
from glob import glob
import numpy as np

file_names = 'files.txt'
tree_names = ['sparse3d_reco', 'sparse3d_pcluster', 'particle_pcluster']

with open(file_names, 'r') as f:
    file_names = f.readlines()
file_names = [f.strip() for f in file_names]
# for fname in file_names:
#     print(fname)

for i, fname in enumerate(file_names):
    print('Processing', fname)
    root_file = ROOT.TFile(fname, 'r')
    path = pathlib.Path(fname)
    out_name = str(path.with_suffix('')) + '_counts.txt'
    if os.path.exists(out_name):
        continue
    with open(out_name, 'w') as out_file:
        header = f'entry,num_sp,num_tp,num_part\n'
        out_file.write(header)
        num_entries = getattr(root_file, f'{tree_names[0]}_tree').GetEntries()
        print('Number of entries', num_entries)
        for i in range(num_entries):
            out_str = f'{i}'
            for tname in tree_names:
                tree = getattr(root_file, f'{tname}_tree')
                tree.GetEntry(i)
                value = getattr(tree, f'{tname}_branch').as_vector().size()
                out_str += f',{value}'

            out_file.write(f'{out_str}\n')
