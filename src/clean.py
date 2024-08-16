import nibabel as nib
import numpy as np
from scipy.ndimage import label

# Load the NIfTI file
nifti_path = "y0_final.nii.gz"
img = nib.load(nifti_path)
data = img.get_fdata()

# Ensure data is binary
binary_data = (data > 0).astype(np.int32)

# Label connected components
labeled_array, num_features = label(binary_data)

# Find the largest connected component
largest_component = 0
largest_size = 0
for component in range(1, num_features + 1):
    component_size = np.sum(labeled_array == component)
    if component_size > largest_size:
        largest_size = component_size
        largest_component = component

# Create a new volume with only the largest component
largest_component_volume = (labeled_array == largest_component).astype(np.int32)

# Save the new volume as a NIfTI file
new_img = nib.Nifti1Image(largest_component_volume, img.affine, img.header)
output_path = "y0_final_clean.nii.gz"
nib.save(new_img, output_path)

print(f"Largest connected component saved to {output_path}")
