#!/usr/bin/env python3
"""
Script para análisis de guiones usando LLMs.
Analiza estructura, personajes, diálogo, ritmo y genera sugerencias.
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

# Configuración para diferentes proveedores de LLM
LLM_CONFIG = {
    "openai": {
        "api_key_env": "OPENAI_API_KEY",
        "model": "gpt-4",
        "temperature": 0.7,
    },
    "anthropic": {
        "api_key_env": "ANTHROPIC_API_KEY",
        "model": "claude-3-sonnet-20240229",
        "temperature": 0.7,
    },
    "local": {
        "api_key_env": None,
        "model": "local",
        "temperature": 0.7,
    },
}


class ScriptAnalyzer:
    """Analizador de guiones en formato markdown."""

    def __init__(self, script_path: Path, llm_provider: str = "openai"):
        self.script_path = script_path
        self.llm_provider = llm_provider
        self.script_content = ""
        self.metadata = {}
        self.analysis_results = {}

        # Verificar que el archivo exista
        if not script_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {script_path}")

    def load_script(self) -> bool:
        """Cargar contenido del guion."""
        try:
            with open(self.script_path, "r", encoding="utf-8") as f:
                self.script_content = f.read()
            return True
        except Exception as e:
            print(f"❌ Error cargando guion: {e}")
            return False

    def extract_metadata(self) -> Dict[str, Any]:
        """Extraer metadatos del guion."""
        metadata = {
            "title": "Desconocido",
            "version": "1.0",
            "author": "Desconocido",
            "format": "Cortometraje",
            "estimated_duration": 0,
            "pages": 0,
            "scenes": 0,
            "characters": [],
            "locations": [],
        }

        # Buscar información en encabezados
        title_match = re.search(r"# GUION - (.+)", self.script_content)
        if title_match:
            metadata["title"] = title_match.group(1).strip()

        # Buscar versión
        version_match = re.search(r"## Versión (\d+\.\d+)", self.script_content)
        if version_match:
            metadata["version"] = version_match.group(1)

        # Buscar autor
        author_match = re.search(r"- \*\*Autor\*\*: (.+)", self.script_content)
        if author_match:
            metadata["author"] = author_match.group(1).strip()

        # Buscar formato
        format_match = re.search(r"- \*\*Formato\*\*: (.+)", self.script_content)
        if format_match:
            metadata["format"] = format_match.group(1).strip()

        # Buscar duración
        duration_match = re.search(
            r"- \*\*Duración estimada\*\*: (.+)", self.script_content
        )
        if duration_match:
            try:
                metadata["estimated_duration"] = int(
                    duration_match.group(1).strip().split()[0]
                )
            except Exception:
                pass

        # Contar escenas
        scenes = re.findall(r"## ESCENA \d+", self.script_content)
        metadata["scenes"] = len(scenes)

        # Extraer personajes
        characters_section = re.search(
            r"### PERSONAJES PRINCIPALES\n(.+?)(?:\n###|\n---)",
            self.script_content,
            re.DOTALL,
        )
        if characters_section:
            lines = characters_section.group(1).strip().split("\n")
            metadata["characters"] = [
                line.strip().replace("- ", "").replace("* ", "")
                for line in lines
                if line.strip() and not line.strip().startswith("#")
            ]

        # Extraer locaciones
        locations = set()
        location_matches = re.findall(r"\*\*INT\./EXT\. (.+?) -", self.script_content)
        for match in location_matches:
            locations.add(match.strip())
        metadata["locations"] = list(locations)

        # Estimar páginas (aproximado: 1 página = 55 líneas de guion)
        lines = self.script_content.split("\n")
        dialogue_lines = sum(
            1 for line in lines if re.match(r"^\*\*.+\*\*$", line.strip())
        )
        metadata["pages"] = max(1, dialogue_lines // 55)

        self.metadata = metadata
        return metadata

    def analyze_structure(self) -> Dict[str, Any]:
        """Analizar estructura narrativa."""
        structure = {
            "act_breaks": [],
            "scene_lengths": [],
            "dialogue_ratio": 0,
            "action_ratio": 0,
            "pacing": "medio",
        }

        # Dividir en escenas
        scenes = re.split(r"## ESCENA \d+", self.script_content)[1:]

        if not scenes:
            return structure

        # Calcular longitud de escenas
        scene_lengths = []
        for scene in scenes:
            lines = scene.strip().split("\n")
            scene_lengths.append(len(lines))

        structure["scene_lengths"] = scene_lengths

        # Calcular proporción diálogo/acción
        total_lines = sum(scene_lengths)
        if total_lines > 0:
            dialogue_lines = 0
            action_lines = 0

            for line in self.script_content.split("\n"):
                line = line.strip()
                if re.match(r"^\*\*.+\*\*$", line):  # Diálogo
                    dialogue_lines += 1
                elif line and not line.startswith("#"):  # Acción/descripción
                    action_lines += 1

            structure["dialogue_ratio"] = (
                dialogue_lines / (dialogue_lines + action_lines) * 100
            )
            structure["action_ratio"] = (
                action_lines / (dialogue_lines + action_lines) * 100
            )

        # Determinar ritmo basado en longitud de escenas
        avg_scene_length = sum(scene_lengths) / len(scene_lengths)
        if avg_scene_length < 15:
            structure["pacing"] = "rápido"
        elif avg_scene_length > 30:
            structure["pacing"] = "lento"
        else:
            structure["pacing"] = "medio"

        return structure

    def analyze_characters(self) -> Dict[str, Any]:
        """Analizar personajes y diálogo."""
        characters = {}

        # Extraer todo el diálogo - solo líneas que comienzan con ** y terminan antes de otro ** o línea vacía
        # Excluir cabeceras de escena que también usan **
        dialogue_pattern = (
            r"^\*\*([A-ZÁÉÍÓÚÑ\s]+(?:\([^)]+\))?)\*\*\s*\n(.+?)(?=\n\*\*|\n\n|$)"
        )
        dialogues = re.findall(
            dialogue_pattern, self.script_content, re.MULTILINE | re.DOTALL
        )

        for character, dialogue in dialogues:
            character = character.strip()
            if character not in characters:
                characters[character] = {
                    "dialogue_count": 0,
                    "total_words": 0,
                    "average_words": 0,
                    "scenes": set(),
                }

            characters[character]["dialogue_count"] += 1
            words = len(dialogue.strip().split())
            characters[character]["total_words"] += words

        # Calcular promedios
        for char in characters:
            if characters[char]["dialogue_count"] > 0:
                characters[char]["average_words"] = (
                    characters[char]["total_words"] / characters[char]["dialogue_count"]
                )

        # Ordenar por cantidad de diálogo
        sorted_chars = sorted(
            characters.items(),
            key=lambda x: x[1]["dialogue_count"],
            reverse=True,
        )

        return {
            "character_count": len(characters),
            "main_characters": sorted_chars[:5]
            if len(sorted_chars) >= 5
            else sorted_chars,
            "dialogue_distribution": {
                char: data["dialogue_count"] for char, data in sorted_chars
            },
            "character_analysis": characters,
        }

    def analyze_dialogue(self) -> Dict[str, Any]:
        """Analizar calidad del diálogo."""
        dialogue_analysis = {
            "average_words_per_line": 0,
            "longest_dialogue": {"character": "", "words": 0, "text": ""},
            "shortest_dialogue": {"character": "", "words": 1000, "text": ""},
            "unique_words": set(),
            "readability_score": 0,
        }

        # Extraer diálogo - solo líneas que comienzan con ** y terminan antes de otro ** o línea vacía
        # Excluir cabeceras de escena que también usan **
        dialogue_pattern = (
            r"^\*\*([A-ZÁÉÍÓÚÑ\s]+(?:\([^)]+\))?)\*\*\s*\n(.+?)(?=\n\*\*|\n\n|$)"
        )
        dialogues = re.findall(
            dialogue_pattern, self.script_content, re.MULTILINE | re.DOTALL
        )

        if not dialogues:
            return dialogue_analysis

        total_words = 0
        total_lines = 0

        for character, dialogue in dialogues:
            character = character.strip()
            dialogue_text = dialogue.strip()
            words = len(dialogue_text.split())

            total_words += words
            total_lines += 1

            # Actualizar palabras únicas
            dialogue_analysis["unique_words"].update(dialogue_text.lower().split())

            # Verificar diálogo más largo
            if words > dialogue_analysis["longest_dialogue"]["words"]:
                dialogue_analysis["longest_dialogue"] = {
                    "character": character,
                    "words": words,
                    "text": dialogue_text[:100]
                    + ("..." if len(dialogue_text) > 100 else ""),
                }

            # Verificar diálogo más corto (excluyendo muy cortos)
            if 0 < words < dialogue_analysis["shortest_dialogue"]["words"]:
                dialogue_analysis["shortest_dialogue"] = {
                    "character": character,
                    "words": words,
                    "text": dialogue_text,
                }

        # Calcular promedios
        if total_lines > 0:
            dialogue_analysis["average_words_per_line"] = total_words / total_lines

        # Calcular puntuación de legibilidad simple
        if total_words > 0:
            # Fórmula simplificada: menos palabras por línea = más legible
            words_per_line = total_words / total_lines
            if words_per_line < 8:
                dialogue_analysis["readability_score"] = 90
            elif words_per_line < 12:
                dialogue_analysis["readability_score"] = 70
            elif words_per_line < 16:
                dialogue_analysis["readability_score"] = 50
            else:
                dialogue_analysis["readability_score"] = 30

        return dialogue_analysis

    def generate_llm_analysis(
        self, analysis_type: str = "comprehensive"
    ) -> Optional[str]:
        """Generar análisis usando LLM (placeholder - implementar según API)."""
        # Este es un placeholder. En una implementación real, se conectaría a una API de LLM.

        prompts = {
            "comprehensive": f"""
