# Guía de Uso - Sistema de Producción Audiovisual

## Introducción

Este sistema está diseñado para gestionar producciones audiovisuales utilizando archivos markdown. La estructura permite organizar todas las fases de una producción, desde la concepción hasta la entrega final, facilitando la colaboración, el versionado con Git y el procesamiento con herramientas de IA.

## Estructura del Sistema

### Directorios Principales

```
video-production-md/
├── productions/                 # Todas las producciones
├── templates/                  # Plantillas reutilizables
├── scripts/                    # Scripts de automatización
├── docs/                       # Documentación del sistema
└── .github/workflows/          # Automatizaciones CI/CD
```

### Estructura de una Producción

Cada producción sigue esta estructura:

```
{nombre-produccion}/
├── README.md                    # Overview de la producción
├── metadata.yaml                # Metadatos estructurados
├── 01-preproduccion/           # Fase 1: Preproducción
├── 02-guion/                   # Fase 2: Desarrollo de guion
├── 03-produccion/              # Fase 3: Rodaje y producción
├── 04-postproduccion/          # Fase 4: Edición y postproducción
└── 05-archivos/                # Fase 5: Documentación y referencias
```

## Primeros Pasos

### 1. Crear una Nueva Producción

#### Método 1: Usando el Script (Recomendado)

```bash
# Navegar al directorio del proyecto
cd video-production-md

# Ejecutar el script de creación
python scripts/create-production.py

# O especificar el nombre directamente
python scripts/create-production.py "Mi-Nueva-Produccion"
```

El script guiará a través del proceso de creación y solicitará información básica.

#### Método 2: Manualmente

```bash
# Copiar la plantilla
cp -r templates/production-template productions/mi-produccion

# O crear la estructura manualmente
mkdir -p productions/mi-produccion/{01-preproduccion,02-guion,03-produccion,04-postproduccion,05-archivos}
```

### 2. Configurar Metadatos

Editar `productions/mi-produccion/metadata.yaml` con la información básica:

```yaml
production:
  title: "Título de la Producción"
  genre: ["Drama", "Suspenso"]
  format: "Cortometraje"
  duration_minutes: 15
  logline: "Una línea que resume la historia completa"
  
crew:
  director:
    name: "Nombre del Director"
    contact: "email@ejemplo.com"
```

### 3. Comenzar con la Preproducción

1. **Concepto Creativo**: Editar `01-preproduccion/concept.md`
2. **Brief del Cliente**: Completar `01-preproduccion/brief.md`
3. **Investigación**: Usar el directorio `01-preproduccion/research/`
4. **Casting**: Documentar en `01-preproduccion/casting/`
5. **Locaciones**: Registrar en `01-preproduccion/locations/`

## Flujo de Trabajo por Fases

### Fase 1: Preproducción (01-preproduccion/)

**Objetivo**: Preparar todo para el rodaje.

**Documentos clave**:
- `concept.md` - Concepto creativo completo
- `brief.md` - Brief del cliente y requisitos
- Archivos en `research/` - Investigación y referencias
- Documentos en `casting/` - Proceso de casting
- Información en `locations/` - Scouting de locaciones

**Checklist**:
- [ ] Concepto creativo aprobado
- [ ] Brief del cliente completo
- [ ] Casting finalizado
- [ ] Locaciones confirmadas
- [ ] Permisos obtenidos
- [ ] Presupuesto aprobado

### Fase 2: Guion (02-guion/)

**Objetivo**: Desarrollar el guion final.

**Documentos clave**:
- `script/guion-v1.0.md` - Versiones del guion
- `script/revisions.md` - Historial de cambios
- `storyboard/` - Storyboard y planos
- `treatment.md` - Tratamiento narrativo
- `outline.md` - Estructura de la historia

**Checklist**:
- [ ] Tratamiento aprobado
- [ ] Estructura completa
- [ ] Guion finalizado
- [ ] Storyboard completo
- [ ] Guion bloqueado para producción

### Fase 3: Producción (03-produccion/)

**Objetivo**: Rodar el material.

**Documentos clave**:
- `shooting-plan/schedule.md` - Plan de rodaje
- `shooting-plan/call-sheets/` - Hojas de llamado diarias
- `crew/roles.md` - Roles y responsabilidades
- `crew/contacts.md` - Contactos del equipo
- `budget/breakdown.md` - Desglose de presupuesto
- `budget/expenses.md` - Gastos registrados

**Checklist**:
- [ ] Plan de rodaje completo
- [ ] Equipo confirmado
- [ ] Presupuesto actualizado
- [ ] Hojas de llamado preparadas
- [ ] Logística organizada
- [ ] Material rodado

### Fase 4: Postproducción (04-postproduccion/)

**Objetivo**: Editar y finalizar la producción.

**Documentos clave**:
- `editing/timeline.md` - Estructura de edición
- `editing/notes.md` - Notas de edición
- `vfx-sound/vfx-list.md` - Lista de efectos visuales
- `vfx-sound/sound-design.md` - Diseño de sonido
- `delivery/specs.md` - Especificaciones de entrega
- `delivery/versions.md` - Versiones finales

**Checklist**:
- [ ] Edición preliminar completa
- [ ] Efectos visuales aplicados
- [ ] Diseño de sonido terminado
- [ ] Corrección de color finalizada
- [ ] Versiones de entrega generadas
- [ ] Control de calidad aprobado

### Fase 5: Archivos (05-archivos/)

**Objetivo**: Documentación final y archivos.

**Documentos clave**:
- `assets/` - Enlaces a assets (no los archivos reales)
- `contracts/` - Documentos legales y contratos
- `references/` - Referencias y materiales de apoyo

**Checklist**:
- [ ] Contratos archivados
- [ ] Assets documentados
- [ ] Referencias organizadas
- [ ] Lecciones aprendidas documentadas

