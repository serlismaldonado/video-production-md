# 🎬 Sistema de Producción Audiovisual - Markdown

Sistema estructurado para gestión de producciones audiovisuales utilizando archivos markdown, diseñado para colaboración, versionado con Git y potenciado con LLMs.

## 🎯 Objetivo

Proporcionar una estructura organizada para gestionar todas las fases de una producción audiovisual, desde la preproducción hasta la entrega final, utilizando archivos markdown que facilitan la colaboración, el versionado y el procesamiento con herramientas de IA.

## 📁 Estructura del Proyecto

```
video-production-md/
├── productions/                 # Todas las producciones
│   └── {nombre-produccion}/    # Cada producción como subdirectorio
│       ├── README.md           # Overview de la producción
│       ├── metadata.yaml       # Metadatos estructurados
│       ├── 01-preproduccion/   # Fase de preproducción
│       ├── 02-guion/           # Desarrollo de guion
│       ├── 03-produccion/      # Rodaje y producción
│       ├── 04-postproduccion/  # Edición y postproducción
│       └── 05-archivos/        # Documentación y referencias
├── templates/                  # Plantillas reutilizables
├── scripts/                    # Scripts de automatización
├── docs/                       # Documentación del sistema
└── .github/workflows/          # Automatizaciones CI/CD
```

## 🚀 Cómo Empezar

### 1. Crear una nueva producción

```bash
# Copiar la plantilla de producción
cp -r templates/production-template productions/nueva-produccion

# O crear manualmente
mkdir -p productions/nueva-produccion/{01-preproduccion,02-guion,03-produccion,04-postproduccion,05-archivos}
```

### 2. Configurar metadatos

Editar `productions/nueva-produccion/metadata.yaml` con la información básica:
- Título, descripción, género
- Fechas de producción
- Equipo clave
- Presupuesto estimado

### 3. Comenzar documentación

Seguir el flujo de trabajo estándar:
1. **Preproducción**: Concepto, investigación, casting, locaciones
2. **Guion**: Tratamiento, estructura, versiones del guion
3. **Producción**: Plan de rodaje, equipo, presupuesto
4. **Postproducción**: Edición, efectos, entrega

## 🔧 Características Principales

### ✅ Markdown First
- Todos los documentos en formato markdown
- Fácil de editar, versionar y colaborar
- Compatible con cualquier editor de texto

### 🤖 LLM Integration
- Estructura optimizada para procesamiento con IA
- Scripts para análisis y generación automática
- Plantillas que facilitan el trabajo con LLMs

### 🔄 Version Control
- Git para control de cambios en guiones y documentos
- Historial completo de revisiones
- Colaboración sin conflictos de formato

### 📊 Metadatos Estructurados
- Archivos YAML para información organizada
- Búsqueda y filtrado eficiente
- Exportación a diferentes formatos

## 🛠️ Herramientas Recomendadas

### Editores
- **Visual Studio Code** con extensiones markdown
- **Typora** para edición WYSIWYG
- **Obsidian** para gestión de conocimiento

### Scripts y Automatización
- Ver `scripts/` para utilidades de automatización
- Workflows de GitHub en `.github/workflows/`
- Plantillas en `templates/`

### Integración con LLMs
- Usar scripts en `scripts/` para análisis de guiones
- Plantillas optimizadas para prompts de IA
- Generación automática de documentos

## 📚 Documentación

- **Guía de uso**: `docs/usage-guide.md`
- **Estructura detallada**: `docs/structure.md`
- **Flujos de trabajo**: `docs/workflows.md`
- **Integración con LLMs**: `docs/llm-integration.md`

## 🤝 Contribución

1. Cada producción debe estar en su propio directorio
2. Seguir la estructura de fases (01-, 02-, etc.)
3. Usar plantillas cuando sea posible
4. Mantener metadatos actualizados
5. Documentar cambios importantes

## 📄 Licencia

Este sistema está diseñado para uso interno de agencias de producción audiovisual. Adaptar según necesidades específicas.

---

**🎥 ¡Que comience la producción!**