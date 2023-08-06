import os
import sys
from numpy.distutils.core import Extension, setup

__author__ = "Anders S. Christensen"
__copyright__ = "Copyright 2016"
__credits__ = ["Anders S. Christensen (2016) https://github.com/qmlcode/qml"]
__license__ = "MIT"
__version__ = "0.2.5"
__maintainer__ = "Anders S. Christensen"
__email__ = "andersbiceps@gmail.com"
__status__ = "Beta"
__description__ = "Quantum Machine Learning"
__url__ = "https://github.com/qmlcode/qml"


FORTRAN = "f90"

# GNU (default)
COMPILER_FLAGS = ["-O3", "-fopenmp", "-m64", "-march=native", "-fPIC"]
LINKER_FLAGS = ["-lgomp"]
MATH_LINKER_FLAGS = ["-lblas", "-llapack"]

# For clang without OpenMP: (i.e. most Apple/mac system)
if sys.platform == "darwin" and all(["gnu" not in arg for arg in sys.argv]):
    COMPILER_FLAGS = ["-O3", "-m64", "-march=native", "-fPIC"]
    LINKER_FLAGS = []
    MATH_LINKER_FLAGS = ["-lblas", "-llapack"]


# Intel
if any(["intelem" in arg for arg in sys.argv]):
    COMPILER_FLAGS = ["-xHost", "-O3", "-axAVX", "-qopenmp"]
    LINKER_FLAGS = ["-liomp5", " -lpthread", "-lm", "-ldl"]
    MATH_LINKER_FLAGS = ["-L${MKLROOT}/lib/intel64", "-lmkl_rt"]


# UNCOMMENT TO FORCE LINKING TO MKL with GNU compilers:
# LINKER_FLAGS = ["-lgomp", " -lpthread", "-lm", "-ldl"]
# MATH_LINKER_FLAGS = ["-L${MKLROOT}/lib/intel64", "-lmkl_rt"]


ext_farad_kernels = Extension(name = 'farad_kernels',
                          sources = ['src/farad_kernels.f90'],
                          extra_f90_compile_args = COMPILER_FLAGS,
                          extra_f77_compile_args = COMPILER_FLAGS,
                          extra_compile_args = COMPILER_FLAGS,
                          extra_link_args = LINKER_FLAGS,
                          language = FORTRAN,
                          f2py_options=['--quiet'])

ext_fcho_solve = Extension(name = 'fcho_solve',
                          sources = ['src/fcho_solve.f90'],
                          extra_f90_compile_args = COMPILER_FLAGS,
                          extra_f77_compile_args = COMPILER_FLAGS,
                          extra_compile_args = COMPILER_FLAGS,
                          extra_link_args = MATH_LINKER_FLAGS + LINKER_FLAGS,
                          language = FORTRAN,
                          f2py_options=['--quiet'])

ext_fdistance = Extension(name = 'fdistance',
                          sources = ['src/fdistance.f90'],
                          extra_f90_compile_args = COMPILER_FLAGS,
                          extra_f77_compile_args = COMPILER_FLAGS,
                          extra_compile_args = COMPILER_FLAGS,
                          extra_link_args = LINKER_FLAGS,
                          language = FORTRAN,
                          f2py_options=['--quiet'])

ext_fkernels = Extension(name = 'fkernels',
                          sources = ['src/fkernels.f90'],
                          extra_f90_compile_args = COMPILER_FLAGS,
                          extra_f77_compile_args = COMPILER_FLAGS,
                          extra_compile_args = COMPILER_FLAGS,
                          extra_link_args = LINKER_FLAGS,
                          language = FORTRAN,
                          f2py_options=['--quiet'])

ext_frepresentations = Extension(name = 'frepresentations',
                          sources = ['src/frepresentations.f90'],
                          extra_f90_compile_args = COMPILER_FLAGS,
                          extra_f77_compile_args = COMPILER_FLAGS,
                          extra_compile_args = COMPILER_FLAGS,
                          extra_link_args = LINKER_FLAGS,
                          language = FORTRAN,
                          f2py_options=['--quiet'])
# Find the absolute path
here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()

def setup_pepytools():

    setup(

        name="qml",

        install_requires=[
            "numpy", 
            "scipy"
        ],

        # metadata
        version=__version__,
        author=__author__,
        author_email=__email__,
        platforms = 'Any',
        description = __description__,
        long_description = long_description,
        keywords = 'Quantum Machine Learning',
        # download_url = "https://github.com/qmlcode/qml/archive/0.2.3.tar.gz",
        url = __url__,

        # set up package contents
        package_dir={'qml': 'src'},
        packages=['qml'],
        ext_package = 'qml',
        ext_modules = [
              ext_farad_kernels,
              ext_fcho_solve,
              ext_fdistance,
              ext_fkernels,
              ext_frepresentations,
        ],
)

if __name__ == '__main__':

    setup_pepytools()
