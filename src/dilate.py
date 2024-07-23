from pyNiftyReg.utils import *

if __name__ == '__main__':
    seg = load_volume('../data/segmentations/summit-2455-xab_Y0_BASELINE_A_airway.nii.gz')
    dilated_seg = dilate(seg, iterations=3)
    nib.save(nib.Nifti1Image(dilated_seg.astype(np.int32), np.eye(4)), 'output_24552/dilated_seg_24552_pasdefo_Y0.nii.gz')