from dash import html
import dash_bootstrap_components as dbc


def create_results_section():
    """Crear la sección de resultados del itinerario"""
    return html.Div([
        html.Div([
            html.H3([
                "🗺️ Tu Aventura Mágica",
                html.Br(),
                html.Small("Aquí aparecerá tu plan personalizado", 
                          className="results-subtitle")
            ], className="results-title"),
            
            # Placeholder inicial
            html.Div([
                create_placeholder_content()
            ], id="results-container", className="results-container")
        ], className="results-section")
    ])


def create_placeholder_content():
    """Crear contenido placeholder antes de generar el itinerario"""
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.Img(
                    src="/assets/Ratoncito.png",
                    className="placeholder-icon"
                ),
                html.H4([
                    "¡El Ratoncito Pérez está esperando! 🐭✨"
                ], className="placeholder-title"),
                
                html.P([
                    "Completa el formulario de la izquierda para que pueda ",
                    "crear tu aventura mágica personalizada por Madrid."
                ], className="placeholder-text"),
                
                html.Div([
                    html.Div([
                        html.I(className="fas fa-map-marked-alt", style={"color": "#FF6B6B"}),
                        html.Span("Itinerarios detallados día a día")
                    ], className="feature-item"),
                    
                    html.Div([
                        html.I(className="fas fa-utensils", style={"color": "#4ECDC4"}),
                        html.Span("Restaurantes familiares recomendados")
                    ], className="feature-item"),
                    
                    html.Div([
                        html.I(className="fas fa-bed", style={"color": "#45B7D1"}),
                        html.Span("Alojamientos perfectos para familias")
                    ], className="feature-item"),
                    
                    html.Div([
                        html.I(className="fas fa-star", style={"color": "#F7DC6F"}),
                        html.Span("Consejos mágicos del Ratoncito Pérez")
                    ], className="feature-item"),
                    
                    html.Div([
                        html.I(className="fas fa-ticket-alt", style={"color": "#BB8FCE"}),
                        html.Span("Información práctica y reservas")
                    ], className="feature-item")
                ], className="features-preview")
                
            ], className="placeholder-content")
        ])
    ], className="placeholder-card magical-card")


def create_itinerary_card(day_info):
    """Crear una tarjeta individual para un día del itinerario"""
    return dbc.Card([
        dbc.CardHeader([
            html.Div([
                html.H5([
                    f"🌟 {day_info.get('title', 'Día de Aventura')}"
                ], className="day-card-title"),
                html.P(
                    day_info.get('theme', 'Descubriendo la magia de Madrid'),
                    className="day-theme"
                )
            ])
        ], className="day-card-header"),
        
        dbc.CardBody([
            # Timeline de actividades
            create_activities_timeline(day_info.get('activities', [])),
            
            # Restaurantes del día
            create_restaurants_section(day_info.get('restaurants', [])),
            
            # Consejo mágico
            create_magical_tip(day_info.get('tip', ''))
        ])
    ], className="day-card magical-card")


def create_activities_timeline(activities):
    """Crear timeline de actividades del día"""
    if not activities:
        return html.Div()
    
    timeline_items = []
    for activity in activities:
        timeline_items.append(
            html.Div([
                html.Div([
                    html.Span(activity.get('time', ''), className="activity-time"),
                    html.Div(className="timeline-dot")
                ], className="timeline-marker"),
                
                html.Div([
                    html.H6(activity.get('name', ''), className="activity-name"),
                    html.P(activity.get('description', ''), className="activity-description"),
                    
                    # Tags de la actividad
                    html.Div([
                        html.Span([
                            html.I(className="fas fa-map-marker-alt"),
                            f" {activity.get('location', '')}"
                        ], className="activity-tag location-tag") if activity.get('location') else "",
                        
                        html.Span([
                            html.I(className="fas fa-euro-sign"),
                            f" {activity.get('price', 'Gratis')}"
                        ], className="activity-tag price-tag") if activity.get('price') else "",
                        
                        html.Span([
                            html.I(className="fas fa-clock"),
                            f" {activity.get('duration', '')}"
                        ], className="activity-tag duration-tag") if activity.get('duration') else ""
                    ], className="activity-tags")
                ], className="timeline-content")
            ], className="timeline-item")
        )
    
    return html.Div([
        html.H6("📅 Programa del día:", className="section-title"),
        html.Div(timeline_items, className="activities-timeline")
    ], className="timeline-section")


