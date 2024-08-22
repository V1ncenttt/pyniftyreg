from pyNiftyReg import Transformer, VolumeOperator
from pyNiftyReg.utils import *
import os

def pipeline(baseline, followup, baseline_transform, followup_transform):

    #Create temporary folder
    os.makedirs("temp", exist_ok=True)

    # Step 1: Resample in both ways
    Transformer.resample(baseline, baseline_transform, "temp/baseline_resampled.nii.gz")
    Transformer.resample(followup, followup_transform, "temp/followup_resampled.nii.gz")
    # Step 2: Dilate
    VolumeOperator.dilate("temp/baseline_resampled.nii.gz", "temp/baseline_dilated.nii.gz")
    VolumeOperator.dilate("temp/followup_resampled.nii.gz", "temp/followup_dilated.nii.gz")
    # Step 3: Multiply with non-resampled
    VolumeOperator.multiply("temp/baseline_dilated.nii.gz", baseline, "temp/baseline_union.nii.gz")
    VolumeOperator.multiply("temp/followup_dilated.nii.gz", followup, "temp/followup_union.nii.gz")
    
    # Step 4: Clean
    clean_seg("temp/baseline_union.nii.gz", "temp/baseline_cleaned.nii.gz")
    clean_seg("temp/followup_union.nii.gz", "temp/followup_cleaned.nii.gz")
    # Step 5: Resample again in both ways
    Transformer.resample("temp/baseline_cleaned.nii.gz", baseline_transform, "temp/baseline_final.nii.gz")
    Transformer.resample("temp/followup_cleaned.nii.gz", followup_transform, "temp/followup_final.nii.gz")
    # Step 6: Dilate again
    VolumeOperator.dilate("temp/baseline_final.nii.gz", "temp/baseline_final_dilated.nii.gz")
    VolumeOperator.dilate("temp/followup_final.nii.gz", "temp/followup_final_dilated.nii.gz")
    # Step 7: Multiply with non-resampled again
    VolumeOperator.multiply("temp/baseline_final_dilated.nii.gz", "temp/baseline_cleaned.nii.gz", "temp/baseline_final_union.nii.gz")
    VolumeOperator.multiply("temp/followup_final_dilated.nii.gz", "temp/followup_cleaned.nii.gz", 'temp/followup_final_union.nii.gz')
    # Step 8: Clean again to get the intersection
    clean_seg("temp/baseline_final_union.nii.gz", "temp/baseline_final_cleaned.nii.gz")
    clean_seg("temp/followup_final_union.nii.gz", "temp/followup_final_cleaned.nii.gz")

    # Delete folder
    os.rmdir("temp")


if __name__ == "__main__":
    # First need to get the files etc.
    participants = []
    for participant in participants:
        pipeline()
    