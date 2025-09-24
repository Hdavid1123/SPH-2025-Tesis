from setuptools import setup, Extension
import pybind11

ext_modules = [
    # Módulo común para kernels
     Extension(
        "algoritms.kernels.common.common",
        sources=[
            "algoritms/kernels/common/bindings.cpp",
        ],
        include_dirs=[
            pybind11.get_include(),
            "algoritms/kernels/common"
        ],
        language="c++",
        extra_compile_args=["-std=c++17"],
    ),
    # Módulo para el kernel cúbico spline
    Extension(
        "algoritms.kernels.cubic_spline.cubicSplineKernel",
        sources=[
            "algoritms/kernels/cubic_spline/bindings.cpp",
            "algoritms/kernels/cubic_spline/cubicSplineKernel.cpp",
        ],
        include_dirs=[
            pybind11.get_include(),
            "algoritms/kernels"
        ],
        language="c++",
        extra_compile_args=["-std=c++17"],
    ),
    # Módulo para el kernel Wendland
    Extension(
        "algoritms.kernels.wendland.wendlandKernel",
        sources=[
            "algoritms/kernels/wendland/bindings.cpp",
            "algoritms/kernels/wendland/wendlandKernel.cpp",
        ],
        include_dirs=[
            pybind11.get_include(),
            "algoritms/kernels"
        ],
        language="c++",
        extra_compile_args=["-std=c++17"],
    ),
]

setup(
    name="algoritms",
    version="0.1",
    packages=["algoritms", "algoritms.kernels", "algoritms.kernels.common",
              "algoritms.kernels.cubic_spline", "algoritms.kernels.wendland"],
    ext_modules=ext_modules,
)