def create_restaurants_section(restaurants):
    """Crear sección de restaurantes recomendados"""
    if not restaurants:
        return html.Div()
    
    restaurant_cards = []
    for restaurant in restaurants:
        restaurant_cards.append(
            html.Div([
                html.Div([
                    html.H6(restaurant.get('name', ''), className="restaurant-name"),
                    html.P(restaurant.get('cuisine', ''), className="restaurant-cuisine"),
                    html.P([
                        html.I(className="fas fa-map-marker-alt"),
                        f" {restaurant.get('address', '')}"
                    ], className="restaurant-address"),
                    
                    html.Div([
                        html.Span([
                            "⭐ " * int(restaurant.get('rating', 0)),
                            f" ({restaurant.get('rating', 'N/A')})"
                        ], className="restaurant-rating"),
                        html.Span(
                            restaurant.get('price_range', ''),
                            className="restaurant-price"
                        )
                    ], className="restaurant-info")
                ])
            ], className="restaurant-card")
        )
    
    return html.Div([
        html.H6("🍽️ Restaurantes recomendados:", className="section-title"),
        html.Div(restaurant_cards, className="restaurants-grid")
    ], className="restaurants-section")


def create_magical_tip(tip_text):
    """Crear el consejo mágico del Ratoncito Pérez"""
    if not tip_text:
        return html.Div()
    
    return dbc.Alert([
        html.Div([
            html.Img(
                src="/assets/Ratoncito.png",
                className="tip-icon"
            ),
            html.Div([
                html.Strong("💫 Consejo Mágico del Ratoncito Pérez:"),
                html.P(tip_text, className="tip-text")
            ], className="tip-content")
        ], className="tip-container")
    ], color="info", className="magical-tip")


def create_summary_card(itinerary_data):
    """Crear tarjeta resumen del itinerario"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5("📋 Resumen de tu Aventura", className="summary-title")
        ]),
        
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.I(className="fas fa-calendar-alt", style={"color": "#FF6B6B"}),
                        html.Span(f" {itinerary_data.get('total_days', 0)} días")
                    ], className="summary-item")
                ], width=6),
                
                dbc.Col([
                    html.Div([
                        html.I(className="fas fa-map-marked-alt", style={"color": "#4ECDC4"}),
                        html.Span(f" {len(itinerary_data.get('total_activities', []))} actividades")
                    ], className="summary-item")
                ], width=6)
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.I(className="fas fa-utensils", style={"color": "#45B7D1"}),
                        html.Span(f" {len(itinerary_data.get('total_restaurants', []))} restaurantes")
                    ], className="summary-item")
                ], width=6),
                
                dbc.Col([
                    html.Div([
                        html.I(className="fas fa-euro-sign", style={"color": "#F7DC6F"}),
                        html.Span(f" ~{itinerary_data.get('estimated_cost', 0)}€ total")
                    ], className="summary-item")
                ], width=6)
            ]),
            
            html.Hr(),
            
            # Botones de acción
            html.Div([
                dbc.Button([
                    html.I(className="fas fa-download"),
                    " Descargar PDF"
                ], color="outline-primary", className="action-btn"),
                
                dbc.Button([
                    html.I(className="fas fa-share-alt"),
                    " Compartir"
                ], color="outline-secondary", className="action-btn"),
                
                dbc.Button([
                    html.I(className="fas fa-heart"),
                    " Guardar"
                ], color="outline-success", className="action-btn")
            ], className="action-buttons")
        ])
    ], className="summary-card magical-card")