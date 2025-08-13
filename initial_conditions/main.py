# initial_conditions/main.py

import sys
from pathlib import Path
import argparse

# Asegurar que el proyecto raíz está en el PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[0]
sys.path.insert(0, str(PROJECT_ROOT))

# Exportadores individuales
from boundaries.export import export_boundary_particles
from fluid.export import export_fluid_particles

# Función combinadora en utils
from utils.export_all import export_all_particles

# Funciones de summary y io
from utils.summary import generate_summary, save_compact_summary
from utils.io import load_json


def main():
    parser = argparse.ArgumentParser(
        description="Herramienta para exportar partículas de fronteras y fluido."
    )
    parser.add_argument(
        "command",
        choices=["export_boundaries", "export_fluid", "export_all"],
        help="Función a ejecutar"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Nombre del archivo de salida (por defecto depende del comando)"
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Visualizar el resultado gráficamente"
    )

    args = parser.parse_args()

    # Carpeta común de salida
    outputs_dir = PROJECT_ROOT / "outputs"
    outputs_dir.mkdir(exist_ok=True)

    if args.command == "export_boundaries":
        filename = args.output or "boundary_particles.txt"
        export_boundary_particles(output_filename=filename, visualize=args.plot, output_dir=outputs_dir)
        print("[✓] Exportación de fronteras finalizada.")

    elif args.command == "export_fluid":
        filename = args.output or "fluid_particles.txt"
        export_fluid_particles(output_filename=filename, visualize=args.plot, output_dir=outputs_dir)
        print("[✓] Exportación de fluido finalizada.")

    elif args.command == "export_all":
        filename = args.output or "all_particles.txt"
        boundary_parts, fluid_parts = export_all_particles(output_filename=filename, visualize=args.plot)

        # Cargar parámetros
        params_boundary = load_json(PROJECT_ROOT / "parameters" / "boundary_conditions.json")
        params_fluid = load_json(PROJECT_ROOT / "parameters" / "fluid_region.json")

        boundary_data = {
            "particles": [(p["position"][0], p["position"][1]) for p in boundary_parts],
            "spacing": params_boundary.get("trapecio", {}).get("resolucion"),
            "sections": params_boundary.get("sections", []),
            "holes": params_boundary.get("agujeros", [])
        }

        fluid_data = {
            "particles": [(p["position"][0], p["position"][1]) for p in fluid_parts],
            "area": None,
            "h": params_fluid.get("h"),
            "start_pos": tuple(params_fluid.get("vertices", {}).get("inf-izq", (None, None))),
            "end_pos": tuple(params_fluid.get("vertices", {}).get("sup-der", (None, None))),
            "vertices": [
                tuple(params_fluid.get("vertices", {}).get("inf-izq", (None, None))),
                tuple(params_fluid.get("vertices", {}).get("inf-der", (None, None))),
                tuple(params_fluid.get("vertices", {}).get("sup-der", (None, None))),
                tuple(params_fluid.get("vertices", {}).get("sup-izq", (None, None))),
            ]
        }

        generate_summary(boundary_data, fluid_data, params_boundary, params_fluid, outputs_dir)
        save_compact_summary(boundary_data, fluid_data, params_boundary, params_fluid, outputs_dir)


if __name__ == "__main__":
    main()
