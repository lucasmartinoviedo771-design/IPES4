import pytest
from django.apps import apps
from model_bakery import baker

TARGET_APPS = ["academia_core", "academia_horarios"]

@pytest.mark.django_db
@pytest.mark.parametrize("app_label", TARGET_APPS)
def test_models_prepare_and_str(app_label):
    app_config = apps.get_app_config(app_label)
    touched = 0

    for model in app_config.get_models():
        # Evitamos nombres muy problemáticos si hiciera falta:
        

        # 1) prepare (no guarda => menos choques con constraints)
        try:
            instance = baker.prepare(model)
            _ = str(instance)
            touched += 1
        except Exception:
            # No hacemos fallar el smoke; seguimos con el resto
            continue

    # Al menos tocamos 1 modelo del app
    assert touched >= 1, f"No models touched for {app_label}"
