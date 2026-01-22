"""
Vista principal con listado de canciones
"""
import flet as ft
from models import MUSICAL_KEYS
from components import create_song_card, create_header, create_empty_state
from .theme_utils import get_theme_colors


class MainView:
    """Vista principal con listado de canciones"""
    
    def __init__(self, page, app):
        self.page = page
        self.app = app
        self.results_column = ft.Column([], spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)
        
        # Crear campos de búsqueda y filtros
        self.search_field = self._create_search_field()
        self.key_filter = self._create_key_filter()
        self.character_filter = self._create_character_filter()
        self.tempo_filter = self._create_tempo_filter()
        self.clear_button = self._create_clear_button()
        
    def _create_search_field(self):
        colors = get_theme_colors(self.page)
        return ft.TextField(
            hint_text="Buscar canción...",
            prefix_icon=ft.Icons.SEARCH,
            border_color=colors["border_color"],
            focused_border_color=colors["border_focused"],
            bgcolor=colors["bg_secondary"],
            color=colors["text_primary"],
            on_change=lambda e: self.search_handler(e),
            text_size=14,
            border_radius=12,
            expand=True,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=16),
        )
    
    def _create_key_filter(self):
        colors = get_theme_colors(self.page)
        return ft.Dropdown(
            hint_text="Tono",
            options=[ft.dropdown.Option("Tono")] + [ft.dropdown.Option(key) for key in MUSICAL_KEYS],
            border_color=colors["border_color"],
            focused_border_color=colors["border_focused"],
            bgcolor=colors["bg_secondary"],
            color=colors["text_primary"],
            on_change=lambda e: self.search_handler(e),
            text_size=13,
            border_radius=12,
            expand=True,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
        )
    
    def _create_character_filter(self):
        colors = get_theme_colors(self.page)
        return ft.Dropdown(
            hint_text="Carácter",
            options=[ft.dropdown.Option("Carácter")] + [ft.dropdown.Option(char) for char in self.app.get_characters()],
            border_color=colors["border_color"],
            focused_border_color=colors["border_focused"],
            bgcolor=colors["bg_secondary"],
            color=colors["text_primary"],
            on_change=lambda e: self.search_handler(e),
            text_size=13,
            border_radius=12,
            expand=True,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
        )
    
    def _create_tempo_filter(self):
        colors = get_theme_colors(self.page)
        return ft.Dropdown(
            hint_text="Ritmo",
            options=[
                ft.dropdown.Option("Ritmo"),
                ft.dropdown.Option("Lenta"),
                ft.dropdown.Option("Rápida"),
            ],
            border_color=colors["border_color"],
            focused_border_color=colors["border_focused"],
            bgcolor=colors["bg_secondary"],
            color=colors["text_primary"],
            on_change=lambda e: self.search_handler(e),
            text_size=13,
            border_radius=12,
            expand=True,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
        )
    
    def _create_clear_button(self):
        colors = get_theme_colors(self.page)
        return ft.Container(
            content=ft.IconButton(
                icon=ft.Icons.FILTER_ALT_OFF,
                icon_color="#ff7675",
                icon_size=20,
                on_click=self.clear_filters_handler,
                tooltip="Limpiar filtros"
            ),
            bgcolor=colors["bg_secondary"],
            border_radius=12,
            border=ft.border.all(1, colors["border_color"]),
            width=50,
            height=50,
            expand=False,
            alignment=ft.alignment.center,
        )
    
    def update_results(self, songs):
        """Actualiza los resultados mostrados"""
        self.results_column.controls.clear()
        if not songs:
            self.results_column.controls.append(create_empty_state(self.page, "No hay canciones"))
        else:
            for song in songs:
                self.results_column.controls.append(
                    create_song_card(self.page, song, self.go_to_edit)
                )
        self.page.update()
    
    def search_handler(self, e):
        """Búsqueda con filtros"""
        query = self.search_field.value.strip() if self.search_field.value else ""
        key = self.key_filter.value if self.key_filter.value and self.key_filter.value != "Tono" else ""
        character = self.character_filter.value if self.character_filter.value and self.character_filter.value != "Carácter" else ""
        tempo = self.tempo_filter.value if self.tempo_filter.value and self.tempo_filter.value != "Ritmo" else ""
        
        songs = self.app.search_songs(query, key, character, tempo)
        self.update_results(songs)
    
    def clear_filters_handler(self, e):
        """Limpia todos los filtros"""
        self.search_field.value = ""
        self.key_filter.value = "Tono"
        self.character_filter.value = "Carácter"
        self.tempo_filter.value = "Ritmo"
        self.search_handler(None)
    
    def go_to_edit(self, song):
        """Navega a la vista de edición"""
        self.page.session.set("editing_song", song)
        self.page.go("/edit")
    
    def refresh_character_options(self):
        """Actualiza las opciones de caracteres en el filtro"""
        self.character_filter.options = [ft.dropdown.Option("Carácter")] + [
            ft.dropdown.Option(char) for char in self.app.get_characters()
        ]
    
    def refresh_theme(self):
        """Actualiza los estilos según el tema"""
        colors = get_theme_colors(self.page)
        # Actualizar search field
        self.search_field.border_color = colors["border_color"]
        self.search_field.bgcolor = colors["bg_secondary"]
        self.search_field.color = colors["text_primary"]
        # Actualizar filtros
        for control in [self.key_filter, self.character_filter, self.tempo_filter]:
            control.border_color = colors["border_color"]
            control.bgcolor = colors["bg_secondary"]
            control.color = colors["text_primary"]
        # Actualizar botón de limpiar
        self.clear_button.bgcolor = colors["bg_secondary"]
        self.clear_button.border = ft.border.all(1, colors["border_color"])
        # Actualizar resultados (tarjetas)
        self.update_results(self.app.search_songs(
            self.search_field.value.strip() if self.search_field.value else "",
            self.key_filter.value if self.key_filter.value and self.key_filter.value != "Tono" else "",
            self.character_filter.value if self.character_filter.value and self.character_filter.value != "Carácter" else "",
            self.tempo_filter.value if self.tempo_filter.value and self.tempo_filter.value != "Ritmo" else "",
        ))

    def build(self):
        """Construye la vista"""
        colors = get_theme_colors(self.page)
        
        self.refresh_theme()
        
        header = create_header(
            self.page,
            "Mis Canciones",
            ["#6c5ce7", "#a29bfe"],
            left_button=ft.Row([
                ft.Container(
                    content=ft.Icon(
                        ft.Icons.MUSIC_NOTE,
                        color="#ffffff",
                        size=26
                    ),
                    width=48,
                    height=48,
                    alignment=ft.alignment.center,
                    bgcolor=ft.Colors.with_opacity(0.15, "#6c5ce7"),
                    border_radius=16,
                    blur=12,
                    border=ft.border.all(1, ft.Colors.with_opacity(0.2, "#ffffff")),
                ),
            ], spacing=12),
            right_buttons=[
                # Configuración
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.SETTINGS_ROUNDED,
                        icon_color="#ffffff",
                        icon_size=22,
                        on_click=lambda e: self.page.go("/settings"),
                        tooltip="Configuración"
                    ),
                    width=48,
                    height=48,
                    alignment=ft.alignment.center,
                    bgcolor=ft.Colors.with_opacity(0.18, "#ffffff"),
                    border_radius=16,
                    blur=14,
                    border=ft.border.all(1, ft.Colors.with_opacity(0.15, "#ffffff")),
                ),
                # Agregar canción
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.ADD_ROUNDED,
                        icon_color="#ffffff",
                        icon_size=22,
                        on_click=lambda e: self.page.go("/add"),
                        tooltip="Agregar canción"
                    ),
                    width=48,
                    height=48,
                    alignment=ft.alignment.center,
                    gradient=ft.LinearGradient(
                        colors=["#00e5a8", "#00b894"],
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                    ),
                    border_radius=18,
                    shadow=ft.BoxShadow(
                        blur_radius=18,
                        spread_radius=1,
                        color=ft.Colors.with_opacity(0.4, "#00b894"),
                    ),
                ),
            ]
        )
        
        filters = ft.Container(
            content=ft.Column([
                ft.Row([
                    self.search_field,
                    self.clear_button,
                ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Row([
                    self.key_filter,
                    self.character_filter,
                    self.tempo_filter,
                ], spacing=8, expand=True),
            ], spacing=12),
            padding=16,
        )
        
        results = ft.Container(
            content=self.results_column,
            padding=ft.padding.only(left=16, right=16, bottom=16),
            expand=True,
        )
        
        return ft.View(
            "/",
            [header, filters, results],
            bgcolor=colors["bg_primary"],
            padding=0,
        )