from distutils.core import setup
from distutils.extension import Extension
from Cython.Build  import cythonize

ext_modules=cythonize([Extension("objects",
                                 sources=["src/objects.pyx",
                                          "src/vector.cpp"],
                                 language="c++")])

setup(ext_modules=ext_modules)
