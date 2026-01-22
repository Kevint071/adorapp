"""
Utilidades para manejo de temas
"""

def get_theme_colors(page):
    """Retorna los colores según el tema activo"""
    is_light = page.session.get("theme_mode") == "light"
    
    return {
        "bg_primary": "#f5f6fa" if is_light else "#0a0e27",
        "bg_secondary": "#ffffff" if is_light else "#1e2347",
        "bg_tertiary": "#e8eaf0" if is_light else "#2d3561",
        "text_primary": "#2d3436" if is_light else "#ffffff",
        "text_secondary": "#636e72" if is_light else "#b2bec3",
        "border_color": "#dfe6e9" if is_light else "#2d3561",
        "border_focused": "#6c5ce7",
        "card_shadow": "#00000020" if is_light else "#00000010",
        "icon_color": "#6c5ce7",
        "empty_icon": "#b2bec3" if is_light else "#2d3561",
    }