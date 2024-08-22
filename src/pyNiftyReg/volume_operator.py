"""
Module: operator.py

This module provides a class, Operator,
for performing various image operations using NiftyReg's reg_tools.

- niftyreg_dir (str): Path to the NiftyReg binaries.

- multiply(img1: str, img2: str, output_name: str = None): Multiplies two images.
- add(img1: str, img2: str, output_name: str = None): Adds two images.
- subtract(img1: str, img2: str, output_name: str = None): Subtracts the second
image from the first.
- divide(img1: str, img2: str, output_name: str = None): Divides the first image by the second.
- nan(img: str, mask: str, output_name: str = None): Applies a mask to an image,
setting masked values to NaN.
```
"""

import os


class VolumeOperator:
    """
    A class to perform various image operations using NiftyReg's reg_tools.

    Attributes:
    niftyreg_dir (str): Path to the NiftyReg binaries.

    Methods:
    multiply(img1: str, img2: str, output_name: str = None): Multiplies two images.
    add(img1: str, img2: str, output_name: str = None): Adds two images.
    substract(img1: str, img2: str, output_name: str = None): Subtracts the
    second image from the first.
    divide(img1: str, img2: str, output_name: str = None): Divides the first image by the second.
    nan(img: str, mask: str, output_name: str = None): Applies a mask to an image,
    setting masked values to NaN.
    """

    def __init__(self):
        """
        Initializes the Operator class with the path to the NiftyReg binaries.
        """
        self.niftyreg_dir = "../niftk-18.5.4/bin/"

    def multiply(self, img1: str, img2: str, output_name: str = None):
        """
        Multiplies two images using NiftyReg's reg_tools.

        Parameters:
        img1 (str): Path to the first image.
        img2 (str): Path to the second image.
        output_name (str, optional): Path to save the output image. Defaults to None.

        Returns:
        None
        """
        mul_command = self.niftyreg_dir + "reg_tools -in " + img1 + " -mul " + img2
        if output_name:
            mul_command += " -out " + output_name

        os.system(mul_command)

    def add(self, img1: str, img2: str, output_name: str = None):
        """
        Adds two images using NiftyReg's reg_tools.

        Parameters:
        img1 (str): Path to the first image.
        img2 (str): Path to the second image.
        output_name (str, optional): Path to save the output image. Defaults to None.

        Returns:
        None
        """
        add_command = self.niftyreg_dir + "reg_tools -in " + img1 + " -add " + img2
        if output_name:
            add_command += " -out " + output_name

        os.system(add_command)

    def substract(self, img1: str, img2: str, output_name: str = None):
        """
        Subtracts the second image from the first using NiftyReg's reg_tools.

        Parameters:
        img1 (str): Path to the first image.
        img2 (str): Path to the second image.
        output_name (str, optional): Path to save the output image. Defaults to None.

        Returns:
        None
        """
        substract_command = (
            self.niftyreg_dir + "reg_tools -in " + img1 + " -sub " + img2
        )
        if output_name:
            substract_command += " -out " + output_name

        os.system(substract_command)

    def divide(self, img1: str, img2: str, output_name: str = None):
        """
        Divides the first image by the second using NiftyReg's reg_tools.

        Parameters:
        img1 (str): Path to the first image.
        img2 (str): Path to the second image.
        output_name (str, optional): Path to save the output image. Defaults to None.

        Returns:
        None
        """
        divide_command = self.niftyreg_dir + "reg_tools -in " + img1 + " -div " + img2
        if output_name:
            divide_command += " -out " + output_name

        os.system(divide_command)

    def nan(self, img: str, mask: str, output_name: str = None):
        """
        Applies a mask to an image, setting masked values to NaN using NiftyReg's reg_tools.

        Parameters:
        img (str): Path to the image.
        mask (str): Path to the mask.
        output_name (str, optional): Path to save the output image. Defaults to None.
        """
        nan_command = self.niftyreg_dir + "reg_tools -in " + img + " -nan " + mask
        if output_name:
            nan_command += " -out " + output_name

        os.system(nan_command)