Analiza el siguiente guion y proporciona feedback detallado:

TÍTULO: {self.metadata.get("title", "Desconocido")}
AUTOR: {self.metadata.get("author", "Desconocido")}
FORMATO: {self.metadata.get("format", "Cortometraje")}
DURACIÓN: {self.metadata.get("estimated_duration", 0)} minutos
ESCENAS: {self.metadata.get("scenes", 0)}
PERSONAJES: {", ".join(self.metadata.get("characters", []))}

Por favor analiza:
1. ESTRUCTURA: ¿Tiene un arco narrativo claro? ¿Los puntos de giro son efectivos?
2. PERSONAJES: ¿Son creíbles? ¿Tienen motivaciones claras?
3. DIÁLOGO: ¿Suena natural? ¿Revela carácter?
4. RITMO: ¿El pacing es apropiado para el género?
5. FORMATO: ¿Sigue convenciones estándar de guion?
6. SUGERENCIAS: 3-5 sugerencias específicas para mejorar.

Responde en español.
""",
            "character_focus": """
Analiza específicamente los personajes del guion:
1. Arcos de personaje
2. Motivaciones y conflictos
3. Diálogo caracterizador
4. Desarrollo a lo largo de la historia
""",
            "structure_focus": """
Analiza específicamente la estructura del guion:
1. Tres actos y puntos de giro
2. Tensión dramática
3. Ritmo y pacing
4. Resolución satisfactoria
""",
        }

        prompt = prompts.get(analysis_type, prompts["comprehensive"])

        # En una implementación real, aquí se haría la llamada a la API
        # Por ahora, retornamos un mensaje indicando que se necesita configuración
        return f"""
