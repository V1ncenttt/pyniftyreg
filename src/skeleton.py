from pyNiftyReg.utils import *
import nibabel as nib
if __name__ == '__main__':
    seg = load_volume('../data/segmentations/summit-2455-xab_Y2_airway.nii.gz')
    sk = skeletonise(seg)
    nib.save(nib.Nifti1Image(sk, np.eye(4)), 'output_24552/skeleton_24552_pasdefo_Y2.nii.gz')

