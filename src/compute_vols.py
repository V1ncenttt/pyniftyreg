from pyNiftyReg.utils import *
import nibabel as nib
import numpy as np
import pandas as pd
vol1 = nib.load('../data/annotated/y0_final_clean_2455_coloured_airway_refactored_all.nii.gz')
vol2 = nib.load('../data/annotated/y2_final_clean_2455_coloured_airway_refactored_all.nii.gz')

max_val = int(np.max(vol1.get_fdata()))
print(f"Max label: {max_val}")
# Get and print all of the  unique values in the volume
unique_vals = np.unique(vol1.get_fdata())
#print(f"Unique values: {unique_vals}")

# Put the results in a pandas dataframe
results = pd.DataFrame(columns=["Label", "Volume Difference", "Volume Difference (%)"])
for i in range(1, max_val + 1):
    print(f"Label {i}")
    volume_diff = np.abs(compute_volume(vol1, i) - compute_volume(vol2, i))
    volume_diff_percent = np.abs(100 * volume_diff / compute_volume(vol1, i))
    #print(f"Volume difference: {volume_diff} mm^3")
    #print(f"Volume difference: {volume_diff_percent} %")
    #print(f"Volume {i}: {np.sum(vol1.get_fdata() == i) * np.prod(vol1.header.get_zooms()) / 1000} cm^3")
    results = results._append({"Label": i, "Volume Difference": volume_diff, "Volume Difference (%)": volume_diff_percent}, ignore_index=True)
    print("---")

print(results)
results.to_csv('volume_differences_2455.xlsx')
