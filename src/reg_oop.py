from pyNiftyReg import Aladin
from pyNiftyReg import F3d
from pyNiftyReg.utils import list_nii_gz_files
import os


if __name__ == "__main__":

    al = Aladin()
    f3d = F3d()

    scans_dir = "../data/nii_dataset/"

    imgs = list_nii_gz_files(scans_dir)
    baseline_imgs = sorted([img for img in imgs if "Y0" in img])
    y2_imgs = sorted([img for img in imgs if "Y2" in img])
    patients = list(zip(y2_imgs, baseline_imgs))

    # al.register_list(patients)
    al.register_list(patients)
