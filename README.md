# IPES4

[![CI](https://github.com/lucasmartinoviedo771-design/IPES4/actions/workflows/tests-coverage.yml/badge.svg)](https://github.com/lucasmartinoviedo771-design/IPES4/actions/workflows/tests-coverage.yml)
[![CodeQL](https://github.com/lucasmartinoviedo771-design/IPES4/actions/workflows/codeql.yml/badge.svg)](https://github.com/lucasmartinoviedo771-design/IPES4/actions/workflows/codeql.yml)

Sistema de gestión académica para el IPES.

## Quickstart (Desarrollo Local)

Este proyecto utiliza `uv` para la gestión del entorno virtual y las dependencias.

**1. Configuración Inicial**

```shell
# Clonar el repositorio (si no lo has hecho)
git clone https://github.com/lucasmartinoviedo771-design/IPES4.git
cd IPES4

# Crear y activar el entorno virtual
uv venv

# En Windows
.venv\Scripts\activate

# En macOS/Linux
source .venv/bin/activate
```

**2. Instalar Dependencias**

```shell
# Instalar dependencias de la aplicación y de desarrollo/test
uv pip install -r requirements.txt
uv pip install -r requirements-test.txt
```

**3. Configurar la Base de Datos y la Aplicación**

```shell
# Copiar el archivo de entorno de ejemplo
# (y ajústalo con tus credenciales de base de datos si es necesario)
copy .env.example .env

# Aplicar las migraciones de la base de datos
python manage.py migrate

# Crear un superusuario para acceder al admin
python manage.py createsuperuser
```

**4. Cargar Datos Iniciales (Seed)**

```shell
# Ejecutar los siguientes comandos para poblar la base de datos con datos básicos
python manage.py setup_roles
python manage.py importar_plan
python manage.py seed_correlatividades
```

**5. Ejecutar el Servidor de Desarrollo**

```shell
python manage.py runserver
```
Accede a `http://127.0.0.1:8000` en tu navegador.

## Comandos Útiles

**Correr los Tests**

```shell
# Correr todos los tests con reporte de cobertura
pytest -n auto --cov --cov-report=xml -q
```
