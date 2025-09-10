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

app.title = "Planificador Mágico del Ratoncito Pérez"

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
     State('interests-checklist', 'value'),
     State('date-picker', 'date')]
)
def generate_itinerary(n_clicks, destination, duration, budget, children_ages, interests, travel_date):
    """Generar itinerario mágico basado en las preferencias del usuario"""
    if not n_clicks:
        return None, [], ""
    
    if not destination or not travel_date:
        return None, [
            dbc.Alert(
                "¡Ups! El Ratoncito Pérez necesita saber el destino y la fecha para crear tu aventura mágica 🐭✨",
                color="warning",
                className="magical-alert"
            )
        ], ""
    
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
            "destination": destination,
            "duration_days": duration,
            "budget_range": budget,
            "children_ages": children_ages if children_ages else [],
            "interests": interests if interests else [],
            "travel_date": travel_date,
            "family_size": len(children_ages) + 2 if children_ages else 2
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
    
    components = []
    
    components.append(
        html.Div([
            html.H3([
                "🎪 Tu Aventura Mágica en Madrid 🎪"
            ], className="itinerary-title"),
            html.P(
                f"✨ Planificado especialmente para tu familia por el Ratoncito Pérez ✨",
                className="itinerary-subtitle"
            )
        ], className="itinerary-header")
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
        html.P(day_data.get('description', ''), className="day-description"),
        
        html.Div([
            html.H6("🎯 Actividades:", className="section-title"),
            html.Ul([
                html.Li([
                    html.Strong(f"{activity.get('time', '')}: "),
                    activity.get('name', ''),
                    html.Br(),
                    html.Small(activity.get('description', ''), className="activity-description")
                ]) for activity in day_data.get('activities', [])
            ], className="activities-list")
        ], className="activities-section")
    ]
    
    if day_data.get('restaurants'):
        card_body_elements.append(
            html.Div([
                html.H6("🍽️ Restaurantes recomendados:", className="section-title"),
                html.Ul([
                    html.Li([
                        html.Strong(restaurant.get('name', '')),
                        f" - {restaurant.get('cuisine', '')}",
                        html.Br(),
                        html.Small(restaurant.get('address', ''), className="restaurant-address")
                    ]) for restaurant in day_data.get('restaurants', [])
                ], className="restaurants-list")
            ], className="restaurants-section")
        )
    
    if day_data.get('tip'):
        card_body_elements.append(
            dbc.Alert([
                html.Div([
                    html.Img(src="/assets/Ratoncito.png", className="tip-icon"),
                    html.Strong("Consejo del Ratoncito Pérez: "),
                    day_data.get('tip', '')
                ])
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
            html.H4("💫 Recomendaciones Adicionales", className="recommendations-title")
        ]),
        dbc.CardBody([
            html.Div([
                html.H6("🏨 Alojamientos:", className="section-title"),
                html.Ul([
                    html.Li([
                        html.Strong(hotel.get('name', '')),
                        f" - ⭐ {hotel.get('rating', 'N/A')}",
                        html.Br(),
                        html.Small(f"💰 {hotel.get('price_range', '')} | 📍 {hotel.get('location', '')}")
                    ]) for hotel in recommendations.get('hotels', [])
                ], className="hotels-list")
            ], className="hotels-section"),
            
            html.Hr(),
            
            html.Div([
                html.H6("🚌 Transporte:", className="section-title"),
                html.P(recommendations.get('transport_info', ''), className="transport-info")
            ], className="transport-section"),
            
            html.Hr(),
            
            html.Div([
                html.H6("💡 Consejos generales:", className="section-title"),
                html.Ul([
                    html.Li(tip) for tip in recommendations.get('general_tips', [])
                ], className="tips-list")
            ], className="general-tips-section")
        ])
    ], className="recommendations-card magical-card")


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
    app.run(debug=True, host='0.0.0.0', port=8050)