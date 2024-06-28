import numpy as np
import os 
#from util import suplementary_functions as sf
import nibabel as nib
import numpy as np
import scipy.ndimage as ndi
from scipy.signal import correlate
import matplotlib.pyplot as plt

def list_nii_gz_files(directory):
    nii_gz_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".nii.gz"):
                nii_gz_files.append(os.path.join(root, file))
    return nii_gz_files

def show_slice(img, slicenb):
    vol = nib.load(img)
    vol_data = vol.get_fdata()
    plt.imshow(ndi.rotate(vol_data[slicenb], 90), cmap='bone')
    plt.axis('off')
    plt.show()

def show_slice_series(img):
    raise NotImplementedError



nifti_dir = ''
niftyreg_dir = '/Applications/niftk-18.5.4/NiftyView.app/Contents/MacOS/'
scans_dir = '../data/nii_dataset/'
# Parameters for the registration
aff_par = ' -rigOnly -floLowThr -1000 -refLowThr -1000 -floUpThr 1000 -refUpThr 100  -pad -1000 -maxit 2'
dir_par = ' -lncc -ln 5 -lp 4 -vel -pad -1000 -maxit 2'


imgs = list_nii_gz_files(scans_dir)
baseline_imgs = sorted([img for img in imgs if 'Y0' in img])
y2_imgs = sorted([img for img in imgs if 'Y2' in img])
patients = list(zip(baseline_imgs, y2_imgs))


for patient in patients:

    source_img = patient[0]
    target_img = patient[1]

    identifier = "".join([ele for ele in patient[0] if ele.isdigit()])
    print('^^^^^^^^^^^^^^^^^')
    print('REGISTRATION STARTED for patient %s' % identifier)
    print('^^^^^^^^^^^^^^^^^')

    aff_output_path = 'output_%s.nii.gz' % identifier
    affine_transform_path = 'affine_transform_%s.txt' % identifier

    def_output_path = 'def_output_%s.nii.gz' % identifier
    cpp_path = 'cpp_%s.nii' % identifier


    affine_command = niftyreg_dir + 'reg_aladin -flo ' + target_img + ' -ref ' + source_img + ' -res ' + aff_output_path + ' -aff ' + affine_transform_path + aff_par
    os.system(affine_command)


    deformable_command = niftyreg_dir + 'reg_f3d -flo ' + target_img + ' -ref ' + source_img + ' -res ' + def_output_path + ' -aff ' + affine_transform_path +  ' -cpp ' + cpp_path + dir_par
    os.system(deformable_command)

    print('^^^^^^^^^^^^^^^^^')
    print('REGISTRATION DONE')
    print('^^^^^^^^^^^^^^^^^')



print('Finito')