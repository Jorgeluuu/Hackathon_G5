COLORS = {
    "primary": "#8B4513",      
    "secondary": "#DEB887",   
    "accent": "#FFD700",       
    "success": "#32CD32",      
    "warning": "#FFA500",     
    "danger": "#DC143C",      
    "info": "#87CEEB",        
    
    "background_primary": "#FFF8DC",   
    "background_secondary": "#F5F5DC",  
    "background_dark": "#8B4513",       
    
    "text_primary": "#2F4F4F",   
    "text_secondary": "#696969",   
    "text_light": "#FFFFFF",       
    "text_muted": "#A9A9A9"       
}

MESSAGES = {
    "welcome": [
        "¡Hola! Soy el Ratoncito Pérez y estoy aquí para hacer tu viaje mágico 🐭✨",
        "¡Bienvenidos a Madrid! Vamos a crear juntos una aventura inolvidable 🎪",
        "¡Hola familias aventureras! ¿Listos para descubrir los secretos de Madrid? 🗺️"
    ],
    
    "loading": [
        "El Ratoncito Pérez está preparando algo especial...",
        "Buscando los mejores lugares mágicos para vuestra familia...",
        "Creando recuerdos inolvidables... ¡Un momento por favor!",
        "Consultando mi mapa secreto de Madrid... 🗺️✨"
    ],
    
    "tips": [
        "¡Recuerda llevar calzado cómodo para caminar por la ciudad! 👟",
        "Los domingos por la mañana, muchos museos tienen entrada gratuita 🎨",
        "El mejor horario para visitar el Retiro es por la mañana temprano 🌳",
        "Siempre lleva una botella de agua, especialmente en verano 💧",
        "Los niños menores de 12 años viajan gratis en transporte público 🚇",
        "¡No olvides probar los churros con chocolate! Son tradición madrileña 🍫",
        "La siesta es sagrada en Madrid: muchas tiendas cierran de 14:00 a 17:00 😴"
    ],
    
    "error": [
        "¡Ups! Parece que el Ratoncito Pérez está ocupado guardando dientes 🦷",
        "¡Oops! Algo salió mal, pero no te preocupes, ¡lo arreglaremos enseguida! 🔧",
        "El Ratoncito Pérez tuvo un pequeño tropiezo, ¡inténtalo de nuevo! 🐭"
    ]
}

APP_CONFIG = {
    "app_name": "Planificador Mágico del Ratoncito Pérez",
    "version": "1.0.0",
    "debug": True,
    "host": "0.0.0.0",
    "port": 8050,
    
    # Límites y validaciones
    "max_duration_days": 7,
    "min_duration_days": 1,
    "max_budget": 200,
    "min_budget": 30,
    "max_children": 6,
    "max_message_length": 500
}

