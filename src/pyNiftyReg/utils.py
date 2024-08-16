import os
import nibabel as nib
import numpy as np
import scipy.ndimage as ndi
import matplotlib.pyplot as plt
from skimage import morphology, measure
from scipy.ndimage import binary_dilation, binary_erosion
import scipy
from scipy.ndimage import label


def show_slice(img: str, slicenb: int) -> None:
    """
    Display a single slice from a NIfTI image.

    Parameters:
    img (str): Path to the NIfTI image file.
    slicenb (int): Slice number to display.

    Returns:
    None
    """

    vol = nib.load(img)
    vol_data = vol.get_fdata()
    plt.imshow(ndi.rotate(vol_data[slicenb], 90), cmap="bone")
    plt.axis("off")
    plt.show()


def show_slice_series(imgs: list, slicenbs: list) -> None:
    """
    Display a series of slices from multiple NIfTI images.

    Parameters:
    imgs (list of str): List of paths to NIfTI image files.
    slicenbs (list of int): List of slice numbers to display for each image.

    Returns:
    None
    """

    num_slices = len(slicenbs)
    rows = (num_slices + 3) // 4

    fig, axs = plt.subplots(rows, 4, figsize=(16, 4 * rows))

    for i in range(rows * 4):
        if i < num_slices:
            img = imgs[i]
            slicenb = slicenbs[i]
            vol = nib.load(img)
            vol_data = vol.get_fdata()
            ax = axs[i // 4, i % 4] if rows > 1 else axs[i % 4]
            ax.imshow(ndi.rotate(vol_data[slicenb], 90), cmap="bone")
            ax.axis("off")
        else:
            fig.delaxes(axs.flatten()[i])

    plt.tight_layout()
    plt.show()


def load_volume(img: str) -> np.ndarray:
    """
    Load a NIfTI image and return its data.

    Parameters:
    img (str): Path to the NIfTI image file.

    Returns:
    numpy.ndarray: The image data.
    """

    vol = nib.load(img)
    vol_data = vol.get_fdata()
    return vol_data


def skeletonise(segmentation: np.ndarray) -> np.ndarray:
    """
    Perform skeletonization on a binary segmentation.

    Parameters:
    segmentation (numpy.ndarray): Binary segmentation image.

    Returns:
    numpy.ndarray: Skeletonized image.
    """

    skeleton = morphology.skeletonize(segmentation, method="lee")
    return skeleton


def visualise_skeleton(skeleton: np.ndarray) -> None:
    """
    Visualize the skeleton of a binary image.

    Parameters:
    skeleton (numpy.ndarray): Skeletonized binary image.

    Returns:
    None
    """

    contours = measure.find_contours(skeleton, 0.5)
    fig, ax = plt.subplots()
    ax.imshow(skeleton[100, :, :], cmap=plt.cm.gray)

    for contour in contours:
        ax.plot(contour[:, 1], contour[:, 0], linewidth=2)
    plt.show()


def dice_coef(image1: str, image2: str) -> float:
    """
    Compute the Dice coefficient between two NIfTI images.

    Parameters:
    image1 (str): Path to the first NIfTI image file.
    image2 (str): Path to the second NIfTI image file.

    Returns:
    float: Dice coefficient.
    """

    img1 = nib.load(image1).get_fdata()
    img2 = nib.load(image2).get_fdata()

    img1 = img1.flatten()
    img2 = img2.flatten()

    return 1 - scipy.spatial.distance.dice(img1, img2)


def list_nii_gz_files(directory: str) -> list:
    """
    List all .nii.gz files in a directory and its subdirectories.

    Parameters:
    directory (str): Path to the directory.

    Returns:
    list of str: List of paths to .nii.gz files.
    """

    nii_gz_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".nii.gz"):
                nii_gz_files.append(os.path.join(root, file))
    return nii_gz_files


def dilate(segmentation: np.ndarray, iterations: int = 1) -> np.ndarray:
    """
    Perform binary dilation on a segmentation image.

    Parameters:
    segmentation (numpy.ndarray): Binary segmentation image.
    iterations (int): Number of dilation iterations.

    Returns:
    numpy.ndarray: Dilated image.
    """

    dilated = binary_dilation(segmentation, iterations=iterations)
    return dilated


def erode(segmentation: np.ndarray, iterations: int = 1) -> np.ndarray:
    """
    Perform binary erosion on a segmentation image.

    Parameters:
    segmentation (numpy.ndarray): Binary segmentation image.
    iterations (int): Number of erosion iterations.

    Returns:
    numpy.ndarray: Eroded image.
    """

    eroded = binary_erosion(segmentation, iterations=iterations)
    return eroded


def clean_seg(seg_path: str, output_path: str) -> None:
    """
    Clean a segmentation by keeping only the largest connected component.

    Parameters:
    seg_path (str): Path to the input NIfTI segmentation file.
    output_path (str): Path to save the cleaned segmentation file.

    Returns:
    None
    """

    # Load the NIfTI file
    img = nib.load(seg_path)
    data = img.get_fdata()

    # Ensure data is binary
    binary_data = (data > 0).astype(np.int32)

    # Label connected components
    labeled_array, num_features = label(binary_data)

    # Find the largest connected component
    largest_component = 0
    largest_size = 0
    for component in range(1, num_features + 1):
        component_size = np.sum(labeled_array == component)
        if component_size > largest_size:
            largest_size = component_size
            largest_component = component

    # Create a new volume with only the largest component
    largest_component_volume = (labeled_array == largest_component).astype(np.int32)

    # Save the new volume as a NIfTI file
    new_img = nib.Nifti1Image(largest_component_volume, img.affine, img.header)
    nib.save(new_img, output_path)

    print(f"Largest connected component saved to {output_path}")


def compute_volume(vol: nib.Nifti1Image, nb: int) -> float:
    """
    Compute the volume of a specific label in a NIfTI image.

    Parameters:
    vol (nibabel.Nifti1Image): NIfTI image object.
    nb (int): Label number to compute the volume for.

    Returns:
    float: Volume of the specified label in cubic millimeters.
    """

    voxel_size = vol.header.get_zooms()
    vol_data = vol.get_fdata()

    return np.sum(vol_data == nb) * np.prod(voxel_size)
