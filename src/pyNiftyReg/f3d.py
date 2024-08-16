"""
A module for performing image registration using the Fast Free-Form Deformation (F3D) algorithm.

This module provides a class, `F3d`, which is a subclass of `Registrator` and serves as an interface
for setting up and executing the F3D registration algorithm. It allows for the configuration
of various parameters specific to the F3D algorithm and executes the registration process
by constructing a command

    parameters_dict (dict): A dictionary holding the parameters for the F3D registration process.

    __init__: Initializes a new instance of the F3d class, setting up default parameters
    for the registration.
    set_max_iterations(maxit: int): Sets the maximum number of iterations for the
    registration algorithm.
    register(fixed_image: str, moving_image: str): Executes the F3D registration algorithm
    with the configured parameters on the specified fixed and moving images.

"""

import os
from pyNiftyReg.registrator import Registrator


class F3d(Registrator):
    """
    A subclass of Registrator for performing image registration
    using the Fast Free-Form Deformation (F3D) algorithm>
    From the M. Modat et al. paper:Fast free-form deformation
    using graphics processing units (2010)

    This class provides an interface for setting up and executing
    the F3D registration algorithm, part of the NiftyReg suite.
    It allows for the configuration of various parameters specific to the F3D algorithm
    and executes the registration process by constructing a command
    line command and executing it in the system's shell.

    Attributes:
        parameters_dict (dict): A dictionary holding the parameters
        for the F3D registration process.
        The keys are parameter names, and the values are their corresponding settings.

    Methods:
        __init__: Initializes a new instance of the F3d class, setting up
        default parameters for the registration.
        set_max_iterations(maxit: int): Sets the maximum number of iterations
        for the registration algorithm.
        register(fixed_image: str, moving_image: str): Executes the F3D registration algorithm
        with the configured parameters on the specified fixed and moving images.
    """

    def __init__(self):
        """
        Initializes a new instance of the F3d class
        with default parameters for the registration process.
        """
        super().__init__()
        self.parameters_dict = {
            "lncc": True,
            "ln": 5,
            "lp": 4,
            "vel": True,
            "pad": -1000,
        }

    def set_max_iterations(self, maxit: int):
        """
        Sets the maximum number of iterations for the Fast Free-Form Deformation algorithm.

        :param maxit: The maximum number of iterations as an integer.
        """
        self.parameters_dict["maxit"] = maxit

    def register(self, fixed_image: str, moving_image: str):
        """
        Executes the F3D registration algorithm using the configured parameters.

        This method constructs a command line command based on the parameters
        set in the `parameters_dict` and the paths to the fixed and moving images.
        It then executes this command in the system's shell to perform the registration.

        :param fixed_image: The path to the fixed image file.
        :param moving_image: The path to the moving image file.
        """
        # TODO: reformat names to get identifier but not all uri

        identifier = "".join([ele for ele in moving_image if ele.isdigit()])
        print("^^^^^^^^^^^^^^^^^")
        print(f"REGISTRATION STARTED for patient {identifier} (F3D)")
        print("^^^^^^^^^^^^^^^^^")

        folder = f"output_{identifier}"
        if not os.path.exists(folder):
            os.makedirs(folder)

        def_output_path = folder + "/" + f"f3d_output_{identifier}.nii.gz"
        affine_transform_path = (
            "./" + folder + "/" + f"ala_affine_transform_{identifier}.txt"
        )
        cpp_path = folder + "/" + f"f3d_cpp_{identifier}.txt"
        parameters = self._param_dict_to_str(self.parameters_dict)

        deformable_command = (
            self.niftyreg_dir
            + "reg_f3d -flo "
            + moving_image
            + " -ref "
            + fixed_image
            + " -res "
            + def_output_path
            + " -aff "
            + affine_transform_path
            + " -cpp "
            + cpp_path
            + parameters
        )
        os.system(deformable_command)
