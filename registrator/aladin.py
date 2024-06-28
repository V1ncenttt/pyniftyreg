import os
from registrator import Registrator


class Aladin(Registrator):

    def __init__(self):
        super().__init__()
        self.parameters_dict = {
                                'rigOnly': True,
                                'floLowThr': '-1000',
                                'refLowThr': '-1000',
                                'floUpThr': '1000',
                                'refUpThr': '100',
                                'pad': '-1000',
                                'maxit': '2'
                                }
        
    def set_param(self, param, value):
        self.parameters_dict[param] = value
    
    def set_max_iterations(self, maxit):
        self.parameters_dict['maxit'] = maxit

    #TODO: add more setters for parameters
    
    def register(self, fixed_image, moving_image):
        # Add destinations
        aff_output_path = "output_%s.nii.gz" % moving_image
        affine_transform_path = "affine_transform_%s.txt" % moving_image
        parameters = self.__param_dict_to_str(self.parameters_dict)
        #TODO: put in a folder?

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

    def register_list(self, images):
        for image_pair in images:
            self.register(image_pair[0], image_pair[1])