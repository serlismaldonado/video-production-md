#!/usr/bin/env python3
"""
Script para crear una nueva producción audiovisual desde plantilla.
Genera la estructura completa de directorios y archivos markdown.
"""

import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

import yaml


def load_template_config():
    """Cargar configuración de la plantilla."""
    template_dir = Path("templates/production-template")

    config = {
        "template_dir": template_dir,
        "required_files": ["README.md", "metadata.yaml"],
        "required_dirs": [
            "01-preproduccion",
            "02-guion",
            "03-produccion",
            "04-postproduccion",
            "05-archivos",
        ],
    }

    return config


def validate_production_name(name):
    """Validar que el nombre de producción sea válido."""
    if not name or name.strip() == "":
        return False, "El nombre no puede estar vacío"

    # Reemplazar caracteres problemáticos
    cleaned_name = name.strip().replace(" ", "-").replace("/", "-").replace("\\", "-")

    # Verificar que no sea un path
    if "/" in cleaned_name or "\\" in cleaned_name:
        return False, "El nombre no puede contener slashes"

    # Verificar longitud
    if len(cleaned_name) > 100:
        return False, "El nombre es demasiado largo (máx 100 caracteres)"

    return True, cleaned_name


def create_production_structure(production_name, template_config, interactive=True):
    """Crear estructura completa de producción."""

    # Directorio de destino
    productions_dir = Path("productions")
    production_dir = productions_dir / production_name

    # Verificar si ya existe
    if production_dir.exists():
        print(f"❌ Error: La producción '{production_name}' ya existe.")
        return False

    # Crear directorio principal
    try:
        production_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Directorio creado: {production_dir}")
    except Exception as e:
        print(f"❌ Error creando directorio: {e}")
        return False

    # Copiar estructura de plantilla
    template_dir = template_config["template_dir"]

    try:
        # Copiar archivos y directorios
        for item in template_dir.rglob("*"):
            if item.is_file():
                # Calcular ruta relativa
                rel_path = item.relative_to(template_dir)
                dest_path = production_dir / rel_path

                # Crear directorios padres si no existen
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                # Copiar archivo
                shutil.copy2(item, dest_path)
                print(f"  📄 Copiado: {rel_path}")

    except Exception as e:
        print(f"❌ Error copiando plantilla: {e}")
        # Limpiar en caso de error
        shutil.rmtree(production_dir, ignore_errors=True)
        return False

    # Actualizar metadatos básicos
    update_production_metadata(production_dir, production_name)

    # Si es interactivo, solicitar información adicional
    if interactive:
        gather_additional_info(production_dir, production_name)

    return True


def update_production_metadata(production_dir, production_name):
    """Actualizar metadatos básicos de la producción."""

    metadata_file = production_dir / "metadata.yaml"

    if not metadata_file.exists():
        print(f"⚠️  Archivo de metadatos no encontrado: {metadata_file}")
        return

    try:
        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = yaml.safe_load(f)

        # Actualizar información básica
        if metadata and "production" in metadata:
            metadata["production"]["title"] = production_name
            metadata["production"]["working_title"] = production_name

            # Actualizar fechas
            today = datetime.now().strftime("%Y-%m-%d")
            if "timeline" in metadata:
                metadata["timeline"]["concept_start"] = today

            # Actualizar metadatos
            if "metadata" in metadata:
                metadata["metadata"]["project_code"] = (
                    f"PROD-{datetime.now().strftime('%Y%m%d')}"
                )
                metadata["metadata"]["status"] = "preproduction"

        # Actualizar historial de versiones
        if "version_history" not in metadata:
            metadata["version_history"] = []

        metadata["version_history"].append(
            {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "version": "1.0",
                "changes": "Creación de producción desde plantilla",
                "author": os.getenv("USER", "system"),
            }
        )

        # Guardar cambios
        with open(metadata_file, "w", encoding="utf-8") as f:
            yaml.dump(
                metadata,
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )

        print(f"✅ Metadatos actualizados: {metadata_file}")

    except Exception as e:
        print(f"⚠️  Error actualizando metadatos: {e}")


def gather_additional_info(production_dir, production_name):
    """Recopilar información adicional interactivamente."""

    print("\n📝 Información adicional de la producción")
    print("=" * 50)

    metadata_file = production_dir / "metadata.yaml"

    if not metadata_file.exists():
        return

    try:
        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = yaml.safe_load(f)

        if not metadata:
            return

        # Solicitar información básica
        print("\nPor favor, proporciona la siguiente información:")
        print("(Presiona Enter para usar valores por defecto)")

        # Género
        current_genre = metadata.get("production", {}).get("genre", ["Drama"])
        genre_input = input(f"\nGénero(s) [{', '.join(current_genre)}]: ").strip()
        if genre_input:
            metadata["production"]["genre"] = [
                g.strip() for g in genre_input.split(",")
            ]

        # Formato
        current_format = metadata.get("production", {}).get("format", "Cortometraje")
        format_input = input(f"\nFormato [{current_format}]: ").strip()
        if format_input:
            metadata["production"]["format"] = format_input

        # Duración
        current_duration = metadata.get("production", {}).get("duration_minutes", 10)
        duration_input = input(
            f"\nDuración estimada (minutos) [{current_duration}]: "
        ).strip()
        if duration_input and duration_input.isdigit():
            metadata["production"]["duration_minutes"] = int(duration_input)

        # Logline
        current_logline = metadata.get("production", {}).get("logline", "")
        logline_input = input(
            f"\nLogline (línea que resume la historia) [{current_logline}]: "
        ).strip()
        if logline_input:
            metadata["production"]["logline"] = logline_input

        # Director
        current_director = metadata.get("crew", {}).get("director", {}).get("name", "")
        director_input = input(f"\nDirector [{current_director}]: ").strip()
        if director_input:
            if "crew" not in metadata:
                metadata["crew"] = {}
            if "director" not in metadata["crew"]:
                metadata["crew"]["director"] = {}
            metadata["crew"]["director"]["name"] = director_input

        # Productor
        current_producer = metadata.get("crew", {}).get("producer", {}).get("name", "")
        producer_input = input(f"\nProductor [{current_producer}]: ").strip()
        if producer_input:
            if "crew" not in metadata:
                metadata["crew"] = {}
            if "producer" not in metadata["crew"]:
                metadata["crew"]["producer"] = {}
            metadata["crew"]["producer"]["name"] = producer_input

        # Guardar cambios
        with open(metadata_file, "w", encoding="utf-8") as f:
            yaml.dump(
                metadata,
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )

        print(f"\n✅ Información adicional guardada en {metadata_file}")

    except Exception as e:
        print(f"⚠️  Error recopilando información: {e}")


