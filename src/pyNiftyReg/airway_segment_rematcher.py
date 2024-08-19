import numpy as np
from scipy.spatial.distance import cdist
import nibabel as nib
import matplotlib.pyplot as plt
class AirwaySegmentRematcher:

    def __init__(self) -> None:
        pass
    
    def get_centroids(self, volume) -> np.ndarray:
        """
        Get the centroids of the airway segmentations in a volume.
        :param volume: Path to the volume.
        :return: Centroids.
        """
        centroids = {}
        
        max_val = int(np.max(volume))

        for i in range(1, max_val + 1):
            # Find the centroid of the segmentation where it is equal to i
            
            # Find the centroid of the segmentation where it is equal to i
            coords = np.argwhere(volume == i)
            centroid = np.mean(coords, axis=0)
            centroids[i] = centroid
        
        return centroids

    
    def centroid_based_matching(self, baseline, followup) -> np.ndarray:
        """
        Rematch the airway segmentations of a baseline and follow-up volume,
        using a centroid-based approach.
        :param baseline: Path to the baseline volume.
        :param followup: Path to the follow-up volume.
        :return: Rematched segmentation.
        """
        baseline_centroids = self.get_centroids(baseline)
        followup_centroids = self.get_centroids(followup)

        baseline_labels = list(baseline_centroids.keys())
        followup_labels = list(followup_centroids.keys())
        
        baseline_coords = np.array([baseline_centroids[label] for label in baseline_labels])
        followup_coords = np.array([followup_centroids[label] for label in followup_labels])
        
        # Compute the distance matrix between the centroids
        distance_matrix = cdist(baseline_coords, followup_coords)
        
        # Now assign each label to its closest match remaining in the set
        # Once a label is matched, it is removed from the set
        # Since the two can have different numbers of labels, we need to keep track of which labels have been matched
        # The remaining will be matched to themselves, and 0 to 0
        matches = {}
        set1 = set(baseline_labels)
        set2 = set(followup_labels)

        # Pick the smallest set to iterate over
        if len(set1) < len(set2):
            set_iter = set1
        else:
            set_iter = set2
        
        while len(set_iter) > 0:
            min_distance = np.inf
            min_pair = None
            
            for label1 in set1:
                for label2 in set2:
                    distance = distance_matrix[label1 - 1, label2 - 1]
                    if distance < min_distance:
                        min_distance = distance
                        min_pair = (label1, label2)
            
            label1, label2 = min_pair
            matches[label1] = label2
            
            set1.remove(label1)
            set2.remove(label2)

        print(matches)
        return matches


    def apply_matching(self, segmentation, matches):
        """
        Apply the matching to a segmentation.
        :param segmentation: Segmentation to apply the matching to.
        :param matches: Matching to apply.
        :return: Rematched segmentation.
        """
        rematched_segmentation = np.zeros_like(segmentation)
        print(segmentation.shape)
        print('----')
        for label1, label2 in matches.items():
            rematched_segmentation[segmentation == label1] = label2
        
        return rematched_segmentation
    
    def rematch(self, baseline, followup) -> np.ndarray:
        """
        Rematch the airway segmentations of a baseline and follow-up volume.
        :param baseline: Path to the baseline volume.
        :param followup: Path to the follow-up volume.
        :return: Rematched segmentation.
        """
        baseline = nib.load(baseline)
        followup = nib.load(followup)
        
        matches = self.centroid_based_matching(baseline.get_fdata(), followup.get_fdata())
        rematched_segmentation = self.apply_matching(baseline.get_fdata(), matches)

        print(rematched_segmentation.shape)
        aff = baseline.affine
        # Save the rematched segmentation
        output_vol = nib.Nifti1Image(rematched_segmentation.astype(np.int32), aff , baseline.header)
        nib.save(output_vol, "rematched_segmentation.nii.gz")
        return rematched_segmentation

def find_centroid(binary_volume):
    # Ensure the input is a numpy array
    binary_volume = np.asarray(binary_volume)
    
    # Find the indices where the binary volume is 1
    indices = np.argwhere(binary_volume == 1)
    
    # Calculate the centroid by taking the mean of these indices along each axis
    centroid = np.mean(indices, axis=0)
    
    return centroid

if __name__ == "__main__":
        # Example usage:
    baseline = '../y0_labeled_resampled.nii.gz'
    followup = '../../data/annotated/y2_final_clean_2455_coloured_airway_refactored_all.nii.gz'
   
    #nib1 = nib.load('rematched_segmentation.nii.gz')
    #d = nib1.get_fdata()
    #print(d.shape)
    #print(d)
    rematcher = AirwaySegmentRematcher()
    rematcher.rematch(baseline, followup)
    



