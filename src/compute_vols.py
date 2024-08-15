from pyNiftyReg.utils import *
import nibabel as nib
import numpy as np
import pandas as pd
import tqdm
vol1 = nib.load('y0_labeled_resampled.nii.gz')
vol2 = nib.load('../data/annotated/y2_final_clean_2455_coloured_airway_refactored_all.nii.gz')

max_val = int(np.max(vol1.get_fdata()))
print(f"Max label: {max_val}")
# Get and print all of the  unique values in the volume
unique_vals = np.unique(vol1.get_fdata())
#print(f"Unique values: {unique_vals}")

# Put the results in a pandas dataframe
results = pd.DataFrame(columns=["Label", "Volume 1", "Volume 2", "Volume Difference", "Volume Difference (%)"])
for i in range(1, max_val + 1):
    print(f"Label {i}")
    volume_vol1 = compute_volume(vol1, i)
    volume_vol2 = compute_volume(vol2, i)

    volume_diff = np.abs(volume_vol1 - volume_vol2)
    volume_diff_percent = np.abs(100 * volume_diff / volume_vol1)

    results = results._append({"Label": i, "Volume 1": volume_vol1, "Volume 2": volume_vol2,"Volume Difference": volume_diff, "Volume Difference (%)": volume_diff_percent}, ignore_index=True)
    print("---")

print(results)
results.to_csv('volume_differences_resampled_2455.csv', index=False)
