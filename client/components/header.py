from dash import html
import dash_bootstrap_components as dbc


def create_header():
    return html.Header([
        dbc.Navbar([
            dbc.Container([
                # Logo y título
                dbc.NavbarBrand([
                    html.Img(
                        src="assets/Brujula.png",
                        height="50px",
                        className="navbar-logo"
                    ),
                    html.Span([
                        "Brújula Mágica ",
                        html.Span("del Ratoncito Pérez", className="brand-highlight")
                    ], className="navbar-title")
                ], href="/", className="navbar-brand-custom"),
            ], fluid=True)
        ], color="light", className="magical-navbar"),
        
        # Hero section
        html.Div([
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H1([
                                "¡Descubre Madrid con Magia! ✨",
                                html.Br(),
                                html.Small("Tu aventura familiar perfecta te espera", 
                                         className="hero-subtitle")
                            ], className="hero-title"),
                            
                            html.P([
                                "El Ratoncito Pérez ha guardado todos los secretos de Madrid ",
                                "especialmente para tu familia. ¡Deja que te guíe en una ",
                                "aventura inolvidable! 🐭🎪"
                            ], className="hero-description"),
                        ], className="hero-content")
                    ], width=12)
                ])
            ], fluid=True)
        ], className="hero-section"),
        
        # Decorative elements
        html.Div([
            create_floating_elements()
        ], className="decorative-elements")
    ])


def create_floating_elements():
    return html.Div([
        html.Div("⭐", className="floating-star star-1"),
        html.Div("✨", className="floating-star star-2"),
        html.Div("🌟", className="floating-star star-3"),
        html.Div("💫", className="floating-star star-4"),
        html.Div("🎪", className="floating-element element-1"),
        html.Div("🎭", className="floating-element element-2"),
        html.Div("🎨", className="floating-element element-3")
    ], className="floating-container")
