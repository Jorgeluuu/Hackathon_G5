import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from datetime import datetime, date
import requests
import json

from components.header import create_header
from components.forms import create_planning_form
from components.results import create_results_section
from components.chat import create_chat_section
from utils.api_client import FastAPIClient
from utils.constants import COLORS, MESSAGES

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Fredoka+One:wght@400&display=swap",
        "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap"
    ],
    assets_folder='assets'
)

app.title = "Brújula Mágica - Planificador mágico del Ratoncito Pérez"

api_client = FastAPIClient()

# Layout principal
app.layout = dbc.Container([
    create_header(),
    
    html.Div([
        dbc.Row([
            # Columna izquierda: Formulario de planificación
            dbc.Col([
                create_planning_form()
            ], width=4, className="form-column"),
            
            # Columna derecha: Resultados y chat
            dbc.Col([
                create_results_section(),
                html.Hr(className="magical-divider"),
                create_chat_section()
            ], width=8, className="results-column")
        ], className="main-content")
    ], className="content-wrapper"),
    
    html.Footer([
        html.P([
            "✨ Hecho con magia por el Ratoncito Pérez ✨",
            html.Br(),
            "Madrid, España 2025"
        ], className="footer-text")
    ], className="magical-footer"),
    
    # Stores para datos
    dcc.Store(id='itinerary-store'),
    dcc.Store(id='chat-store', data=[]),
    dcc.Store(id='user-preferences-store')
], fluid=True, className="main-container")


@app.callback(
    [Output('itinerary-store', 'data'),
     Output('results-container', 'children'),
     Output('loading-spinner', 'children')],
    [Input('generate-plan-btn', 'n_clicks')],
    [State('destination-input', 'value'),
     State('duration-slider', 'value'),
     State('budget-slider', 'value'),
     State('children-ages', 'value'),
     State('interests-checklist', 'value'),]
)
def generate_itinerary(n_clicks, destination, duration, budget, children_ages, interests):
    """Generar itinerario mágico basado en las preferencias del usuario"""
    if not n_clicks:
        return None, [], ""
    
    # Mostrar spinner de carga
    loading_component = dbc.Spinner([
        html.Div([
            html.Img(src="/assets/Ratoncito.png", className="spinning-tooth"),
            html.H5("El Ratoncito Pérez está preparando tu aventura mágica...", 
                   className="loading-text")
        ])
    ], color="primary")
    
    try:
        # Preparar datos para la API
        planning_data = {
        "destination": str(destination),
        "duration_days": int(duration),
        "budget_range": str(budget).lower(),  # siempre string
        "children_ages": (
            [int(children_ages)] if isinstance(children_ages, str) else
            [int(age) for age in children_ages] if children_ages else []
        ),
        "interests": interests if isinstance(interests, list) else [interests],
        "family_size": (len(children_ages) if isinstance(children_ages, list) else 1) + 2
        }

        
        # Llamada a la API
        itinerary = api_client.generate_itinerary(planning_data)
        
        if itinerary:
            results_component = create_itinerary_display(itinerary)
            return itinerary, results_component, ""
        else:
            error_message = dbc.Alert([
                html.H5("¡Oops! Algo salió mal 😅"),
                html.P("El Ratoncito Pérez tuvo un pequeño problema. ¡Inténtalo de nuevo!")
            ], color="danger", className="magical-alert")
            return None, [error_message], ""
            
    except Exception as e:
        error_message = dbc.Alert([
            html.H5("¡Error mágico! 🎩"),
            html.P(f"Hubo un problema: {str(e)}")
        ], color="danger", className="magical-alert")
        return None, [error_message], ""


def create_itinerary_display(itinerary_data):
    """Crear la visualización del itinerario generado"""
    if not itinerary_data:
        return []
    
    # Si hay un error en la respuesta
    if isinstance(itinerary_data, dict) and "error" in itinerary_data:
        return dbc.Alert([
            html.H5("❌ Error en el itinerario"),
            html.P(itinerary_data["error"])
        ], color="danger")
    
    components = []
    
    components.append(
        html.Div([
            html.H3([
                html.Span("🎪 ", style={"color": "#FF6B6B"}),
                f"Tu Aventura Mágica en {itinerary_data.get('destination', 'Madrid')}",
                html.Span(" 🎪", style={"color": "#FF6B6B"})
            ], className="itinerary-title", 
               style={"color": "#2C3E50", "textAlign": "center", "marginBottom": "10px"}),
            html.P(
                "✨ Planificado especialmente para tu familia por el Ratoncito Pérez ✨",
                className="itinerary-subtitle",
                style={"textAlign": "center", "color": "#7F8C8D", "fontSize": "16px", "marginBottom": "30px"}
            )
        ], className="itinerary-header", 
           style={"backgroundColor": "#FFFDE7", "padding": "20px", "borderRadius": "10px", "marginBottom": "30px",
                  "border": "2px dashed #FFD700"})
    )
    
    if 'days' in itinerary_data:
        for i, day in enumerate(itinerary_data['days'], 1):
            day_card = create_day_card(i, day)
            components.append(day_card)
    
    if 'recommendations' in itinerary_data:
        recommendations_card = create_recommendations_card(itinerary_data['recommendations'])
        components.append(recommendations_card)
    
    return components


