from pyNiftyReg.utils import *
import nibabel as nib
from skimage.morphology import thin, remove_small_objects, medial_axis
if __name__ == '__main__':
    seg = load_volume('../data/segmentations/summit-2455-xab_Y0_BASELINE_A_airway.nii.gz')
    sk = medial_axis(seg)
    sk = remove_small_objects(sk, min_size=20)

    
    nib.save(nib.Nifti1Image(sk, np.eye(4)), 'output_24552/skeleton_24552_pasdefo_Y0_ma.nii.gz')