⚠️  ANÁLISIS CON LLM (CONFIGURACIÓN REQUERIDA)

Para usar análisis con LLM, configura tu API key:

1. Para OpenAI: export OPENAI_API_KEY='tu-api-key'
2. Para Anthropic: export ANTHROPIC_API_KEY='tu-api-key'

Luego implementa la llamada a la API en generate_llm_analysis().

Prompt que se enviaría:
{prompt[:500]}...
"""

    def generate_report(self, include_llm: bool = False) -> str:
        """Generar reporte completo de análisis."""

        # Realizar análisis
        metadata = self.extract_metadata()
        structure = self.analyze_structure()
        characters = self.analyze_characters()
        dialogue = self.analyze_dialogue()

        # Generar reporte
        report = []
        report.append("# 📊 ANÁLISIS DE GUION")
        report.append(f"**Archivo**: {self.script_path.name}")
        report.append(
            f"**Fecha de análisis**: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        report.append("")

        report.append("## 📋 METADATOS")
        report.append(f"- **Título**: {metadata['title']}")
        report.append(f"- **Autor**: {metadata['author']}")
        report.append(f"- **Versión**: {metadata['version']}")
        report.append(f"- **Formato**: {metadata['format']}")
        report.append(
            f"- **Duración estimada**: {metadata['estimated_duration']} minutos"
        )
        report.append(f"- **Páginas estimadas**: {metadata['pages']}")
        report.append(f"- **Número de escenas**: {metadata['scenes']}")
        report.append(f"- **Locaciones**: {', '.join(metadata['locations'][:5])}")
        if len(metadata["locations"]) > 5:
            report.append(f"  (y {len(metadata['locations']) - 5} más)")
        report.append("")

        report.append("## 🎭 PERSONAJES")
        report.append(f"- **Total de personajes**: {characters['character_count']}")
        report.append("")
        report.append("### Personajes principales (por diálogo):")
        for i, (char, data) in enumerate(characters["main_characters"], 1):
            report.append(
                f"{i}. **{char}**: {data['dialogue_count']} líneas de diálogo"
            )
        report.append("")

        report.append("## 🏗️ ESTRUCTURA")
        report.append(f"- **Ritmo**: {structure['pacing'].capitalize()}")
        report.append(
            f"- **Proporción diálogo/acción**: {structure['dialogue_ratio']:.1f}% / {structure['action_ratio']:.1f}%"
        )
        report.append(
            f"- **Longitud promedio de escenas**: {sum(structure['scene_lengths']) / len(structure['scene_lengths']):.1f} líneas"
        )
        report.append("")

        report.append("### Distribución de longitud de escenas:")
        if structure["scene_lengths"]:
            avg = sum(structure["scene_lengths"]) / len(structure["scene_lengths"])
            min_len = min(structure["scene_lengths"])
            max_len = max(structure["scene_lengths"])
            report.append(f"- **Más corta**: {min_len} líneas")
            report.append(f"- **Más larga**: {max_len} líneas")
            report.append(f"- **Promedio**: {avg:.1f} líneas")
        report.append("")

        report.append("## 💬 DIÁLOGO")
        report.append(
            f"- **Palabras por línea (promedio)**: {dialogue['average_words_per_line']:.1f}"
        )
        report.append(
            f"- **Puntuación de legibilidad**: {dialogue['readability_score']}/100"
        )
        report.append(f"- **Palabras únicas**: {len(dialogue['unique_words'])}")
        report.append("")

        if dialogue["longest_dialogue"]["words"] > 0:
            report.append("### Diálogo más largo:")
            report.append(
                f"- **Personaje**: {dialogue['longest_dialogue']['character']}"
            )
            report.append(f"- **Palabras**: {dialogue['longest_dialogue']['words']}")
            report.append(f'- **Texto**: "{dialogue["longest_dialogue"]["text"]}"')
            report.append("")

        report.append("## 📈 ESTADÍSTICAS CLAVE")
        report.append("```")
        report.append(
            f"Escenas por página: {metadata['scenes'] / max(1, metadata['pages']):.1f}"
        )
        report.append(
            f"Diálogo por personaje (promedio): {sum(c[1]['dialogue_count'] for c in characters['main_characters']) / max(1, characters['character_count']):.1f} líneas"
        )

        # Calcular densidad de diálogo
        if metadata["pages"] > 0:
            total_dialogue = sum(
                c[1]["dialogue_count"] for c in characters["main_characters"]
            )
            report.append(
                f"Densidad de diálogo: {total_dialogue / metadata['pages']:.1f} líneas por página"
            )
            report.append("```")
            report.append("")

            report.append("## 💡 RECOMENDACIONES")
            report.append("")

            # Recomendaciones basadas en análisis
            recommendations = []

            # Recomendaciones de estructura
            if structure["pacing"] == "rápido" and metadata["pages"] > 30:
                recommendations.append(
                    "Considera desarrollar más las escenas clave para mayor impacto emocional"
                )
            elif structure["pacing"] == "lento" and metadata["pages"] < 20:
                recommendations.append(
                    "Podrías acelerar el ritmo eliminando o combinando escenas menos importantes"
                )

            # Recomendaciones de diálogo
            if dialogue["average_words_per_line"] > 15:
                recommendations.append(
                    "El diálogo es bastante largo. Considera dividir líneas largas para mayor naturalidad"
                )
            elif dialogue["average_words_per_line"] < 5:
                recommendations.append(
                    "El diálogo es muy breve. Asegúrate de que los personajes se expresen completamente"
                )

            # Recomendaciones de personajes
            if characters["character_count"] > 8 and metadata["pages"] < 30:
                recommendations.append(
                    "Muchos personajes para pocas páginas. Considera fusionar o eliminar algunos"
                )
            elif characters["character_count"] < 3 and metadata["pages"] > 50:
                recommendations.append(
                    "Pocos personajes para muchas páginas. Podrías desarrollar personajes secundarios"
                )

            # Recomendaciones de formato
            if metadata["scenes"] / max(1, metadata["pages"]) > 3:
                recommendations.append(
                    "Alta densidad de escenas. Verifica que cada escena sea necesaria y contribuya a la historia"
                )
            elif metadata["scenes"] / max(1, metadata["pages"]) < 1:
                recommendations.append(
                    "Baja densidad de escenas. Considera si algunas escenas podrían dividirse para mayor claridad"
                )

            # Añadir recomendaciones al reporte
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    report.append(f"{i}. {rec}")
            else:
                report.append(
                    "El guion tiene buenas proporciones estructurales. Continúa desarrollando según tu visión creativa."
                )
            report.append("")

            # Análisis LLM si se solicita
            if include_llm:
                report.append("## 🤖 ANÁLISIS CON LLM")
                report.append("")
                llm_analysis = self.generate_llm_analysis()
                report.append(llm_analysis)
                report.append("")

            report.append("## 📁 ARCHIVOS RELACIONADOS")
            report.append(f"- **Guion analizado**: `{self.script_path}`")
            report.append(
                f"- **Metadatos de producción**: `{self.script_path.parent.parent.parent}/metadata.yaml`"
            )
            report.append(
                f"- **Concepto creativo**: `{self.script_path.parent.parent.parent}/01-preproduccion/concept.md`"
            )
            report.append("")

            report.append("## 🔄 PRÓXIMOS PASOS SUGERIDOS")
            report.append("1. Revisar las recomendaciones específicas para tu guion")
            report.append("2. Compartir el análisis con el equipo creativo")
            report.append("3. Actualizar el guion basado en el feedback")
            report.append("4. Documentar cambios en el historial de versiones")
            report.append("5. Realizar nuevo análisis después de las revisiones")
            report.append("")

            report.append("---")
            report.append(
                f"*Análisis generado automáticamente el {datetime.now().strftime('%Y-%m-%d')}*"
            )
            report.append(
                "*Usa `python scripts/analyze-script.py --help` para más opciones*"
            )

        return "\n".join(report)

    def save_report(self, report: str, output_path: Optional[Path] = None) -> Path:
        """Guardar reporte de análisis."""

        if output_path is None:
            # Crear nombre de archivo basado en el guion
            script_name = self.script_path.stem
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = (
                self.script_path.parent / f"analysis_{script_name}_{timestamp}.md"
            )

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(report)
            return output_path
        except Exception as e:
            print(f"❌ Error guardando reporte: {e}")
            raise


def main():
    """Función principal."""

    parser = argparse.ArgumentParser(
        description="Analizador de guiones en formato markdown"
    )
    parser.add_argument("script", help="Ruta al archivo de guion (.md)")
    parser.add_argument(
        "--output", "-o", help="Ruta de salida para el reporte (opcional)"
    )
    parser.add_argument(
        "--llm",
        action="store_true",
        help="Incluir análisis con LLM (requiere configuración)",
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "anthropic", "local"],
        default="openai",
        help="Proveedor de LLM a usar",
    )

    args = parser.parse_args()

    print("📊 Analizador de Guiones")
    print("=" * 50)

    try:
        # Crear analizador
        analyzer = ScriptAnalyzer(Path(args.script), args.provider)

        # Cargar guion
        print(f"📖 Cargando guion: {args.script}")
        if not analyzer.load_script():
            return 1

        # Extraer metadatos
        print("🔍 Extrayendo metadatos...")
        metadata = analyzer.extract_metadata()
        print(f"   • Título: {metadata['title']}")
        print(f"   • Autor: {metadata['author']}")
        print(f"   • Escenas: {metadata['scenes']}")
        print(f"   • Personajes: {len(metadata['characters'])}")

        # Generar reporte
        print("\n📈 Generando análisis...")
        report = analyzer.generate_report(include_llm=args.llm)

        # Guardar reporte
        output_path = analyzer.save_report(
            report, Path(args.output) if args.output else None
        )
        print(f"\n✅ Reporte guardado: {output_path}")

        # Mostrar resumen
        print("\n📋 RESUMEN DEL ANÁLISIS")
        print("-" * 40)

        # Análisis de estructura
        structure = analyzer.analyze_structure()
        print(f"Ritmo: {structure['pacing'].capitalize()}")
        print(
            f"Diálogo/Acción: {structure['dialogue_ratio']:.1f}% / {structure['action_ratio']:.1f}%"
        )

        # Análisis de personajes
        characters = analyzer.analyze_characters()
        print(f"Personajes principales: {len(characters['main_characters'])}")

        # Análisis de diálogo
        dialogue = analyzer.analyze_dialogue()
        print(f"Legibilidad: {dialogue['readability_score']}/100")

        print(f"\n📄 Ver reporte completo: {output_path}")

        return 0

    except FileNotFoundError as e:
        print(f"❌ {e}")
        return 1
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada por el usuario.")
        sys.exit(1)
