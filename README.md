<p align="center">
  <a href="" rel="noopener">
 <img height=100px src="img/niftyreg.jpg" alt="Project logo"></a>
</p>

<h3 align="center">PyNiftyReg</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]
[![GitHub Issues](https://img.shields.io/github/issues/V1ncenttt/pyniftyreg)]
[![License](https://img.shields.io/github/license/V1ncenttt/pyniftyreg)](/LICENSE)

</div>

---

<p align="center"> PyNiftyReg is a robust Python wrapper designed to simplify the integration of NiftyReg’s powerful executables into your Python projects. This library enables seamless interaction with NiftyReg’s image registration and transformation tools, allowing you to harness their full potential directly from your Python code.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [TODO](../TODO.md)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

PyNiftyReg is a comprehensive Python wrapper designed to facilitate the integration and utilization of the NiftyReg library, a suite of tools for performing robust image registration and transformation tasks. This wrapper aims to bridge the gap between the powerful capabilities of NiftyReg and the flexibility and ease of use offered by Python, making advanced image registration techniques more accessible to researchers and developers in medical imaging, computer vision, and related fields.

With PyNiftyReg, users can effortlessly configure and execute various image registration algorithms, including the renowned Aladin and F3D algorithms, directly from their Python code. The library provides a simplified interface for setting up registration parameters, executing the registration process, and handling the output, all while maintaining the precision and efficiency NiftyReg is known for.

Whether you're working on registring medical scans, performing image analysis, or developing computer vision applications, PyNiftyReg offers a powerful yet user-friendly solution to incorporate state-of-the-art image registration capabilities into your projects.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them.

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running.

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo.


## 🎈 Usage <a name="usage"></a>

Here is an example use of pyNiftyReg.

```python 
from pyNiftyreg import Aladin, F3d

# Example of using PyNiftyReg for image registration
fixed_image = 'path/to/fixed_image.nii'
moving_image = 'path/to/moving_image.nii'
output_image = 'path/to/output_image.nii'

al = Aladin()
f3d = F3d()

al.register(fixed_image, moving_image)
f3d.register(fixed_image, moving_image)
```
You can also use pyNiftyReg to transform images using deformation fields, and multipy/add/divide images together.
## ✍️ Authors <a name = "authors"></a>

- [@V1ncenttt](https://github.com/V1ncenttt) - Initial work

See also the list of [contributors](https://github.com/V1ncenttt/cmic_registeration/contributors) who participated in this project.