MADRID_DATA = {
    "destinations": {
        "Madrid Centro": {
            "description": "El corazón histórico de Madrid",
            "main_attractions": ["Plaza Mayor", "Puerta del Sol", "Palacio Real"],
            "recommended_days": 2
        },
        "Madrid Alrededores": {
            "description": "Madrid y sus alrededores más cercanos",
            "main_attractions": ["El Escorial", "Alcalá de Henares", "Chinchón"],
            "recommended_days": 3
        },
        "Madrid Completo": {
            "description": "Toda la Comunidad de Madrid",
            "main_attractions": ["Toledo", "Segovia", "Ávila"],
            "recommended_days": 5
        }
    },
    
    "default_activities": [
        {
            "name": "Museo del Prado",
            "category": "museums",
            "age_group": "all",
            "duration": "2-3 horas",
            "price": "15€",
            "description": "Una de las pinacotecas más importantes del mundo"
        },
        {
            "name": "Parque del Retiro",
            "category": "parks",
            "age_group": "families",
            "duration": "2-4 horas",
            "price": "Gratis",
            "description": "El pulmón verde de Madrid con actividades para niños"
        },
        {
            "name": "Palacio Real",
            "category": "history",
            "age_group": "all",
            "duration": "1-2 horas",
            "price": "12€",
            "description": "Residencia oficial de la Familia Real Española"
        },
        {
            "name": "Mercado de San Miguel",
            "category": "food",
            "age_group": "families",
            "duration": "1 hora",
            "price": "Variable",
            "description": "Mercado gourmet en estructura de hierro del siglo XX"
        },
        {
            "name": "Teatro Real",
            "category": "shows",
            "age_group": "older_children",
            "duration": "2-3 horas",
            "price": "25-100€",
            "description": "Ópera y espectáculos de alto nivel"
        },
        {
            "name": "Zoo Aquarium",
            "category": "adventure",
            "age_group": "children",
            "duration": "4-6 horas",
            "price": "25€",
            "description": "Zoo y acuario con más de 6000 animales"
        }
    ],
    
    "default_restaurants": [
        {
            "name": "Casa Botín",
            "cuisine": "Tradicional madrileña",
            "price_range": "€€€",
            "family_friendly": True,
            "speciality": "Cochinillo asado",
            "address": "Calle Cuchilleros, 17"
        },
        {
            "name": "Lateral",
            "cuisine": "Tapas modernas",
            "price_range": "€€",
            "family_friendly": True,
            "speciality": "Tapas creativas",
            "address": "Varias ubicaciones"
        },
        {
            "name": "Chocolatería San Ginés",
            "cuisine": "Dulces y chocolate",
            "price_range": "€",
            "family_friendly": True,
            "speciality": "Churros con chocolate",
            "address": "Pasadizo San Ginés, 5"
        },
        {
            "name": "La Bola",
            "cuisine": "Cocina tradicional",
            "price_range": "€€",
            "family_friendly": True,
            "speciality": "Cocido madrileño",
            "address": "Calle Bola, 5"
        }
    ],
    
    "default_hotels": [
        {
            "name": "Hotel Familiar Madrid Centro",
            "category": "hotel",
            "price_range": "€€",
            "rating": 4.0,
            "family_rooms": True,
            "location": "Centro",
            "amenities": ["WiFi", "Desayuno", "Aire acondicionado"]
        },
        {
            "name": "Apartamentos Turísticos Madrid",
            "category": "apartment",
            "price_range": "€€€",
            "rating": 4.2,
            "family_rooms": True,
            "location": "Salamanca",
            "amenities": ["Cocina", "Lavadora", "WiFi"]
        },
        {
            "name": "Hotel Económico Plaza",
            "category": "budget",
            "price_range": "€",
            "rating": 3.5,
            "family_rooms": True,
            "location": "Centro",
            "amenities": ["WiFi", "Recepción 24h"]
        }
    ]
}

INTERESTS_MAPPING = {
    "museums": "museums",
    "parks": "parks", 
    "shows": "shows",
    "history": "history",
    "food": "food",
    "shopping": "shopping",
    "art": "art",
    "sports": "sports",
    "adventure": "adventure",
    "learning": "learning"
}

AGE_GROUPS = {
    "toddlers": (0, 4),      
    "children": (5, 12),      
    "teens": (13, 17),        
    "adults": (18, 99),       
    "families": (0, 99),      
    "older_children": (8, 99) 
}

MOTIVATIONAL_PHRASES = [
    "¡Cada diente que recojo me cuenta una historia de aventura! 🦷✨",
    "Madrid está lleno de magia, solo hay que saber dónde buscar 🔍💫",
    "Las mejores aventuras comienzan con un buen plan... ¡y una sonrisa! 😊",
    "¡Recuerda cepillarte los dientes después de probar los churros! 🪥🍫",
    "En Madrid, cada esquina esconde una sorpresa mágica 🎪",
    "¡Los mejores recuerdos se crean en familia! 👨‍👩‍👧‍👦💕"
]

EXTERNAL_APIS = {
    "google_maps": {
        "base_url": "https://maps.googleapis.com/maps/api",
        "timeout": 10
    },
    "weather": {
        "base_url": "https://api.openweathermap.org/data/2.5",
        "timeout": 5
    },
    "transport": {
        "madrid_metro": "https://api.crtm.es",
        "timeout": 8
    }
}

CACHE_CONFIG = {
    "activities_ttl": 3600,      
    "restaurants_ttl": 1800,     
    "weather_ttl": 900,          
    "transport_ttl": 300         
}