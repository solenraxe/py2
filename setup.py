from setuptools import setup
from Cython.Build import cythonize
from Cython.Distutils import build_ext
from Cython.Build.Dependencies import create_dependency_tree
from distutils.core import Extension

# source ../.ven/bin/activate
# python setup.py build_ext --build-lib=./libraries

ext = Extension(
    "interpreter",
    sources=["cpp/inter.pyx", "cpp/interpreter.cpp"],
    include_dirs=["."],
    language="c++",
)

setup(
    ext_modules=[ext],
    cmdclass={"build_ext": build_ext},
)