## Scripts de Automatización

### Crear Producción

```bash
python scripts/create-production.py "Nombre-Produccion"
```

**Funcionalidades**:
- Crea estructura completa desde plantilla
- Solicita información interactiva
- Actualiza metadatos automáticamente
- Genera reporte de creación

### Analizar Guion

```bash
python scripts/analyze-script.py productions/mi-produccion/02-guion/script/guion-v1.0.md
```

**Opciones**:
- `--output report.md` - Especificar archivo de salida
- `--llm` - Incluir análisis con IA (requiere configuración)
- `--provider openai` - Especificar proveedor de LLM

**Análisis generado**:
- Metadatos del guion
- Estructura narrativa
- Análisis de personajes
- Calidad del diálogo
- Recomendaciones específicas

## Integración con Git

### Flujo de Trabajo Recomendado

1. **Commits por fase**: Agrupar cambios por fase de producción
2. **Mensajes descriptivos**: Usar convenciones claras
3. **Branches por features**: Para cambios experimentales
4. **Tags para versiones**: Marcar versiones importantes

### Ejemplo de Commits

```bash
# Preproducción
git commit -m "feat(preproduccion): Concepto creativo inicial"
git commit -m "feat(casting): Selección de actores principales"

# Guion
git commit -m "feat(guion): Versión 1.0 del guion"
git commit -m "fix(guion): Correcciones de diálogo en escena 5"

# Producción
git commit -m "feat(produccion): Plan de rodaje día 1"
git commit -m "docs(produccion): Actualización de contactos de equipo"
```

### .gitignore Configurado

El sistema incluye un `.gitignore` que:
- Excluye archivos multimedia grandes
- Mantiene solo referencias a assets
- Ignora archivos temporales y de configuración local
- Preserva la estructura markdown y YAML

## Integración con LLMs

### Estructura Optimizada para IA

1. **Markdown limpio**: Fácil de procesar por LLMs
2. **Metadatos estructurados**: Información organizada en YAML
3. **Plantillas con prompts**: Sugerencias para análisis con IA
4. **Scripts preparados**: Listos para integración con APIs

### Análisis Automatizado

Los scripts están diseñados para:
- Extraer información estructurada de guiones
- Generar reportes analíticos
- Integrarse con APIs de LLM (OpenAI, Anthropic, etc.)
- Proporcionar feedback específico y accionable

### Configuración de LLMs

1. **OpenAI**:
   ```bash
   export OPENAI_API_KEY='tu-api-key'
   ```

2. **Anthropic**:
   ```bash
   export ANTHROPIC_API_KEY='tu-api-key'
   ```

3. **Local**:
   Configurar en `scripts/analyze-script.py`

## Workflows de GitHub

### Validación Automática

El sistema incluye un workflow que:
1. Valida sintaxis markdown
2. Verifica estructura YAML
3. Comprueba integridad de producciones
4. Genera reportes de estructura

### Activación

Se ejecuta automáticamente en:
- Push a ramas main/master
- Pull requests
- Manualmente desde GitHub Actions

## Mejores Prácticas

### Nomenclatura

1. **Nombres de producción**: Usar guiones, sin espacios
   - ✅ `mi-corto-dramatico`
   - ❌ `Mi Corto Dramático`

2. **Archivos markdown**: Nombre descriptivo en minúsculas
   - ✅ `concepto-creativo.md`
   - ❌ `Concepto Creativo.md`

3. **Versiones de guion**: Usar números de versión
   - ✅ `guion-v1.0.md`, `guion-v1.1.md`
   - ❌ `guion-final.md`, `guion-nuevo.md`

### Organización

1. **Seguir la estructura**: Mantener las fases numeradas
2. **Documentar cambios**: Actualizar historiales de versión
3. **Mantener metadatos**: Actualizar `metadata.yaml` regularmente
4. **Usar plantillas**: Para consistencia entre producciones

### Colaboración

1. **Commits pequeños**: Cambios específicos y descriptivos
2. **Comunicación clara**: Documentar decisiones importantes
3. **Revisiones regulares**: Revisar progreso por fases
4. **Backups**: Usar Git para versionado, no solo almacenamiento

## Solución de Problemas

### Problemas Comunes

1. **Archivo no encontrado**:
   - Verificar rutas relativas
   - Confirmar que la producción existe en `productions/`

2. **Error de sintaxis YAML**:
   - Usar validador YAML online
   - Verificar indentación (2 espacios, no tabs)

3. **Problemas con scripts**:
   - Asegurar Python 3.8+
   - Instalar dependencias: `pip install pyyaml`

4. **Git ignore no funciona**:
   - Verificar que `.gitignore` esté en raíz
   - Ejecutar `git rm -r --cached .` y re-add

### Recursos Adicionales

1. **Documentación Markdown**: [Guía básica](https://www.markdownguide.org/)
2. **YAML Tutorial**: [Learn YAML](https://learnxinyminutes.com/docs/yaml/)
3. **Git Best Practices**: [Conventional Commits](https://www.conventionalcommits.org/)

## Soporte y Contribución

### Reportar Problemas

1. Verificar documentación existente
2. Revisar estructura del proyecto
3. Crear issue con:
   - Descripción del problema
   - Pasos para reproducir
   - Archivos relevantes

### Sugerir Mejoras

1. Analizar impacto en workflow existente
2. Proponer cambios específicos
3. Considerar compatibilidad con LLMs

### Contribuir al Sistema

1. Fork del repositorio
2. Crear branch para feature
3. Implementar cambios
4. Actualizar documentación
5. Crear pull request

---

**Última actualización**: Sistema versión 1.0  
**Próximos pasos**: Comenzar con `python scripts/create-production.py`
