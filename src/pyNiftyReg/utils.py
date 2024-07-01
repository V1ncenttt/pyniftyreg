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

def show_slice_series(imgs, slicenbs):
    num_slices = len(slicenbs)
    rows = (num_slices +3) // 4

    fig, axs = plt.subplots(rows, 4, figsize=(16, 4*rows))

    for i in range(rows*4):
        if i < num_slices:
            img = imgs[i]
            slicenb = slicenbs[i]
            vol = nib.load(img)
            vol_data = vol.get_fdata()
            ax = axs[i//4, i%4] if rows > 1 else axs[i%4]
            ax.imshow(ndi.rotate(vol_data[slicenb], 90), cmap='bone')
            ax.axis('off')
        else:
            fig.delaxes(axs.flatten()[i])

    plt.tight_layout()
    plt.show()