from pyNiftyReg import Transformer, VolumeOperator
from pyNiftyReg.utils import *
import os
import shutil


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def multiply_vol(vol1, vol2, output):
    """
    Multiply two volumes
    """
    v1_data = nib.load(vol1).get_fdata()
    v2_data = nib.load(vol2).get_fdata()
    result = v1_data * v2_data
    output_vol = nib.Nifti1Image(result, nib.load(vol1).affine, nib.load(vol1).header)
    nib.save(output_vol, output)


def pipeline(baseline, followup, baseline_transform, followup_transform):

    # Create temporary folder
    os.makedirs("temp", exist_ok=True)

    try:
        tr = Transformer()
        vo = VolumeOperator()
        # Step 1: Resample in both ways
        print(bcolors.BOLD + bcolors.OKGREEN + "Step 1/8 : Resampling" + bcolors.ENDC)
        tr.resample(
            followup, baseline, baseline_transform, "temp/baseline_resampled.nii.gz"
        )
        tr.resample(
            baseline, followup, followup_transform, "temp/followup_resampled.nii.gz"
        )

        # Step 2: Dilate
        print(bcolors.BOLD + bcolors.OKGREEN + "Step 2/8 : Dilating" + bcolors.ENDC)
        dilate_vol("temp/baseline_resampled.nii.gz", "temp/baseline_dilated.nii.gz")
        dilate_vol("temp/followup_resampled.nii.gz", "temp/followup_dilated.nii.gz")

        # Step 3: Multiply with non-resampled
        print(bcolors.BOLD + bcolors.OKGREEN + "Step 3/8 : Multiplying" + bcolors.ENDC)
        multiply_vol(
            "temp/followup_dilated.nii.gz", baseline, "temp/baseline_union.nii.gz"
        )
        multiply_vol(
            "temp/baseline_dilated.nii.gz", followup, "temp/followup_union.nii.gz"
        )

        # Step 4: Clean
        print(bcolors.BOLD + bcolors.OKGREEN + "Step 4/8 : Cleaning" + bcolors.ENDC)
        clean_seg("temp/baseline_union.nii.gz", "temp/baseline_cleaned.nii.gz")
        clean_seg("temp/followup_union.nii.gz", "temp/followup_cleaned.nii.gz")

        # Step 5: Resample again in both ways OK
        print("Step 5/8 : Resampling again")
        tr.resample(
            followup,
            "temp/baseline_cleaned.nii.gz",
            baseline_transform,
            "temp/baseline_final.nii.gz",
        )
        tr.resample(
            baseline,
            "temp/followup_cleaned.nii.gz",
            followup_transform,
            "temp/followup_final.nii.gz",
        )

        # Step 6: Dilate again
        print("Step 6/8 : Dilating again")
        dilate_vol("temp/baseline_final.nii.gz", "temp/baseline_final_dilated.nii.gz")
        dilate_vol("temp/followup_final.nii.gz", "temp/followup_final_dilated.nii.gz")

        # Step 7: Multiply with non-resampled again
        print("Step 7/8 : Multiplying again")
        multiply_vol(
            "temp/followup_final_dilated.nii.gz",
            "temp/baseline_cleaned.nii.gz",
            "temp/baseline_final_union.nii.gz",
        )
        multiply_vol(
            "temp/baseline_final_dilated.nii.gz",
            "temp/followup_cleaned.nii.gz",
            "temp/followup_final_union.nii.gz",
        )

        # Step 8: Clean again to get the intersection
        print("Step 8/8 : Cleaning again")
        clean_seg(
            "temp/baseline_final_union.nii.gz", "pipeline_baseline_final_cleaned.nii.gz"
        )
        clean_seg(
            "temp/followup_final_union.nii.gz", "pipeline_followup_final_cleaned.nii.gz"
        )

        # Delete folder
        shutil.rmtree("temp")
        print("Done!")

    except Exception as e:
        print(e)
        shutil.rmtree("temp")


if __name__ == "__main__":
    # First need to get the files etc.
    baseline = "../data/segmentations/summit-4669-sup_Y0_BASELINE_A_airway.nii.gz"
    followup = "../data/segmentations/summit-4669-sup_Y2_airway.nii.gz"
    baseline_transform = "output_46692/f3d_cpp_46692.txt.nii"
    followup_transform = "output_46692/f3d_cpp_46692.txt_backward.nii"

    pipeline(baseline, followup, followup_transform, baseline_transform)
