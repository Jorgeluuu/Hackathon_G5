# Importa el cliente de Supabase que definiste en database.py
from server.core.database import supabase

def save_itinerary(itinerary_data):
    """
    Guarda un plan de viaje completo y sus actividades en la base de datos.
    """
    if not supabase:
        print("Error: No hay conexión a Supabase.")
        return None

    try:
        # 1. Inserta el viaje principal y obtiene su ID
        trip_response = supabase.from_('trips').insert({
            'nombre_viaje': itinerary_data['nombre_viaje'],
            'fecha_inicio': itinerary_data['fecha_inicio'],
            'fecha_fin': itinerary_data['fecha_fin']
        }).execute()

        # El ID del viaje es la clave para conectar las actividades
        trip_id = trip_response.data[0]['id']

        # 2. Prepara una lista para guardar las actividades
        activities_to_insert = []
        for activity in itinerary_data['actividades']:
            # Añade el 'trip_id' a cada actividad antes de insertarla
            activity['trip_id'] = trip_id
            activities_to_insert.append(activity)

        # 3. Inserta todas las actividades de golpe
        supabase.from_('activities').insert(activities_to_insert).execute()

        print(f"Plan '{itinerary_data['nombre_viaje']}' guardado con éxito.")
        return trip_id

    except Exception as e:
        print(f"Ocurrió un error al guardar el itinerario: {e}")
        return None