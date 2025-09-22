from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "initial_conditions",  # nombre del módulo importable en Python
        ["initialConditionsGenerator.cpp"],
        include_dirs=[pybind11.get_include()],
        language="c++",
    ),
]

setup(
    name="initial_conditions",
    ext_modules=ext_modules,
)
