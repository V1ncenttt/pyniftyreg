from sys import platform


class Registrator:
    """
    A class to handle image/volume registration processes using NiftyReg,
    supporting different platforms. It allows setting parameters
    for the registration process and executing the registration.
    """

    def __init__(self):
        """
        Initializes the Registrator class, setting up the environment based on the operating system.
        """
        self.parameters_dict = {}

        if platform in ("linux", "linux2"):
            self.niftyreg_dir = '~/Downloads/niftk-v18.05.4-ubuntu-14.04-x64/niftk-18.5.4/bin/'
        elif platform == "darwin":
            self.niftyreg_dir = (
                "/Applications/niftk-18.5.4/NiftyView.app/Contents/MacOS/"
            )
        elif platform == "win32":
            pass

    def set_niftyreg_dir(self, niftyreg_dir: str):
        """
        Sets the directory where NiftyReg tools are located.

        :param niftyreg_dir: The directory path as a string.
        """
        self.niftyreg_dir = niftyreg_dir

    def register(self, fixed_image, moving_image):
        """
        Placeholder for the actual registration method. Raises NotImplementedError.

        :param fixed_image: Path to the fixed image.
        :param moving_image: Path to the moving image.
        """
        raise NotImplementedError

    def register_list(self, images: list):
        """
        Registers a list of image pairs.

        :param images: A list of tuples, each containing paths to the fixed and moving images.
        """
        for image_pair in images:
            self.register(image_pair[0], image_pair[1])

    def _param_dict_to_str(self, param_dict: dict):
        """
        Converts a dictionary of parameters into a string format suitable for command line usage.

        :param param_dict: A dictionary of parameters.
        :return: A string of parameters formatted for command line usage.
        """
        params = ""
        for param in param_dict:
            
            if param_dict[param] and isinstance(param_dict[param], bool):
                params += " -" + param
            elif isinstance(param_dict[param], str):
                params += " -" + param + " " + param_dict[param]
            elif isinstance(param_dict[param], int):
                params += " -" + param + " " + str(param_dict[param])

        return params

    def set_param(self, param: str, value):
        """
        Sets a parameter for the registration process.

        :param param: The name of the parameter.
        :param value: The value of the parameter.
        """
        # TODO: prevent from command line injections
        self.parameters_dict[param] = value


if __name__ == "__main__":
    Registrator()
