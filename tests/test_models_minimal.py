import pytest
from model_bakery import baker


@pytest.mark.django_db
def test_core_models_create_smoke():
    carrera = baker.make("academia_core.Carrera")
    plan = baker.make("academia_core.PlanEstudios", carrera=carrera)
    assert carrera.pk and plan.pk
