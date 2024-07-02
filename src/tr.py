from pyNiftyReg import Transformer

if __name__ == "__main__":
    transformer = Transformer()
    fixed = '../data/nii_dataset/nii_dataset/summit-2455-xab_Y0_BASELINE_A.nii.gz'
    moving = '../data/nii_dataset/nii_dataset/summit-2455-xab_Y2.nii.gz'
    deformation = 'output_24552/ala_affine_transform_24552.txt'
    transformer.resample(fixed, moving, deformation)