import nibabel as nib
import numpy as np
import scipy.ndimage as ndi
import matplotlib.pyplot as plt

def show_slice(img, slicenb):
    vol = nib.load(img)
    vol_data = vol.get_fdata()
    plt.imshow(ndi.rotate(vol_data[slicenb], 90), cmap='bone')
    plt.axis('off')
    plt.show()

def show_slice_series(img):
    raise NotImplementedError