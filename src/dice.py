import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from pyNiftyReg.utils import dice_coef, list_nii_gz_files

if __name__ == "__main__":
    ids = [2455, 4669, 4962, 9492]

    scans_dir = "../data/segmentations/"
    imgs = list_nii_gz_files(scans_dir)
    baseline_imgs = sorted([img for img in imgs if "Y0" in img])
    y2_imgs = sorted([img for img in imgs if "Y2" in img])
    patients = list(zip(y2_imgs, baseline_imgs))

    results = []

    for i in range(len(ids)):

        id = ids[i]
        img_fixed = baseline_imgs[i]
        img_fixed_backwards = y2_imgs[i]

        img_moving_ala = f"output_{id}2/updated_resampled_seg_ala_{id}2.nii.gz"
        img_moving_f3d = f"output_{id}2/updated_resampled_seg_f3d_{id}2.nii.gz"

        img_moving_ala_back = f"output_{id}0/updated_resampled_seg_ala_{id}0.nii.gz"
        img_moving_f3d_back = (
            f"output_{id}0/updated_resampled_seg_f3d_back_{id}0.nii.gz"
        )

        # Compute dice coefficients
        dice_front_aladin = dice_coef(img_fixed, img_moving_ala)
        dice_front_f3d = dice_coef(img_fixed, img_moving_f3d)
        dice_back_aladin = dice_coef(img_fixed_backwards, img_moving_ala_back)
        dice_back_f3d = dice_coef(img_fixed_backwards, img_moving_f3d_back)

        # Store results
        results.append(
            [id, dice_front_aladin, dice_front_f3d, dice_back_aladin, dice_back_f3d]
        )

    # Create a DataFrame
    df = pd.DataFrame(
        results,
        columns=[
            "ID",
            "Dice Front Aladin",
            "Dice Front F3D",
            "Dice Back Aladin",
            "Dice Back F3D",
        ],
    )

    # Calculate means
    front_mean = df[["Dice Front Aladin", "Dice Front F3D"]].mean().mean()
    back_mean = df[["Dice Back Aladin", "Dice Back F3D"]].mean().mean()

    # Calculate standard errors
    front_se = df[["Dice Front Aladin", "Dice Front F3D"]].stack().std() / np.sqrt(
        len(df) * 2
    )
    back_se = df[["Dice Back Aladin", "Dice Back F3D"]].stack().std() / np.sqrt(
        len(df) * 2
    )

    # Calculate confidence intervals using T-distribution
    confidence_level = 0.95
    t_critical = stats.t.ppf((1 + confidence_level) / 2, df=(len(df) * 2) - 1)
    front_margin_of_error = t_critical * front_se
    back_margin_of_error = t_critical * back_se

    front_ci = (front_mean - front_margin_of_error, front_mean + front_margin_of_error)
    back_ci = (back_mean - back_margin_of_error, back_mean + back_margin_of_error)

    # Print confidence intervals
    print(f"Front Dice CI: {front_ci}")
    print(f"Back Dice CI: {back_ci}")

    # Plotting
    plt.figure(figsize=(10, 5))

    # Front Dice CI
    plt.errorbar(
        ["Front"],
        [front_mean],
        yerr=[front_margin_of_error],
        fmt="o",
        label="Front Dice",
        capsize=5,
    )

    # Back Dice CI
    plt.errorbar(
        ["Back"],
        [back_mean],
        yerr=[back_margin_of_error],
        fmt="o",
        label="Back Dice",
        capsize=5,
    )

    plt.title("Confidence Intervals for Dice Coefficients")
    plt.ylabel("Dice Coefficient")
    plt.legend()
    plt.grid(True)
    plt.show()
