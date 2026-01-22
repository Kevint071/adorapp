"""
Vista para editar caracteres
"""
import flet as ft
from components import create_header, create_character_item, show_snackbar
from .theme_utils import get_theme_colors


class CharacterSettingsView:
    """Vista para editar caracteres"""

    def __init__(self, page, app):
        self.page = page
        self.app = app
        self.characters_list = ft.Column([], spacing=8, scroll=ft.ScrollMode.AUTO, expand=True)
        self.new_character_field = self._create_new_character_field()

    def _create_new_character_field(self):
        colors = get_theme_colors(self.page)
        return ft.TextField(
            hint_text="Nuevo carácter...",
            border_color=colors["border_color"],
            focused_border_color=colors["border_focused"],
            bgcolor=colors["bg_secondary"],
            color=colors["text_primary"],
            height=55,
            text_size=14,
            border_radius=12,
        )

    def refresh_theme(self):
        """Actualiza los estilos según el tema"""
        colors = get_theme_colors(self.page)
        self.new_character_field.border_color = colors["border_color"]
        self.new_character_field.bgcolor = colors["bg_secondary"]
        self.new_character_field.color = colors["text_primary"]

    def refresh_characters_list(self):
        """Actualiza la lista de caracteres"""
        self.characters_list.controls.clear()
        for char in self.app.get_characters():
            self.characters_list.controls.append(
                create_character_item(self.page, char, self.remove_character_handler)
            )
        self.page.update()

    def add_character_handler(self, main_view):
        """Agrega un nuevo carácter"""
        if self.new_character_field.value and self.new_character_field.value.strip():
            if self.app.add_character(self.new_character_field.value.strip()):
                self.new_character_field.value = ""
                self.refresh_characters_list()
                main_view.refresh_character_options()
                show_snackbar(self.page, "Carácter agregado exitosamente", "#00b894")

    def remove_character_handler(self, character):
        """Elimina un carácter"""
        if self.app.remove_character(character):
            self.refresh_characters_list()
            show_snackbar(self.page, "Carácter eliminado exitosamente", "#ff7675")

    def build(self, main_view):
        """Construye la vista de edición de caracteres"""
        colors = get_theme_colors(self.page)
        
        self.refresh_theme()
        
        header = create_header(
            self.page,
            "Editar Caracteres",
            ["#fd79a8", "#fdcb6e"],
            left_button=ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color="#ffffff",
                icon_size=26,
                on_click=lambda e: self.page.go("/settings"),
                tooltip="Volver"
            ),
        )

        content = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.CATEGORY, size=22, color="#74b9ff"),
                    ft.Text("Gestión de Caracteres", size=18, weight=ft.FontWeight.BOLD, color=colors["text_primary"])
                ], spacing=10),
                ft.Container(height=8),
                ft.Row([
                    ft.Container(content=self.new_character_field, expand=True),
                    ft.IconButton(
                        icon=ft.Icons.ADD_CIRCLE,
                        icon_color="#00b894",
                        icon_size=32,
                        on_click=lambda e: self.add_character_handler(main_view),
                        tooltip="Agregar carácter"
                    ),
                ], spacing=8),
                ft.Container(
                    content=ft.Container(height=1, bgcolor=colors["border_color"]),
                    margin=ft.margin.symmetric(vertical=16),
                ),
                ft.Text("Caracteres disponibles:", size=14, color=colors["text_secondary"], weight=ft.FontWeight.W_500),
                ft.Container(height=8),
                self.characters_list,
            ], spacing=12, expand=True),
            padding=16,
            expand=True,
        )

        return ft.View(
            "/settings/characters",
            [header, content],
            bgcolor=colors["bg_primary"],
            padding=0,
        )