def create_day_card(day_number, day_data):
    """Crear tarjeta para un día específico del itinerario"""
    
    card_body_elements = [
        html.P(day_data.get('description', 'Descripción del día mágico'),
               className="day-description"),
        
        # Barra de progreso decorativa
        html.Div(className="day-progress"),
    ]
    
    # Actividades
    activities = day_data.get('activities', [])
    if activities:
        activities_list = []
        for activity in activities:
            activities_list.append(
                html.Li([
                    html.Div([
                        html.Span([
                            html.Span("⏰ ", style={"color": "#FF6B6B"}),
                            html.Strong(f"{activity.get('time', 'Horario:')}"),
                            html.Span(" • ", style={"color": "#BDC3C7"}),
                            html.Span("📍 ", style={"color": "#3498DB"}),
                            activity.get('location', 'Madrid')
                        ], className="info-badge badge-time"),
                        html.Br(),
                        html.Strong(f"🎯 {activity.get('name', 'Actividad')}", 
                                  style={"color": "#D7DADE", "fontSize": "16px"}),
                        html.Br(),
                        html.Span(activity.get('description', ''), 
                                className="activity-description"),
                    ])
                ])
            )
        
        card_body_elements.append(
            html.Div([
                html.H6("🎯 Actividades del día:", className="section-title"),
                html.Ul(activities_list, className="activities-list")
            ], className="activities-section")
        )
    
    # Restaurantes
    restaurants = day_data.get('restaurants', [])
    if restaurants:
        restaurants_list = []
        for restaurant in restaurants:
            restaurants_list.append(
                html.Li([
                    html.Div([
                        html.Strong(f"🍽️ {restaurant.get('name', 'Restaurante')}", 
                                  style={"color": "#E67E22"}),
                        html.Br(),
                        html.Span(f"🍳 {restaurant.get('cuisine', 'Cocina local')}"),
                        html.Br(),
                        html.Small(f"📍 {restaurant.get('address', 'Madrid')}", 
                                 className="restaurant-address"),
                        html.Br(),
                        html.Span([
                            html.Span(f"⭐ {restaurant.get('rating', '4.0')}"),
                            html.Span(" • "),
                            html.Span(f"💰 {restaurant.get('price_range', '€€')}")
                        ], style={"color": "#7F8C8D", "fontSize": "14px"})
                    ])
                ])
            )
        
        card_body_elements.append(
            html.Div([
                html.H6("🍽️ Restaurantes recomendados:", className="section-title"),
                html.Ul(restaurants_list, className="restaurants-list")
            ], className="restaurants-section")
        )
    
    # Consejo
    tip = day_data.get('tip')
    if tip:
        card_body_elements.append(
            dbc.Alert([
                html.Div([
                    html.Img(src="/assets/Ratoncito.png", className="tip-icon"),
                    html.Div([
                        html.Strong("💫 Consejo Mágico del Ratoncito Pérez:"),
                        html.P(tip, className="tip-text")
                    ], className="tip-content")
                ], className="tip-container")
            ], color="info", className="magical-tip")
        )
    
    return dbc.Card([
        dbc.CardHeader([
            html.H4([
                f"🌟 Día {day_number} - {day_data.get('title', 'Aventura Mágica')}"
            ], className="day-title")
        ], className="day-header"),
        dbc.CardBody(card_body_elements)
    ], className="day-card magical-card")

