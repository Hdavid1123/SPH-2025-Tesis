from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import pybind11
import os

ext_modules = []

methods_dir = os.path.dirname(__file__)  # .../algoritms/neighbors
project_root = os.path.abspath(os.path.join(methods_dir, "..", ".."))  # .../SPH-2025-Tesis
algoritms_root = os.path.join(project_root, "algoritms")
kernels_root = os.path.join(algoritms_root, "kernels")

# Buscar automáticamente todos los .cpp dentro de kernels/
kernel_sources = []
for root, _, files in os.walk(kernels_root):
    for f in files:
        if f.endswith(".cpp"):
            kernel_sources.append(os.path.join(root, f))

for method in os.listdir(methods_dir):
    subdir = os.path.join(methods_dir, method)
    if not os.path.isdir(subdir):
        continue

    bindings_path = os.path.join(subdir, "bindings.cpp")
    if os.path.exists(bindings_path):
        cpp_sources = [bindings_path]
        for f in os.listdir(subdir):
            if f.endswith(".cpp") and f != "bindings.cpp":
                cpp_sources.append(os.path.join(subdir, f))

        # Agregamos los kernels para enlazarlos automáticamente
        cpp_sources += kernel_sources

        ext_modules.append(
            Extension(
                f"neighbors_{method}",
                sources=cpp_sources,
                include_dirs=[
                    pybind11.get_include(),
                    pybind11.get_include(user=True),
                    subdir,  # headers locales del método (ej: linkedList.h)
                    os.path.join(project_root, "data_structures"),  # particle.h, cell.h
                    kernels_root,  # headers de kernels
                    algoritms_root,
                ],
                language="c++",
                extra_compile_args=["-std=c++17"],
            )
        )

setup(
    name="neighbors",
    version="0.1",
    description="Distintos métodos de búsqueda de vecinos en C++",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
