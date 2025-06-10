import xarray as xr
import numpy as np
import re
import glob
from collections import defaultdict

prefix = "/cluster/home/vogtva/cno/CNO2d_time_dependent_&_foundation_model/out/stat/"
# Get all .npy files
files = glob.glob(prefix + "pred_pattern_*_batch_*_jump_*.npy")
res = []
# # Parse filenames into (pattern, batch, jump) → filepath
pattern_re = re.compile(r"pattern_(\d+)_batch_(\d+)_jump_(\d+)\.npy")
filemap = defaultdict(lambda: defaultdict(dict))

for f in files:
    match = pattern_re.search(f)
    if match:
        p, b, j = map(int, match.groups())
        res.append([p, b, j])

res = np.array(res)

data = {}
patterns = np.unique(res[:, 0])
batch_indices = np.unique(
    res[:, 1]
)  # Fill this with your batch indices (e.g. range(N))

for p in patterns:
    data[p] = {}
    for b in batch_indices:
        data[p][b] = {}
        for j in range(p):
            filename = prefix + f"pred_pattern_{p}_batch_{b}_jump_{j}.npy"
            data[p][b][j] = np.load(filename)

np.savez(
    "/cluster/scratch/vogtva/out/cno_outputs/merged_data.npz",
    **{
        f"{p}_{b}_{j}": data[p][b][j] for p in data for b in data[p] for j in data[p][b]
    },
)
