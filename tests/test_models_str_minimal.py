import pytest
from model_bakery import baker

@pytest.mark.django_db
def test_core_models_str_and_create():
    carrera = baker.make("academia_core.Carrera")
    plan = baker.make("academia_core.PlanEstudios", carrera=carrera)
    assert carrera.pk and plan.pk
    assert str(carrera)
    assert str(plan)

@pytest.mark.django_db
def test_horarios_models_create_minimal():
    # Crea relaciones mínimas para Horario sin violar constraints
    materia = baker.make("academia_core.Materia")
    plan = baker.make("academia_core.PlanEstudios")
    ec = baker.make("academia_core.EspacioCurricular", materia=materia, plan=plan)
    h = baker.make("academia_horarios.Horario", materia=ec, plan=plan)
    assert h.pk
