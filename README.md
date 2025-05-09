# VÉRTICE - Sistema de Gestión Académica

**Vértice** es un sistema web desarrollado como proyecto de tesis para gestionar información académica y administrativa de una institución educativa. Incluye funcionalidades para estudiantes, docentes, coordinadores, personal administrativo y superusuarios.

## Tecnologías Usadas

- Backend: Python 3.10+, Flask, Tortoise ORM, PostgreSQL  
- Frontend: SvelteKit, TailwindCSS, Flowbite-Svelte  
- ORM/Migraciones: Tortoise ORM + Aerich  
- Gestión de paquetes: Poetry (Python), pnpm (Node)

## Módulos y Funcionalidades

### Administración
- ✅ Módulo de estudiantes (búsqueda, visualización)
- ✅ Módulo de pagos (consulta, registro, reportes)
- 🚫 Módulo de movimientos (acceso restringido al superusuario)

### Web Estudiantil
- ✅ Inicio de sesión
- ✅ Ver información personal, materias inscritas y horario
- ✅ Ver histórico de notas
- 🔲 Ver calificaciones por corte
- 🔲 Descargar planificación del docente
- 🔲 Descargar constancia de estudio

### Web Docente
- ✅ Ver materias asignadas
- ✅ Ver estudiantes inscritos y cargar calificaciones por corte
- 🔲 Descargar calificaciones
- 🔲 Subir planificación (PDF)

### Web Coordinador
- ✅ Configurar sistema (cortes, inscripciones, pagos)
- ✅ Registrar y editar materias (incluye prelación)
- ✅ Registrar docentes y ver estudiantes por carrera/semestre
- 🟡 Prelación de materias (listo pero falta probar)

### Web Control de Estudios
- ✅ Ver materias por carrera/semestre
- ✅ Gestionar peticiones de corrección de notas
- ✅ Ver estudiantes y ficha técnica

### Web Superusuario
- ✅ Administrar usuarios (coordinadores y control de estudio)
- ✅ Ver log del sistema
- ✅ Crear/editar carreras


✅ Avance: (26 / 31) × 100 = ~83.87%

---

## Guía de Instalación y Ejecución

### 1. Requisitos

- Python 3.10+: https://www.python.org/downloads/
- Node.js 18+: https://nodejs.org/en/download
- pnpm (desde npm): CODIGO bash  
  npm install -g pnpm@latest
- Poetry:
```bash  
  curl -sSL https://install.python-poetry.org | python3 -
  ```

### 2. Configuración

- Descomprimir `vertice-main.zip` fuera de carpetas sincronizadas.
- Restaurar base de datos con pgAdmin:
  - Crear base de datos llamada `pascal`
  - Usar la opción **Restore** y seleccionar `pascal.dump`

### 3. Backend (Vértice)

```bash  
cd ruta/a/vertice-main  
poetry install  
poetry shell  
aerich migrate --name baseline  
aerich upgrade  
uvicorn app:app --reload
```

### 4. Frontend

```bash  
cd packages/front  
pnpm install  
pnpm dev
```

### 5. Acceso

- Frontend: http://localhost:5173  
- Backend: http://localhost:8000

---

## Estado del Proyecto

Avance total: ~84%  
Faltantes: 5 funcionalidades (detalladas arriba)

---

## Licencia

Proyecto académico sin fines comerciales.
