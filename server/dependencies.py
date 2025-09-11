_resource_data = {} # Variable interna para almacenar los recursos

def set_resource_data(data):
    """Establece los datos de los recursos una vez que han sido cargados."""
    global _resource_data
    _resource_data = data

def get_resource_data():
    """Obtiene los datos de los recursos."""
    return _resource_data