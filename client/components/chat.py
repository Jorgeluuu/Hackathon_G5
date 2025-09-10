from dash import html, dcc
import dash_bootstrap_components as dbc


def create_chat_section():
    """Crear la sección de chat con el Ratoncito Pérez"""
    return html.Div([
        html.Div([
            html.H4([
                "💬 Chatea con el Ratoncito Pérez",
                html.Br(),
                html.Small("¡Pregúntame cualquier cosa sobre tu aventura!", 
                          className="chat-subtitle")
            ], className="chat-title")
        ], className="chat-header"),
        
        # Área de mensajes
        html.Div([
            html.Div(
                id="chat-messages",
                className="chat-messages-container"
            )
        ], className="chat-messages-area"),
        
        # Input de chat
        create_chat_input()
        
    ], className="chat-section")


def create_chat_input():
    """Crear el área de input del chat"""
    return html.Div([
        dbc.InputGroup([
            dbc.Textarea(
                id="chat-input",
                placeholder="Escríbele al Ratoncito Pérez... ✨",
                rows=2,
                className="chat-input-field"
            ),
            dbc.Button([
                html.I(className="fas fa-paper-plane")
            ], 
            id="send-message-btn",
            color="primary",
            className="send-button magical-button")
        ], className="chat-input-group"),
        
    ], className="chat-input-section")


def create_chat_message(message_data, sender_type="user"):
    """Crear un mensaje individual del chat"""
    if sender_type == "user":
        message_class = "user-message"
        avatar = "👤"
        align_class = "message-right"
    else:
        message_class = "mouse-message"
        avatar = "🐭"
        align_class = "message-left"
    
    return html.Div([
        html.Div([
            # Avatar
            html.Div([
                html.Span(avatar, className="message-avatar")
            ], className="avatar-container"),
            
            # Contenido del mensaje
            html.Div([
                html.Div([
                    message_data.get("message", ""),
                    html.Div(
                        format_timestamp(message_data.get("timestamp", "")),
                        className="message-timestamp"
                    )
                ], className=f"message-bubble {message_class}")
            ], className="message-content")
            
        ], className=f"message-item {align_class}")
    ], className="message-container")


def create_typing_indicator():
    """Crear indicador de escritura del Ratoncito Pérez"""
    return html.Div([
        html.Div([
            html.Span("🐭", className="message-avatar")
        ], className="avatar-container"),
        
        html.Div([
            html.Div([
                html.Div([
                    html.Span(className="typing-dot"),
                    html.Span(className="typing-dot"),
                    html.Span(className="typing-dot")
                ], className="typing-animation"),
                html.Small("El Ratoncito Pérez está escribiendo...", 
                          className="typing-text")
            ], className="typing-indicator")
        ], className="message-content")
    ], className="message-container message-left")


def create_welcome_message():
    """Crear mensaje de bienvenida del chat"""
    return html.Div([
        html.Div([
            html.Img(
                src="/assets/Ratoncito.png",
                className="welcome-mouse-icon"
            ),
            html.Div([
                html.H6("¡Hola! Soy el Ratoncito Pérez 🐭✨", 
                       className="welcome-title"),
                html.P([
                    "Estoy aquí para ayudarte con cualquier pregunta sobre tu aventura en Madrid. ",
                    "¿Hay algo específico que te gustaría saber?"
                ], className="welcome-text"),
                
                # Botones de inicio rápido
                html.Div([
                    dbc.Button("🗺️ ¿Cómo usar el metro?", 
                              size="sm", color="link", 
                              className="quick-btn"),
                    dbc.Button("🎪 ¿Actividades gratis?", 
                              size="sm", color="link", 
                              className="quick-btn"),
                    dbc.Button("🍽️ ¿Restaurantes familiares?", 
                              size="sm", color="link", 
                              className="quick-btn")
                ], className="quick-buttons")
            ], className="welcome-content")
        ], className="welcome-message-container")
    ], className="welcome-message")


def format_timestamp(timestamp_str):
    """Formatear timestamp para mostrar en el chat"""
    if not timestamp_str:
        return ""
    
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime("%H:%M")
    except:
        return ""


def create_chat_error_message():
    """Crear mensaje de error en el chat"""
    return html.Div([
        dbc.Alert([
            html.I(className="fas fa-exclamation-triangle"),
            " ¡Ups! El Ratoncito Pérez tuvo un pequeño problema. ¿Puedes intentar de nuevo?"
        ], color="warning", className="chat-error-alert")
    ], className="error-message-container")