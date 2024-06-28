from registrator import Registrator
import os

class Aladin(Registrator):

    def __init__(self):
        super().__init__()
        self.parameters = ' -rigOnly -floLowThr -1000 -refLowThr -1000 -floUpThr 1000 -refUpThr 100  -pad -1000 -maxit 2'
        #self.parameters_dict = {'rigOnly': True, 'floLowThr': True, '1000': True,...}

    def register(self, fixed_image, moving_image):
        #Add destinations
        aff_output_path = 'output_%s.nii.gz' 
        affine_transform_path = 'affine_transform_%s.txt'
        
        affine_command = self.niftyreg_dir + 'reg_aladin -flo ' + moving_image + ' -ref ' + fixed_image + ' -res ' + aff_output_path + ' -aff ' + affine_transform_path + self.parameters
        os.system(affine_command)