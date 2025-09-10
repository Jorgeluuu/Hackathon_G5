"""
Componentes de formularios para la planificación mágica
"""

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
            # Destino
            create_destination_section(),
            
            html.Hr(className="form-divider"),
            
            # Fechas
            create_dates_section(),
            
            html.Hr(className="form-divider"),
            
            # Duración y presupuesto
            create_duration_budget_section(),
            
            html.Hr(className="form-divider"),
            
            # Información familiar
            create_family_section(),
            
            html.Hr(className="form-divider"),
            
            # Intereses
            create_interests_section(),
            
            html.Hr(className="form-divider"),
            
            # Botón de generar
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
                {"label": "🌳 Madrid + Alrededores", "value": "Madrid Alrededores"},
                {"label": "🎪 Madrid Completo", "value": "Madrid Completo"},
                {"label": "🏰 Madrid + Toledo", "value": "Madrid Toledo"},
                {"label": "🌲 Madrid + Segovia", "value": "Madrid Segovia"}
            ],
            placeholder="Selecciona tu destino mágico...",
            className="magical-select"
        ),
        html.Small(
            "El Ratoncito Pérez conoce los mejores rincones de cada zona 🐭",
            className="form-help-text"
        )
    ], className="form-section")


def create_dates_section():
    """Sección de selección de fechas"""
    today = date.today()
    max_date = today + timedelta(days=365)
    
    return html.Div([
        html.Label([
            "📅 ¿Cuándo comenzará tu aventura?",
            html.Span(" *", className="required-field")
        ], className="form-label"),
        dcc.DatePickerSingle(
            id="date-picker",
            date=today + timedelta(days=7),
            min_date_allowed=today,
            max_date_allowed=max_date,
            display_format='DD/MM/YYYY',
            className="magical-date-picker"
        ),
        html.Small(
            "¡El Ratoncito Pérez está disponible todo el año! ✨",
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
                    1: {'label': '1 día', 'style': {'color': '#8B4513'}},
                    2: {'label': '2 días', 'style': {'color': '#8B4513'}},
                    3: {'label': '3 días', 'style': {'color': '#8B4513'}},
                    4: {'label': '4 días', 'style': {'color': '#8B4513'}},
                    5: {'label': '5 días', 'style': {'color': '#8B4513'}},
                    6: {'label': '6 días', 'style': {'color': '#8B4513'}},
                    7: {'label': '1 semana', 'style': {'color': '#8B4513'}}
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
                    30: {'label': '30€', 'style': {'color': '#8B4513'}},
                    60: {'label': '60€', 'style': {'color': '#8B4513'}},
                    100: {'label': '100€', 'style': {'color': '#8B4513'}},
                    150: {'label': '150€', 'style': {'color': '#8B4513'}},
                    200: {'label': '200€+', 'style': {'color': '#8B4513'}}
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
                rows=2,
                className="magical-textarea"
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