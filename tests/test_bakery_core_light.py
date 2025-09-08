from importlib import import_module

import pytest
from model_bakery import baker


def _resolve_core_models():
    try:
        module = import_module("academia_core.models")
    except Exception:
        return None, None
    return getattr(module, "Carrera", None), getattr(module, "PlanEstudios", None)


@pytest.mark.django_db
def test_bakery_can_build_core_models():
    Carrera, PlanEstudios = _resolve_core_models()
    if not Carrera or not PlanEstudios:
        pytest.skip("Modelos core no disponibles con esos nombres")
        return  # aplaca a CodeQL/linters

    c = baker.make(Carrera)
    p = baker.make(PlanEstudios)
    assert c.pk is not None
    assert p.pk is not None