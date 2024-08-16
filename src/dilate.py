from pyNiftyReg.utils import *

ITERS = 3

if __name__ == "__main__":
    seg = "y2_inter_clean_resampled.nii.gz"
    output_name = seg.split(".")[0] + "_dilated_%s.nii.gz" % ITERS
    vol = load_volume(seg)
    aff = nib.load(seg).affine
    dilated_vol = dilate(vol, iterations=ITERS)
    nib.save(nib.Nifti1Image(dilated_vol.astype(np.int32), aff), output_name)
    """
    segs_dir = "../data/segmentations/"
    segs = list_nii_gz_files(segs_dir)
    baseline_segs = sorted([seg for seg in segs if "Y0" in seg])
    y2_segs = sorted([seg for seg in segs if "Y2" in seg])
    patients = list(zip(baseline_segs, y2_segs))

    original_nifti = nib.load('../data/segmentations/summit-2455-xab_Y2_airway.nii.gz')
    original_affine = original_nifti.affine
    
    for patient in patients:
        identifier = "".join([ele for ele in patient[0] if ele.isdigit()])[:-1]

        registered_seg = 'output_%s2/updated_resampled_seg_f3d_%s2.nii.gz' % (identifier, identifier)
        registered_seg_back = 'output_%s0/updated_resampled_seg_f3d_back_%s0.nii.gz' % (identifier, identifier)

        baseline_seg = patient[0]
        y2_seg = patient[1]

        for seg in [registered_seg, registered_seg_back, baseline_seg, y2_seg]:
            if not seg.startswith('../'):
                output_name = seg.split('.')[0] + '_dilated_%s.nii.gz' % ITERS
            else:
                output_name = seg.split('/')[-1].split('.')[0] + '_dilated_%s.nii.gz' % ITERS

            print(seg)
            print(output_name)
            print('---')

            vol = load_volume(seg)
            aff = nib.load(seg).affine
            dilated_vol = dilate(vol, iterations=ITERS)
            nib.save(nib.Nifti1Image(dilated_vol.astype(np.int32), aff), output_name)
                                 
        """
