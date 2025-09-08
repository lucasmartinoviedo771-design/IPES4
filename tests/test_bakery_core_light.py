import pytest
from model_bakery import baker

@pytest.mark.django_db
def test_bakery_can_build_core_models():
    """
    Crea instancias mínimas de modelos core sin tocar constraints complejas.
    Si no existen (nombre distinto), se salta.
    """
    try:
        core = __import__("academia_core.models", fromlist=["Carrera", "PlanEstudios"])
        Carrera = getattr(core, "Carrera", None)
        PlanEstudios = getattr(core, "PlanEstudios", None)
        if not Carrera or not PlanEstudios:
            pytest.skip("Modelos core no disponibles con esos nombres")
    except Exception:
        pytest.skip("academia_core.models no disponible")

    carrera = baker.make(Carrera)
    plan = baker.make(PlanEstudios)
    assert carrera.pk is not None
    assert plan.pk is not None
