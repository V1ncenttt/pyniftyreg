from sys import platform
import os


class Transformer:
    def __init__(self) -> None:
        self.niftyreg_dir = "../niftk-18.5.4/bin/"

    def transform(self, fixed_image, moving_image, deformation):
        raise NotImplementedError

    def resample(
        self, ref_image: str, floating_image: str, deformation: str, output_name: str
    ) -> None:
        """
        Resamples an image using a deformation field.
        :param ref_image: Path to the reference image.
        :param floating_image: Path to the floating image.
        :param deformation: Path to the deformation field.
        """
        resample_command = (
            self.niftyreg_dir
            + "reg_resample -ref "
            + ref_image
            + " -flo "
            + floating_image
            + " -trans "
            + deformation
            + " -res "
            + output_name
        )
        print(resample_command)
        os.system(resample_command)

    def update_sform(
        self, image: str, moving_image, deformation: str, output_loc
    ) -> None:
        """
        Updates the sform of an image using a deformation field.
        :param image: Path to the image.
        :param deformation: Path to the deformation field.
        """
        update_sform_command = (
            self.niftyreg_dir
            + "reg_transform -ref "
            + image
            + " -updSform "
            + moving_image
            + " "
            + deformation
            + " "
            + output_loc
        )
        print(update_sform_command)
        os.system(update_sform_command)
