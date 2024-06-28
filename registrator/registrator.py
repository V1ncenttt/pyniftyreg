from sys import platform
import os

class Registrator:
    def __init__(self):
        if platform == "linux" or platform == "linux2":
            pass
        elif platform == "darwin":
            self.niftyreg_dir = '/Applications/niftk-18.5.4/NiftyView.app/Contents/MacOS/'
        elif platform == "win32":
            pass
    
    def set_niftyreg_dir(self, niftyreg_dir):
        self.niftyreg_dir = niftyreg_dir
    
    def register(self, fixed_image, moving_image):
        raise NotImplementedError
    
    def register_list(self, images):
        raise NotImplementedError

if __name__ == '__main__':
    Registrator()