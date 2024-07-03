from sys import platform
import os

class Transformer:
    def __init__(self) -> None:
        if platform in ("linux", "linux2"):
            self.niftyreg_dir = '~/Downloads/niftk-v18.05.4-ubuntu-14.04-x64/niftk-18.5.4/bin/'
        elif platform == "darwin":
            self.niftyreg_dir = (
                "/Applications/niftk-18.5.4/NiftyView.app/Contents/MacOS/"
            )
        elif platform == "win32":
            pass


    def transform(self, fixed_image, moving_image, deformation):
        raise NotImplementedError
    
    def resample(self, ref_image: str, floating_image: str, deformation: str) -> None:
        """
        Resamples an image using a deformation field.
        :param ref_image: Path to the reference image.
        :param floating_image: Path to the floating image.
        :param deformation: Path to the deformation field.
        """
        resample_command = (
            self.niftyreg_dir
            + 'reg_resample -ref '
            + ref_image
            + ' -flo '
            + floating_image
            + ' -trans '
            + deformation
            + ' -res  output_test.nii.gz'
        )
        print(resample_command)
        os.system(resample_command)

    def update_sform(self, image: str, deformation: str) -> None:
        """
        Updates the sform of an image using a deformation field.
        :param image: Path to the image.
        :param deformation: Path to the deformation field.
        """
        update_sform_command = (
            self.niftyreg_dir
            + 'reg_transform -ref '
            + image
            + ' -updSform '
            + deformation
        )
        os.system(update_sform_command)
        
