import requests
import logging
from typing import Dict, Any, Optional
import json


class FastAPIClient:
    """Cliente para interactuar con la API del Ratoncito Pérez"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Inicializar cliente API
        
        Args:
            base_url: URL base de la API FastAPI
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        
        # Configurar logging
        self.logger = logging.getLogger(__name__)
        
    
    def generate_itinerary(self, planning_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Generar itinerario basado en las preferencias del usuario
        
        Args:
            planning_data: Datos del formulario de planificación
            
        Returns:
            Diccionario con el itinerario generado o None si hay error
        """
        try:
            endpoint = f"{self.base_url}/api/v1/itinerary/generate"
            
            # Validar datos requeridos
            required_fields = ["destination", "duration_days", "travel_date"]
            for field in required_fields:
                if field not in planning_data or not planning_data[field]:
                    self.logger.error(f"Campo requerido faltante: {field}")
                    return None
            
            # Realizar petición
            response = self.session.post(
                endpoint,
                json=planning_data,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Error en API: {response.status_code} - {response.text}")
                return self._create_fallback_itinerary(planning_data)
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error de conexión con API: {e}")
            return self._create_fallback_itinerary(planning_data)
        except Exception as e:
            self.logger.error(f"Error inesperado: {e}")
            return self._create_fallback_itinerary(planning_data)
    
    
    def chat_with_mouse(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Enviar mensaje al chat del Ratoncito Pérez
        
        Args:
            message: Mensaje del usuario
            context: Contexto adicional (itinerario actual, etc.)
            
        Returns:
            Respuesta del Ratoncito Pérez
        """
        try:
            endpoint = f"{self.base_url}/api/v1/chat"
            
            payload = {
                "message": message,
                "context": context or {}
            }
            
            response = self.session.post(
                endpoint,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Error en chat API: {response.status_code}")
                return self._create_fallback_chat_response(message)
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error de conexión en chat: {e}")
            return self._create_fallback_chat_response(message)
        except Exception as e:
            self.logger.error(f"Error inesperado en chat: {e}")
            return self._create_fallback_chat_response(message)
    
    
    def get_recommendations(self, category: str, filters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Obtener recomendaciones específicas (restaurantes, hoteles, etc.)
        
        Args:
            category: Tipo de recomendación ('restaurants', 'hotels', 'activities')
            filters: Filtros a aplicar
            
        Returns:
            Lista de recomendaciones
        """
        try:
            endpoint = f"{self.base_url}/api/v1/recommendations/{category}"
            
            response = self.session.get(
                endpoint,
                params=filters,
                timeout=20
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Error obteniendo recomendaciones: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error en recomendaciones: {e}")
            return None
    
    
    def _create_fallback_itinerary(self, planning_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear un itinerario de respaldo cuando la API no está disponible
        
        Args:
            planning_data: Datos originales del formulario
            
        Returns:
            Itinerario básico de ejemplo
        """
        duration = planning_data.get("duration_days", 2)
        destination = planning_data.get("destination", "Madrid Centro")
        
        fallback_itinerary = {
            "destination": destination,
            "total_days": duration,
            "created_with_fallback": True,
            "days": []
        }
        
        # Generar días básicos
        basic_activities = [
            {
                "name": "Museo del Prado",
                "time": "10:00",
                "description": "Visita a una de las pinacotecas más importantes del mundo",
                "location": "Paseo del Prado",
                "duration": "2-3 horas",
                "price": "15€"
            },
            {
                "name": "Parque del Retiro",
                "time": "14:00", 
                "description": "Paseo por el pulmón verde de Madrid",
                "location": "Puerta de Alcalá",
                "duration": "2 horas",
                "price": "Gratis"
            }
        ]
        
        basic_restaurants = [
            {
                "name": "Casa Botín",
                "cuisine": "Cocina tradicional madrileña",
                "address": "Calle Cuchilleros, 17",
                "rating": 4.2,
                "price_range": "€€€"
            }
        ]
        
        for day in range(1, duration + 1):
            day_data = {
                "title": f"Descubriendo Madrid - Día {day}",
                "description": "Un día lleno de magia y descubrimientos",
                "activities": basic_activities,
                "restaurants": basic_restaurants,
                "tip": "¡Recuerda llevar calzado cómodo para caminar por la ciudad! 👟"
            }
            fallback_itinerary["days"].append(day_data)
        
        # Añadir recomendaciones generales
        fallback_itinerary["recommendations"] = {
            "hotels": [
                {
                    "name": "Hotel Familiar Madrid Centro",
                    "rating": 4.0,
                    "price_range": "€€",
                    "location": "Centro"
                }
            ],
            "transport_info": "Utiliza el Metro de Madrid para moverte fácilmente por la ciudad.",
            "general_tips": [
                "Compra la tarjeta turística para ahorrar en transporte",
                "Reserva con antelación los museos más populares",
                "Lleva siempre una botella de agua"
            ]
        }
        
        return fallback_itinerary
    
    
    def _create_fallback_chat_response(self, user_message: str) -> Dict[str, Any]:
        """
        Crear respuesta de chat de respaldo
        
        Args:
            user_message: Mensaje original del usuario
            
        Returns:
            Respuesta genérica del Ratoncito Pérez
        """
        
        # Respuestas basadas en palabras clave
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ["metro", "transporte", "moverse"]):
            response = """¡Hola! 🚇 Para moverte por Madrid, te recomiendo:
            
• **Metro**: La forma más rápida. Compra un abono de 10 viajes por 12,20€
• **Autobús**: Perfecto para ver la ciudad. Mismas tarifas que el metro
• **A pie**: El centro histórico es muy caminable
• **Taxi/Uber**: Para trayectos con niños y equipaje

¡La tarjeta Multi Card es perfecta para toda la familia! 🎫"""
            
        elif any(word in message_lower for word in ["comer", "restaurante", "comida"]):
            response = """🍽️ ¡Me encanta hablar de comida! En Madrid encontrarás:

• **Cocido madrileño**: Un plato tradicional perfecto para familias
• **Mercado San Miguel**: Tapas gourmet en un ambiente único  
• **Chocolatería San Ginés**: ¡Los churros más famosos de Madrid!
• **Casa Botín**: El restaurante más antiguo del mundo según el Guinness

¿Algún tipo de comida en particular que os guste? 🐭✨"""
            
        elif any(word in message_lower for word in ["lluvia", "lluvioso", "mal tiempo"]):
            response = """☔ ¡No te preocupes! Madrid tiene opciones geniales para días lluviosos:

• **Museos**: Prado, Reina Sofía, Thyssen... ¡arte para todos los gustos!
• **Centros comerciales**: El Corte Inglés, Xanadú con parque de nieve
• **Mercados cubiertos**: San Miguel, San Antón, Mercado de la Paz
• **Teatro infantil**: Muchos espectáculos familiares los fines de semana

¡La lluvia también puede ser mágica en Madrid! 🌂✨"""
            
        elif any(word in message_lower for word in ["gratis", "barato", "económico"]):
            response = """💰 ¡El Ratoncito Pérez sabe cómo ahorrar! Actividades gratuitas:

• **Parque del Retiro**: Perfecto para niños, con el Palacio de Cristal
• **Templo de Debod**: Un templo egipcio real en Madrid
• **Plaza Mayor y Puerta del Sol**: El corazón de la ciudad
• **Rastro** (domingos): El mercadillo más famoso
• **Muchos museos**: Gratis los últimos días de cada mes

¡La magia no siempre cuesta dinero! 🎪✨"""
            
        else:
            response = """¡Hola! 🐭✨ Soy el Ratoncito Pérez y estoy aquí para ayudarte con tu aventura en Madrid.

Puedo ayudarte con:
• 🗺️ Cómo moverte por la ciudad
• 🍽️ Dónde comer en familia  
• 🎪 Actividades para niños
• 💰 Opciones económicas
• ☔ Planes para días lluviosos

¿En qué puedo ayudarte específicamente? ¡Pregúntame lo que quieras! 💫"""
        
        return {
            "message": response,
            "sender": "mouse",
            "created_with_fallback": True
        }
    
    
    def test_connection(self) -> bool:
        """
        Probar la conexión con la API
        
        Returns:
            True si la API está disponible, False en caso contrario
        """
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False