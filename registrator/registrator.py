from sys import platform
import os


class Registrator:
    def __init__(self):
        if platform == "linux" or platform == "linux2":
            pass
        elif platform == "darwin":
            self.niftyreg_dir = (
                "/Applications/niftk-18.5.4/NiftyView.app/Contents/MacOS/"
            )
        elif platform == "win32":
            pass

    def set_niftyreg_dir(self, niftyreg_dir):
        self.niftyreg_dir = niftyreg_dir

    def register(self, fixed_image, moving_image):
        raise NotImplementedError

    def register_list(self, images):
        raise NotImplementedError

    def __param_dict_to_str(self, param_dict):
        params = ""
        for param in param_dict:
            if param_dict[param] == True:
                params += " -" + param
            elif isinstance(param_dict[param], str):
                params += " -" + param + " " + param_dict[param]
            elif isinstance(param_dict[param], int):
                params += " -" + param + " " + str(param_dict[param])
                
        return params
                

if __name__ == "__main__":
    Registrator()
