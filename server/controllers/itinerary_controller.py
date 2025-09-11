from server.core.database import supabase

def save_user_petition(petition_data):
    """
    Guarda la petición estructurada del usuario en la tabla 'user_petitions'.
    """
    if not supabase:
        print("Error: No hay conexión a Supabase.")
        return None

    try:
        response = supabase.from_('user_petitions').insert({
            'duration': petition_data.get('duration'),
            'kids_age': petition_data.get('kids_age'),
            'budget': petition_data.get('budget'),
            'interests': petition_data.get('interests')
        }).execute()
        
        # Devuelve el ID de la fila recién insertada
        return response.data[0]['id']

    except Exception as e:
        print(f"Ocurrió un error al guardar la petición del usuario: {e}")
        return None

def save_itinerary(trip_data, activities_data):
    """
    Guarda el plan de viaje final en las tablas 'trips' y 'activities'.
    """
    if not supabase:
        print("Error: No hay conexión a Supabase.")
        return None

    try:
        # 1. Guardar la información principal del viaje
        trip_response = supabase.from_('trips').insert({
            'nombre_viaje': trip_data.get('nombre_viaje'),
            'duration': trip_data.get('duration'),
            'budget': trip_data.get('budget'),
            'kids_age': trip_data.get('kids_age'),
            'interests': trip_data.get('interests'),
            'descripcion_viaje': trip_data.get('descripcion_viaje')
        }).execute()
        
        trip_id = trip_response.data[0]['id']

        # 2. Guardar las actividades, enlazándolas al viaje
        for activity in activities_data:
            activity['trip_id'] = trip_id
        
        supabase.from_('activities').insert(activities_data).execute()

        print("Itinerario guardado con éxito.")
        return True

    except Exception as e:
        print(f"Ocurrió un error al guardar el itinerario: {e}")
        return False