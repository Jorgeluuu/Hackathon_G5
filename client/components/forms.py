from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime, date, timedelta


def create_planning_form():
    """Crear el formulario principal de planificación"""
    return dbc.Card([
        dbc.CardHeader([
            html.H4([
                "🎪 Planifica tu Aventura Mágica",
                html.Br(),
                html.Small("Cuéntale al Ratoncito Pérez sobre tu familia", 
                          className="form-subtitle")
            ], className="form-title")
        ], className="form-header"),
        
        dbc.CardBody([
            create_destination_section(),
            
            html.Hr(className="form-divider"),
            
            create_duration_budget_section(),
            
            html.Hr(className="form-divider"),
            
            create_family_section(),
            
            html.Hr(className="form-divider"),
            
            create_interests_section(),
            
            html.Hr(className="form-divider"),
            
            create_generate_button()
        ])
    ], className="planning-form magical-card")


def create_destination_section():
    """Sección de selección de destino"""
    return html.Div([
        html.Label([
            "📍 ¿Dónde quieres vivir la magia?",
            html.Span(" *", className="required-field")
        ], className="form-label"),
        dbc.Select(
            id="destination-input",
            options=[
                {"label": "🏛️ Madrid Centro", "value": "Madrid Centro"},
                {"label": "🎪 Madrid Completo", "value": "Madrid Completo"},
            ],
            placeholder="Selecciona tu destino mágico...",
            className="magical-select"
        ),
        html.Small(
            "El Ratoncito Pérez conoce los mejores rincones de cada zona 🐭",
            className="form-help-text"
        )
    ], className="form-section")


def create_duration_budget_section():
    """Sección de duración y presupuesto"""
    return html.Div([
        # Duración
        html.Div([
            html.Label("⏰ Duración de tu aventura", className="form-label"),
            dcc.Slider(
                id="duration-slider",
                min=1,
                max=7,
                step=1,
                value=2,
                marks={
                    1: {'label': '1 día', 'style': {'color': "#FFFFFF"}},
                    2: {'label': '2 días', 'style': {'color': "#FFFFFF"}},
                    3: {'label': '3 días', 'style': {'color': "#FFFFFF"}},
                    4: {'label': '4 días', 'style': {'color': "#FFFFFF"}},
                    5: {'label': '5 días', 'style': {'color': "#FFFFFF"}},
                    6: {'label': '6 días', 'style': {'color': "#FFFFFF"}},
                    7: {'label': '1 semana', 'style': {'color': "#FFFFFF"}}
                },
                className="magical-slider"
            )
        ], className="slider-section"),
        
        html.Br(),
        
        # Presupuesto
        html.Div([
            html.Label("💰 Presupuesto aproximado por persona/día", className="form-label"),
            dcc.Slider(
                id="budget-slider",
                min=30,
                max=200,
                step=10,
                value=80,
                marks={
                    30: {'label': '300€', 'style': {'color': "#FFFFFF"}},
                    60: {'label': '600€', 'style': {'color': "#FFFFFF"}},
                    100: {'label': '900€', 'style': {'color': "#FFFFFF"}},
                    150: {'label': '1200€', 'style': {'color': "#FFFFFF"}},
                    200: {'label': '1500€+', 'style': {'color': "#FFFFFF"}}
                },
                className="magical-slider"
            ),
            html.Small(
                "Incluye comidas, actividades y transporte básico 🎪",
                className="form-help-text"
            )
        ], className="slider-section")
    ], className="form-section")


def create_family_section():
    """Sección de información familiar"""
    return html.Div([
        html.Label("👨‍👩‍👧‍👦 Háblanos de tu familia", className="form-label"),
        
        html.Div([
            html.Label("Edades de los niños:", className="sub-label"),
            dbc.Textarea(
                id="children-ages",
                placeholder="Ejemplo: 5, 8, 12 años",
                rows=1,
                maxLength=10,
                className="magical-textarea",
                style={
                    'resize': 'none',  
                    'overflow': 'hidden' 
                }
            ),
            html.Small(
                "Esto ayuda al Ratoncito Pérez a personalizar las actividades 🎈",
                className="form-help-text"
            )
        ], className="input-group")
    ], className="form-section")


def create_interests_section():
    """Sección de intereses y preferencias"""
    return html.Div([
        html.Label("🎯 ¿Qué les gusta hacer?", className="form-label"),
        dbc.Checklist(
            id="interests-checklist",
            options=[
                {"label": "🏛️ Museos y cultura", "value": "museums"},
                {"label": "🌳 Parques y naturaleza", "value": "parks"},
                {"label": "🎪 Espectáculos y teatros", "value": "shows"},
                {"label": "🏰 Historia y monumentos", "value": "history"},
                {"label": "🍽️ Gastronomía", "value": "food"},
                {"label": "🛍️ Compras y mercados", "value": "shopping"},
                {"label": "🎨 Arte y creatividad", "value": "art"},
                {"label": "⚽ Deportes", "value": "sports"},
                {"label": "🎢 Diversión y aventura", "value": "adventure"},
                {"label": "📚 Aprendizaje interactivo", "value": "learning"}
            ],
            value=["museums", "parks", "shows"],
            className="magical-checklist",
            inline=False
        ),
        html.Small(
            "¡Selecciona todo lo que os emocione! El Ratoncito Pérez lo combinará mágicamente ✨",
            className="form-help-text"
        )
    ], className="form-section")


def create_generate_button():
    """Botón para generar el plan"""
    return html.Div([
        dbc.Button([
            html.I(className="fas fa-magic"),
            " ¡Crear mi Aventura Mágica!"
        ],
        id="generate-plan-btn",
        color="primary",
        size="lg",
        className="generate-button magical-button"),
        
        html.Div(id="loading-spinner", className="loading-container"),
        
        html.Small(
            "El Ratoncito Pérez creará un plan personalizado para tu familia 🐭✨",
            className="button-help-text"
        )
    ], className="button-section", style={"text-align": "center"})