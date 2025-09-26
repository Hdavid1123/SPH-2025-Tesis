from setuptools import setup, Extension
import pybind11
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

ext_modules = [
    Extension(
        "initial_particles_builder",
        sources=[
            str(Path("particleCppBuilder.cpp")),  # <-- único archivo C++ en esta carpeta
        ],
        include_dirs=[
            pybind11.get_include(),
            pybind11.get_include(user=True),
            str(project_root / "data_structures"),  # para particle.h, cell.h, etc.
        ],
        language="c++",
        extra_compile_args=["-std=c++17"],
    ),
]

setup(
    name="initial_particles_builder",
    version="0.1",
    description="Módulo de inicialización de partículas (Pybind11 + C++)",
    ext_modules=ext_modules,
)
