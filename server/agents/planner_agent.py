# Importa la función de guardado desde tu controlador
from server.controllers.itinerary_controller import save_itinerary

def run_planner_agent(user_prompt):
    """
    Función que gestiona el flujo del agente de planificación.
    """
    # [Aquí va la lógica de tu compañero para hablar con el LLM]
    #
    # Por ejemplo, el código que procesa 'user_prompt',
    # lo envía a un LLM y recibe una respuesta.

    # Esta es la estructura de datos que tu compañero debe generar
    # para que tu función de guardado funcione correctamente.
    generated_plan = {
        'nombre_viaje': 'Ejemplo de Viaje',
        'fecha_inicio': 'YYYY-MM-DD',
        'fecha_fin': 'YYYY-MM-DD',
        'actividades': [
            {
                'nombre_actividad': 'Ejemplo de Actividad',
                'lugar': 'Ubicación',
                'hora_inicio': 'YYYY-MM-DDTHH:MM:SSZ'
            }
        ]
    }
    
    # Llama a tu función para guardar el plan
    trip_id = save_itinerary(generated_plan)

    if trip_id:
        print(f"Plan guardado en Supabase con ID: {trip_id}")
    else:
        print("Fallo al guardar el plan de viaje.")

# La siguiente línea permite ejecutar este archivo para probarlo
if __name__ == "__main__":
    test_prompt = "Planifica un viaje a Madrid..."
    run_planner_agent(test_prompt)