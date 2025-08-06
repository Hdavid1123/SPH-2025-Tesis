# initial_conditions/main.py

import sys
from pathlib import Path
import argparse

# Asegurar que el proyecto raíz está en el PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[0]
sys.path.insert(0, str(PROJECT_ROOT))

# Importar funciones disponibles
from boundaries.export import export_boundary_particles

def main():
    parser = argparse.ArgumentParser(description="Herramienta para ejecutar funciones del módulo initial_conditions.")
    parser.add_argument("command", choices=["export_boundaries"], help="Función a ejecutar")
    parser.add_argument("--output", type=str, default="boundary_particles.txt", help="Archivo de salida")
    parser.add_argument("--plot", action="store_true", help="Visualizar el resultado gráficamente")

    args = parser.parse_args()

    if args.command == "export_boundaries":
        export_boundary_particles(output_filename=args.output, visualize=args.plot)

if __name__ == "__main__":
    main()
