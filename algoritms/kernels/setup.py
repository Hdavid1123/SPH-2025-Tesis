from setuptools import setup, Extension
import pybind11

ext_modules = [
    # Módulo para el kernel cúbico spline
    Extension(
        "cubic_spline.cubicSplineKernel",
        sources=[
            "cubic_spline/bindings.cpp",
            "cubic_spline/cubicSplineKernel.cpp",
        ],
        include_dirs=[
            pybind11.get_include(),
            ".",                        # kernels
            "../../data_structures"                     # dimension.h
        ],
        language="c++",
        extra_compile_args=["-std=c++17"],
    ),
    # Módulo para el kernel Wendland
    Extension(
        "wendland.wendlandKernel",
        sources=[
            "wendland/bindings.cpp",
            "wendland/wendlandKernel.cpp",
        ],
        include_dirs=[
            pybind11.get_include(),
            ".",                    
            "../../data_structures"      
        ],
        language="c++",
        extra_compile_args=["-std=c++17"],
    ),
]

setup(
    name="kernels",
    version="0.1",
    packages=["algoritms.kernels",
              "algoritms.kernels.cubic_spline",
              "algoritms.kernels.wendland"],
    ext_modules=ext_modules,
)
