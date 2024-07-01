from pyNiftyReg import Aladin
from pyNiftyReg import F3d

import os

def list_nii_gz_files(directory):
    nii_gz_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".nii.gz"):
                nii_gz_files.append(os.path.join(root, file))
    return nii_gz_files

if __name__ == '__main__':
    
    al = Aladin()
    f3d = F3d()

    niftyreg_dir = '/Applications/niftk-18.5.4/NiftyView.app/Contents/MacOS/'
    scans_dir = '../data/nii_dataset/'

    imgs = list_nii_gz_files(scans_dir)
    baseline_imgs = sorted([img for img in imgs if 'Y0' in img])
    y2_imgs = sorted([img for img in imgs if 'Y2' in img])
    patients = list(zip(baseline_imgs, y2_imgs))

    
    # al.register_list(patients)
    f3d.register_list(patients)
    
    

