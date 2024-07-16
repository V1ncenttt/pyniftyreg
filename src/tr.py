from pyNiftyReg import Transformer
import os

def list_nii_gz_files(directory):
    nii_gz_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".nii.gz"):
                nii_gz_files.append(os.path.join(root, file))
    return nii_gz_files

if __name__ == "__main__":
    
    segs_dir = '../data/segmentations/'
    segs = list_nii_gz_files(segs_dir)
    baseline_segs = sorted([seg for seg in segs if 'Y0' in seg])
    y2_segs = sorted([seg for seg in segs if 'Y2' in seg])
    patients = list(zip(baseline_segs, y2_segs))

    transformer = Transformer()

    for patient in patients:
        print('---')
        identifier = "".join([ele for ele in patient[0] if ele.isdigit()])
        fixed = patient[0]
        moving = patient[1]
        aff_deformation = ('output_%s/ala_affine_transform_%s.txt' % (identifier, identifier)).replace('0', '2')
        f3d_def = ('output_%s/f3d_cpp_%s.txt.nii' % (identifier, identifier)).replace('0', '2')
        output_name = ('output_%s/updated_resampled_seg_f3d_%s.nii.gz' % (identifier, identifier)).replace('0', '2')
        transformer.resample(fixed, moving, f3d_def, output_name)
        