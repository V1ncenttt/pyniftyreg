import numpy as np
from scipy.spatial.distance import cdist

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
        
        # Find the closest centroid in centroids2 for each centroid in centroids1
        matches = {}
        for i, label1 in enumerate(baseline_coords):
            closest_idx = np.argmin(distance_matrix[i])
            label2 = followup_labels[closest_idx]
            matches[label1] = label2
        
        return matches


def apply_matching(segmentation, matches):
    """
    Apply the matching to a segmentation.
    :param segmentation: Segmentation to apply the matching to.
    :param matches: Matching to apply.
    :return: Rematched segmentation.
    """
    rematched_segmentation = np.zeros_like(segmentation)
    
    for label1, label2 in matches.items():
        rematched_segmentation[segmentation == label1] = label2
    
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
    # Assuming `binary_volume` is a 3D numpy array where 1 represents the object and 0 represents the background
    binary_volume = np.array([
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 1, 0], [1, 1, 1], [0, 0, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    ])

    centroid = find_centroid(binary_volume)
    print("Centroid:", centroid)



