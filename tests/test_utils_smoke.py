def test_utils_modules_importable():
    import academia_core.auth_utils as u4
    import academia_core.label_utils as u3
    import academia_core.utils as u1
    import academia_core.view_utils as u2
    import ui.context_processors as u5

    # que no exploten al importar; opcionalmente llama funciones si son puras
    assert u1 and u2 and u3 and u4 and u5