def print_success_message(production_name, production_dir):
    """Mostrar mensaje de éxito con instrucciones."""

    print("\n" + "=" * 60)
    print("🎬 PRODUCCIÓN CREADA EXITOSAMENTE")
    print("=" * 60)

    print(f"\n📁 Nombre: {production_name}")
    print(f"📂 Ubicación: {production_dir}")

    print("\n📋 Estructura creada:")
    print("  ├── README.md                    # Overview de la producción")
    print("  ├── metadata.yaml                # Metadatos estructurados")
    print("  ├── 01-preproduccion/           # Fase de preproducción")
    print("  │   ├── concept.md              # Concepto creativo")
    print("  │   ├── brief.md                # Brief del cliente")
    print("  │   ├── research/               # Investigación")
    print("  │   ├── casting/                # Casting")
    print("  │   └── locations/              # Locaciones")
    print("  ├── 02-guion/                   # Desarrollo de guion")
    print("  │   ├── script/                 # Versiones del guion")
    print("  │   └── storyboard/             # Storyboard")
    print("  ├── 03-produccion/              # Rodaje y producción")
    print("  │   ├── shooting-plan/          # Plan de rodaje")
    print("  │   ├── crew/                   # Equipo")
    print("  │   └── budget/                 # Presupuesto")
    print("  ├── 04-postproduccion/          # Edición y postproducción")
    print("  │   ├── editing/                # Edición")
    print("  │   ├── vfx-sound/              # Efectos y sonido")
    print("  │   └── delivery/               # Entrega")
    print("  └── 05-archivos/                # Documentación y referencias")
    print("      ├── assets/                 # Enlaces a assets")
    print("      ├── contracts/              # Documentos legales")
    print("      └── references/             # Referencias")

    print("\n🚀 Próximos pasos:")
    print("  1. Editar metadata.yaml con información específica")
    print("  2. Completar concept.md con el concepto creativo")
    print("  3. Desarrollar el guion en 02-guion/script/")
    print("  4. Planificar el rodaje en 03-produccion/shooting-plan/")

    print("\n🔧 Comandos útiles:")
    print(f"  cd {production_dir}                    # Navegar a la producción")
    print(f"  code {production_dir}/metadata.yaml    # Editar metadatos")
    print(f"  code {production_dir}/01-preproduccion/concept.md  # Editar concepto")

    print("\n🤖 Integración con LLMs:")
    print("  • Los archivos markdown son fácilmente procesables por IA")
    print("  • Usa scripts/analyze-script.py para análisis de guiones")
    print("  • Los metadatos en YAML permiten búsqueda estructurada")

    print("\n💡 Recuerda:")
    print("  • Mantén actualizado el README.md con el progreso")
    print("  • Usa Git para versionar cambios importantes")
    print("  • Documenta decisiones clave en los archivos correspondientes")


def main():
    """Función principal."""

    print("🎬 Creador de Producciones Audiovisuales")
    print("=" * 50)

    # Cargar configuración de plantilla
    template_config = load_template_config()

    # Verificar que la plantilla exista
    if not template_config["template_dir"].exists():
        print(
            f"❌ Error: No se encuentra la plantilla en {template_config['template_dir']}"
        )
        print("   Asegúrate de que templates/production-template/ existe.")
        return 1

    # Obtener nombre de producción
    if len(sys.argv) > 1:
        production_name = sys.argv[1]
        interactive = False
    else:
        production_name = input("\n📝 Nombre de la nueva producción: ").strip()
        interactive = True

    # Validar nombre
    is_valid, result = validate_production_name(production_name)
    if not is_valid:
        print(f"❌ Error: {result}")
        return 1

    production_name = result

    # Confirmar creación
    if interactive:
        print(f"\n📋 Resumen:")
        print(f"  Nombre: {production_name}")
        print(f"  Ubicación: productions/{production_name}")
        print(f"  Plantilla: {template_config['template_dir']}")

        confirm = input("\n¿Crear producción? (s/n): ").strip().lower()
        if confirm not in ["s", "si", "y", "yes"]:
            print("❌ Creación cancelada.")
            return 0

    # Crear producción
    print(f"\n🛠️  Creando producción: {production_name}")
    print("-" * 40)

    success = create_production_structure(production_name, template_config, interactive)

    if success:
        production_dir = Path("productions") / production_name
        print_success_message(production_name, production_dir)
        return 0
    else:
        print("\n❌ Error creando la producción.")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
