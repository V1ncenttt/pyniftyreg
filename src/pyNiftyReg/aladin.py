import os
from pyNiftyReg.registrator import Registrator


class Aladin(Registrator):
    """
    A subclass of Registrator for performing image registration
    using the Aladin algorithm.

    This class provides an interface for setting up and executing
    the Aladin registration algorithm, part of the NiftyReg suite.
    It allows for the configuration of various parameters specific
    to the Aladin algorithm and executes the registration process
    by constructing a command line command and executing it in the system's shell.

    Attributes:
        parameters_dict (dict): A dictionary holding the parameters
        for the Aladin registration process. The keys are parameter names,
        and the values are their corresponding settings.

    Methods:
        __init__: Initializes a new instance of the Aladin class,
        setting up default parameters for the registration.
        set_max_iterations(maxit: int): Sets the maximum number
        of iterations for the registration algorithm.
        register(fixed_image: str, moving_image: str): Executes the Aladin registration algorithm
        with the configured parameters on the specified fixed and moving images.
    """

    def __init__(self):
        """
        Initializes a new instance of the Aladin class 
        with default parameters for the registration process.
        """
        super().__init__()
        self.parameters_dict = {
            "rigOnly": True,
            "floLowThr": -1000,
            "refLowThr": -1000,
            "floUpThr": 1000,
            "refUpThr": 100,
            "pad": -1000,
        }

    def set_max_iterations(self, maxit: int):
        """
        Sets the maximum number of iterations for the Aladin registration algorithm.

        :param maxit: The maximum number of iterations as an integer.
        """
        self.parameters_dict["maxit"] = maxit

    # TODO: add more setters for parameters

    def register(self, fixed_image: str, moving_image: str):
        """
        Executes the Aladin registration algorithm using the configured parameters.

        This method constructs a command line command based on the parameters
        set in the `parameters_dict` and the paths to the fixed and moving images.
        It then executes this command in the system's shell to perform the registration.

        :param fixed_image: The path to the fixed image file.
        :param moving_image: The path to the moving image file.
        """
        #TODO: print statements
        #TODO: Add destinations
        identifier = "".join([ele for ele in moving_image if ele.isdigit()])
        print("^^^^^^^^^^^^^^^^^")
        print(f"REGISTRATION STARTED for patient {identifier} (Aladin)")
        print("^^^^^^^^^^^^^^^^^")

        folder = f"output_{identifier}"
        if not os.path.exists(folder):
            os.makedirs(folder)

       
        

        aff_output_path = './' + folder + '/' + f"ala_output_{identifier}.nii.gz"
        print(aff_output_path)
        affine_transform_path = './' + folder + '/' + f"ala_affine_transform_{identifier}.txt"
        print(affine_transform_path)
        parameters = self._param_dict_to_str(self.parameters_dict)
        print(parameters)
        print(self.parameters_dict)

        affine_command = (
            self.niftyreg_dir
            + "reg_aladin -flo "
            + moving_image
            + " -ref "
            + fixed_image
            + " -res "
            + aff_output_path
            + " -aff "
            + affine_transform_path
            + parameters
        )
        os.system(affine_command)
