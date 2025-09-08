import importlib

import pytest

MODULES = [
    # academia_core
    "academia_core.forms",
    "academia_core.forms_admin",
    "academia_core.forms_carga",
    "academia_core.forms_correlativas",
    "academia_core.forms_espacios",
    "academia_core.forms_student",
    "academia_core.kpis",
    "academia_core.label_utils",
    "academia_core.utils",
    "academia_core.utils_inscripciones",
    "academia_core.eligibilidad",
    "academia_core.condiciones",
    "academia_core.correlativas",
    "academia_core.view_utils",
    "academia_core.views",
    "academia_core.views_api",
    "academia_core.views_auth",
    "academia_core.views_cbv",
    "academia_core.views_inscripciones",
    "academia_core.views_panel",
    "academia_core.signals",
    "academia_core.context_processors",
    "academia_core.urls",

    # academia_horarios
    "academia_horarios.forms",
    "academia_horarios.services",
    "academia_horarios.signals",
    "academia_horarios.views",
    "academia_horarios.urls",

    # ui
    "ui.api",
    "ui.auth_views",
    "ui.context_processors",
    "ui.forms",
    "ui.menu",
    "ui.mixins",
    "ui.permissions",
    "ui.signals",
    "ui.views",
    "ui.views_api",
    "ui.views_docentes",
    "ui.views_panel",
    "ui.urls",

    # proyecto
    "academia_project.urls",
]

@pytest.mark.parametrize("mod", MODULES)
def test_all_modules_import(mod):
    importlib.import_module(mod)
