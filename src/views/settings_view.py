import flet as ft
from components import create_header
from .theme_utils import get_theme_colors


class SettingsView:
    """Vista de configuración principal"""

    def __init__(self, page, app):
        self.page = page
        self.app = app

    def _get_theme_mode(self):
        return self.page.session.get("theme_mode") or "dark"

    def _set_theme_mode(self, mode, main_view):
        self.page.session.set("theme_mode", mode)
        self.page.theme_mode = ft.ThemeMode.LIGHT if mode == "light" else ft.ThemeMode.DARK
        self.page.bgcolor = "#f5f6fa" if mode == "light" else "#0a0e27"

        self.page.views.clear()
        self.page.views.append(self.build(main_view) if main_view else self.build(None))
        self.page.update()

        # Actualizar MainView si está presente
        if hasattr(self.page, "main_view") and self.page.main_view:
            self.page.main_view.refresh_theme()

    def build(self, main_view):
        """Construye la vista de configuración principal"""
        colors = get_theme_colors(self.page)
        
        header = create_header(
            self.page,
            "Configuración",
            ["#fd79a8", "#fdcb6e"],
            left_button=ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color="#ffffff",
                icon_size=26,
                on_click=lambda e: self.page.go("/"),
                tooltip="Volver"
            ),
        )

        theme_mode = self._get_theme_mode()
        is_light_mode = theme_mode == "light"
        
        # Icono y texto dinámicos según el modo actual
        theme_icon = ft.Icon(
            ft.Icons.LIGHT_MODE if is_light_mode else ft.Icons.DARK_MODE,
            size=22,
            color="#fdcb6e" if is_light_mode else "#74b9ff"
        )
        
        theme_text = ft.Text(
            "Modo Claro" if is_light_mode else "Modo Oscuro",
            size=16,
            weight=ft.FontWeight.W_500,
            color=colors["text_primary"]
        )
        
        theme_switch = ft.Switch(
            value=is_light_mode,
            on_change=lambda e: self._set_theme_mode("light" if e.control.value else "dark", main_view),
            active_color="#00b894",
            inactive_thumb_color="#636e72",
            inactive_track_color="#b2bec3",
        )

        theme_settings_container = ft.Container(
            content=ft.Row([
                theme_icon,
                theme_text,
                ft.Container(expand=True),
                theme_switch,
            ], spacing=10),
            bgcolor=colors["bg_secondary"],
            padding=16,
            border_radius=12,
            border=ft.border.all(1, colors["border_color"]),
        )

        character_settings_btn = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.CATEGORY, size=22, color="#74b9ff"),
                ft.Text("Personalizar Caracteres", size=16, weight=ft.FontWeight.W_500, color=colors["text_primary"]),
                ft.Container(expand=True),
                ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=18, color=colors["text_secondary"]),
            ], spacing=10),
            bgcolor=colors["bg_secondary"],
            padding=16,
            border_radius=12,
            border=ft.border.all(1, colors["border_color"]),
            on_click=lambda e: self.page.go("/settings/characters"),
            ink=True,
        )

        content = ft.Container(
            content=ft.Column([
                ft.Text("Preferencias", size=18, weight=ft.FontWeight.BOLD, color=colors["text_primary"]),
                ft.Container(height=12),
                theme_settings_container,
                ft.Container(height=16),
                character_settings_btn,
            ], spacing=8, expand=True),
            padding=16,
            expand=True,
        )

        return ft.View(
            "/settings",
            [header, content],
            bgcolor=colors["bg_primary"],
            padding=0,
        )