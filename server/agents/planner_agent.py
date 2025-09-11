# Importa las funciones del controlador de base de datos.
from controllers.itinerary_controller import save_user_petition, save_itinerary

def generate_and_save_itinerary(user_input_text: str):
    """
    Función principal que procesa la petición de un usuario y guarda el itinerario.
    
    Args:
        user_input_text: El texto original que el usuario ha escrito.
    """
    
    # --- PASO 1: EXTRAER LA INFORMACIÓN CLAVE (LA "ENTRADA") ---
    # Tu tarea pendiente para configurar el agente es analizar el 'user_input_text' y extraer los datos relevantes.
    # El resultado debe ser un diccionario con las siguientes variables.
    
    print(f"Agente: Analizando la petición del usuario: '{user_input_text}'")
    
    # Aquí es donde tu modelo LLM hará su magia.
    # Por ahora, usamos datos de ejemplo:
    extracted_data = {
        "duration": 5,
        "kids_age": "5, 8",
        "budget": "medio",
        "interests": "museos, parques",
    }
    
    # --- PASO 2: GUARDAR LA ENTRADA EN LA BASE DE DATOS ---
    # Llama a la función del controlador que guarda la petición estructurada.
    # No te preocupes por el código de la función, solo llámala con los datos correctos.
    request_id = save_user_petition(extracted_data)
    
    if not request_id:
        print("Error: No se pudo guardar la petición. Abortando.")
        return None
        
    print(f"Agente: Petición guardada con ID: {request_id}")


    # --- PASO 3: GENERAR EL PLAN DE VIAJE (LA "SALIDA") ---
    # Usa la información extraída para generar el plan de viaje completo.
    # El resultado debe ser un diccionario para el viaje y una lista de diccionarios para las actividades.
    
    print("Agente: Generando el plan de viaje...")
    
    trip_plan_data = {
        "nombre_viaje": "Viaje a Madrid con Niños",
        "duration": extracted_data["duration"],
        "budget": extracted_data["budget"],
        "kids_age": extracted_data["kids_age"],
        "interests": extracted_data["interests"],
        "descripcion_viaje": "Un plan de 5 días enfocado en actividades familiares.",
    }

    activities_list = [
        {
            "nombre_actividad": "Visita al Museo del Prado",
            "lugar": "Madrid",
            "descripcion_actividad": "Tour por la colección de arte española.",
            "hora_sugerida": "mañana",
            "costo_estimado": "15€",
            "transporte_sugerido": "Metro",
        },
        {
            "nombre_actividad": "Paseo en el Parque del Retiro",
            "lugar": "Madrid",
            "descripcion_actividad": "Disfrutar de un paseo en barca en el lago.",
            "hora_sugerida": "tarde",
            "costo_estimado": "Gratis",
            "transporte_sugerido": "Caminando",
        },
    ]
    
    # --- PASO 4: GUARDAR LA SALIDA EN LA BASE DE DATOS ---
    # Llama a la función del controlador que guarda el plan final.
    # Esta función guarda los datos en las tablas 'trips' y 'activities'.
    success = save_itinerary(trip_plan_data, activities_list)
    
    if success:
        print("Agente: ¡Plan de viaje guardado con éxito!")
    else:
        print("Agente: Hubo un error al guardar el itinerario.")

# Ejemplo de uso:
# generate_and_save_itinerary("Quiero un viaje a Madrid de 5 días con mis dos hijos de 5 y 8 años, con un presupuesto medio, y nos gustan los museos y parques.")