def create_recommendations_card(recommendations):
    """Crear tarjeta con recomendaciones adicionales"""
    return dbc.Card([
        dbc.CardHeader([
            html.H4("💫 Recomendaciones Adicionales", 
                   className="recommendations-title",
                   style={"color": "#2C3E50", "textAlign": "center", "margin": "0"})
        ], style={"backgroundColor": "#E8F5E9", "padding": "15px", "borderBottom": "2px solid #4CAF50"}),
        dbc.CardBody([
            html.Div([
                html.H6("🏨 Alojamientos recomendados:", 
                       className="section-title",
                       style={"color": "#2C3E50", "borderBottom": "1px solid #4CAF50", "paddingBottom": "5px"}),
                html.Ul([
                    html.Li([
                        html.Strong(hotel.get('name', 'Hotel'), 
                                  style={"color": "#2E86C1"}),
                        f" - ⭐ {hotel.get('rating', 'N/A')}",
                        html.Br(),
                        html.Small(f"💰 {hotel.get('price_range', '')} | 📍 {hotel.get('location', '')}", 
                                 style={"color": "#7F8C8D"})
                    ], style={"marginBottom": "10px", "padding": "5px", "backgroundColor": "#F8F9FA", "borderRadius": "5px"}) 
                    for hotel in recommendations.get('hotels', [])
                ], className="hotels-list", style={"paddingLeft": "20px"})
            ], className="hotels-section", style={"marginBottom": "20px"}),
            
            html.Hr(style={"borderColor": "#BDC3C7"}),
            
            html.Div([
                html.H6("🚌 Transporte:", 
                       className="section-title",
                       style={"color": "#2C3E50", "borderBottom": "1px solid #3498DB", "paddingBottom": "5px"}),
                html.P(recommendations.get('transport_info', ''), 
                      className="transport-info",
                      style={"fontSize": "15px", "color": "#34495E", "padding": "10px", "backgroundColor": "#EBF5FB", "borderRadius": "5px"})
            ], className="transport-section", style={"marginBottom": "20px"}),
            
            html.Hr(style={"borderColor": "#BDC3C7"}),
            
            html.Div([
                html.H6("💡 Consejos generales:", 
                       className="section-title",
                       style={"color": "#2C3E50", "borderBottom": "1px solid #F39C12", "paddingBottom": "5px"}),
                html.Ul([
                    html.Li(tip, style={"marginBottom": "8px", "padding": "5px", "backgroundColor": "#FEF9E7", "borderRadius": "5px"}) 
                    for tip in recommendations.get('general_tips', [])
                ], className="tips-list", style={"paddingLeft": "20px"})
            ], className="general-tips-section")
        ], style={"padding": "20px"})
    ], className="recommendations-card magical-card", 
       style={"marginBottom": "25px", "border": "1px solid #D5F5E3", "borderRadius": "15px", "boxShadow": "0 4px 8px rgba(0,0,0,0.1)"})


@app.callback(
    [Output('chat-store', 'data'),
     Output('chat-messages', 'children'),
     Output('chat-input', 'value')],
    [Input('send-message-btn', 'n_clicks'),
     Input('chat-input', 'n_submit')],
    [State('chat-input', 'value'),
     State('chat-store', 'data'),
     State('itinerary-store', 'data')]
)
def handle_chat(n_clicks, n_submit, message, chat_history, itinerary_data):
    """Manejar el chat con el Ratoncito Pérez"""
    if not (n_clicks or n_submit) or not message:
        return chat_history or [], create_chat_messages(chat_history or []), ""
    
    new_chat_history = chat_history.copy() if chat_history else []
    new_chat_history.append({
        "sender": "user",
        "message": message,
        "timestamp": datetime.now().isoformat()
    })
    
    try:
        # Llamar a la API para obtener respuesta del Ratoncito Pérez
        response = api_client.chat_with_mouse(message, itinerary_data)
        
        new_chat_history.append({
            "sender": "mouse",
            "message": response.get("message", "¡El Ratoncito Pérez está pensando! 🤔"),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        new_chat_history.append({
            "sender": "mouse",
            "message": "¡Ups! Tuve un pequeño problema. ¿Puedes repetir tu pregunta? 🐭",
            "timestamp": datetime.now().isoformat()
        })
    
    return new_chat_history, create_chat_messages(new_chat_history), ""


def create_chat_messages(chat_history):
    """Crear componentes de mensajes del chat"""
    if not chat_history:
        return [
            html.Div([
                html.Img(src="/assets/Ratoncito.png", className="welcome-icon"),
                html.P("¡Hola! Soy el Ratoncito Pérez 🐭✨"),
                html.P("¿Tienes alguna pregunta sobre tu aventura mágica en Madrid?")
            ], className="welcome-message")
        ]
    
    messages = []
    for chat in chat_history:
        if chat["sender"] == "user":
            message_class = "user-message"
            icon = "👤"
        else:
            message_class = "mouse-message"
            icon = "🐭"
        
        messages.append(
            html.Div([
                html.Div([
                    html.Span(icon, className="message-icon"),
                    html.Div(chat["message"], className="message-content")
                ], className=f"message {message_class}")
            ], className="message-container")
        )
    
    return messages


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8050)