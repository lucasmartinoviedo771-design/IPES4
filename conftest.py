# conftest.py (raíz)
from pathlib import Path


def pytest_ignore_collect(collection_path: Path, config):
    # Ignora cualquier cosa cuyo path contenga "IPES3" en la ruta (por si acaso)
    return "ipes3" in str(collection_path).lower()
