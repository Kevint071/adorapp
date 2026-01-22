"""
Vista base para agregar/editar canciones con múltiples caracteres
"""

import flet as ft
from time import sleep
from models import MUSICAL_KEYS
from components import create_header, show_snackbar
from .theme_utils import get_theme_colors


class SongFormView:
    """Vista base para agregar/editar canciones"""

    # ✅ Constantes para opciones especiales (placeholders)
    PLACEHOLDER_TONO = "-- Seleccionar Tono --"
    PLACEHOLDER_CARACTER = "-- Seleccionar Carácter --"
    PLACEHOLDER_TEMPO = "-- Seleccionar Tempo --"

    def __init__(self, page, app, route, title, header_colors):
        self.page = page
        self.app = app
        self.route = route
        self.title = title
        self.header_colors = header_colors
        self.selected_characters = []  # ✅ Lista de caracteres seleccionados

        # Crear campos del formulario
        self.title_field = self._create_title_field()
        self.key_dropdown = self._create_key_dropdown()
        self.character_chips_row = ft.Row([], wrap=True, spacing=8)  # ✅ Chips de caracteres
        self.character_dropdown = self._create_character_dropdown()
        self.tempo_dropdown = self._create_tempo_dropdown()

    def _create_title_field(self):
        colors = get_theme_colors(self.page)
        return ft.TextField(
            label="Nombre de la canción",
            border_color=colors["border_color"],
            focused_border_color=colors["border_focused"],
            bgcolor=colors["bg_secondary"],
            color=colors["text_primary"],
            text_size=14,
            border_radius=12,
        )

    def _create_key_dropdown(self):
        colors = get_theme_colors(self.page)
        # ✅ Agregar opción placeholder al inicio
        options = [ft.dropdown.Option(self.PLACEHOLDER_TONO)]
        options.extend([ft.dropdown.Option(key) for key in MUSICAL_KEYS])
        
        return ft.Dropdown(
            label="Tono",
            options=options,
            value=self.PLACEHOLDER_TONO,  # ✅ Valor inicial
            border_color=colors["border_color"],
            focused_border_color=colors["border_focused"],
            bgcolor=colors["bg_secondary"],
            color=colors["text_primary"],
            text_size=14,
            border_radius=12,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
            expand=True,
        )

    def _clear_key_dropdown(self, e):
        """Limpia el dropdown de tono"""
        self.key_dropdown.value = self.PLACEHOLDER_TONO
        self.key_dropdown.update()
        self.page.update()

    def _create_character_dropdown(self):
        """Dropdown para agregar caracteres (se puede seleccionar múltiples veces)"""
        colors = get_theme_colors(self.page)
        # ✅ Agregar opción placeholder al inicio
        options = [ft.dropdown.Option(self.PLACEHOLDER_CARACTER)]
        options.extend([ft.dropdown.Option(char) for char in self.app.get_characters()])
        
        return ft.Dropdown(
            label="Agregar carácter",
            options=options,
            value=self.PLACEHOLDER_CARACTER,  # ✅ Valor inicial
            border_color=colors["border_color"],
            focused_border_color=colors["border_focused"],
            bgcolor=colors["bg_secondary"],
            color=colors["text_primary"],
            text_size=14,
            border_radius=12,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
            expand=True,
            on_change=self._on_character_selected,
        )

    def _on_character_selected(self, e):
        """Cuando se selecciona un carácter, se agrega a la lista"""
        selected = e.control.value
        # ✅ Ignorar si es el placeholder
        if selected and selected != self.PLACEHOLDER_CARACTER and selected not in self.selected_characters:
            self.selected_characters.append(selected)
            self._update_character_chips()
        # ✅ CRÍTICO: Resetear de forma inmediata y forzada
        e.control.value = self.PLACEHOLDER_CARACTER
        sleep(0.1)
        e.control.update()

    def _remove_character(self, character):
        """Elimina un carácter de la lista seleccionada"""
        if character in self.selected_characters:
            self.selected_characters.remove(character)
            self._update_character_chips()
        
        # ✅ CRÍTICO: Reset inmediato del dropdown
        self.character_dropdown.value = self.PLACEHOLDER_CARACTER
        
        # ✅ Forzar múltiples actualizaciones para asegurar sincronización
        try:
            self.character_dropdown.update()
            self.page.update()
        except Exception:
            pass

    def _clear_all_characters(self, e):
        """Limpia todos los caracteres seleccionados"""
        self.selected_characters.clear()
        
        # ✅ Reset ANTES de actualizar chips
        self.character_dropdown.value = self.PLACEHOLDER_CARACTER
        
        self._update_character_chips()
        
        # ✅ Doble actualización para forzar sincronización
        try:
            self.character_dropdown.update()
            self.page.update()
        except Exception:
            pass

    def _update_character_chips(self):
        """Actualiza los chips visuales de caracteres seleccionados"""
        colors = get_theme_colors(self.page)
        self.character_chips_row.controls.clear()
        
        for char in self.selected_characters:
            chip = ft.Container(
                content=ft.Row([
                    ft.Text(char, size=13, color=colors["text_primary"], weight=ft.FontWeight.W_500),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        icon_size=16,
                        icon_color="#ff7675",
                        on_click=lambda e, c=char: self._remove_character(c),
                        tooltip="Eliminar"
                    ),
                ], spacing=4, tight=True),
                bgcolor=colors["bg_tertiary"],
                border_radius=20,
                padding=ft.padding.only(left=12, right=4, top=4, bottom=4),
                border=ft.border.all(1, colors["border_color"]),
            )
            self.character_chips_row.controls.append(chip)
        
        # ✅ Solo actualizar si el control ya está en la página
        try:
            self.character_chips_row.update()
        except (AssertionError, AttributeError):
            # El control aún no está en la página, se actualizará cuando se agregue
            pass

    def _create_tempo_dropdown(self):
        colors = get_theme_colors(self.page)
        # ✅ Agregar opción placeholder al inicio
        options = [
            ft.dropdown.Option(self.PLACEHOLDER_TEMPO),
            ft.dropdown.Option("Lenta"),
            ft.dropdown.Option("Rápida"),
        ]
        
        return ft.Dropdown(
            label="Tempo",
            options=options,
            value=self.PLACEHOLDER_TEMPO,  # ✅ Valor inicial
            border_color=colors["border_color"],
            focused_border_color=colors["border_focused"],
            bgcolor=colors["bg_secondary"],
            color=colors["text_primary"],
            text_size=14,
            border_radius=12,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
            expand=True,
        )

    def _clear_tempo_dropdown(self, e):
        """Limpia el dropdown de tempo"""
        self.tempo_dropdown.value = self.PLACEHOLDER_TEMPO
        self.tempo_dropdown.update()
        self.page.update()

    def refresh_theme(self):
        """Actualiza los estilos según el tema"""
        colors = get_theme_colors(self.page)

        for control in [self.title_field, self.key_dropdown, self.character_dropdown, self.tempo_dropdown]:
            control.border_color = colors["border_color"]
            control.bgcolor = colors["bg_secondary"]
            control.color = colors["text_primary"]
        
        self._update_character_chips()  # Refrescar chips

    def clear_form(self):
        """Limpia todos los campos del formulario"""
        self.title_field.value = ""
        self.key_dropdown.value = self.PLACEHOLDER_TONO
        self.character_dropdown.value = self.PLACEHOLDER_CARACTER
        self.tempo_dropdown.value = self.PLACEHOLDER_TEMPO
        self.selected_characters = []
        self._update_character_chips()
        
        # ✅ NUEVO: Forzar actualización de todos los controles
        try:
            self.title_field.update()
            self.key_dropdown.update()
            self.character_dropdown.update()
            self.tempo_dropdown.update()
        except Exception:
            pass

    def load_song_data(self, song):
        """Carga los datos de una canción en el formulario"""
        # ✅ CRÍTICO: Trabajar con una copia para evitar mutación
        self.title_field.value = str(song["title"])  # Forzar string
        
        # ✅ Cargar tono (si está vacío, usar placeholder)
        key_value = song.get("key", "")
        self.key_dropdown.value = key_value if key_value else self.PLACEHOLDER_TONO
        
        # ✅ Cargar tempo (si está vacío, usar placeholder)
        tempo_value = song.get("tempo", "")
        self.tempo_dropdown.value = tempo_value if tempo_value else self.PLACEHOLDER_TEMPO
        
        # ✅ Cargar múltiples caracteres
        characters = song.get("character", "")
        if isinstance(characters, list):
            # Crear nueva lista, no referencia
            self.selected_characters = [str(c) for c in characters]
        elif characters:
            self.selected_characters = [c.strip() for c in str(characters).split(",") if c.strip()]
        else:
            self.selected_characters = []
        
        self._update_character_chips()

    def save_song_handler(self, main_view):
        """Guarda la canción (agregar o editar)"""
        if not self.title_field.value or not self.title_field.value.strip():
            show_snackbar(self.page, "El nombre de la canción es obligatorio", "#ff7675")
            return

        editing_song = self.page.session.get("editing_song")
        
        # ✅ Validar y obtener valores reales (no placeholders)
        key_value = self.key_dropdown.value
        if key_value == self.PLACEHOLDER_TONO:
            key_value = ""
        
        tempo_value = self.tempo_dropdown.value
        if tempo_value == self.PLACEHOLDER_TEMPO:
            tempo_value = ""
        
        # ✅ Convertir lista de caracteres a string separado por comas
        characters_str = ",".join(self.selected_characters) if self.selected_characters else ""
        
        # ✅ VALIDACIÓN: Al menos uno de los tres campos debe tener un valor real
        if not key_value and not characters_str and not tempo_value:
            show_snackbar(
                self.page, 
                "Debes seleccionar al menos un valor en Tono, Carácter o Tempo", 
                "#ff7675"
            )
            return

        if editing_song:
            self.app.update_song(
                editing_song["id"],
                title=self.title_field.value.strip(),
                key=key_value,
                character=characters_str,
                tempo=tempo_value
            )
            self.page.session.remove("editing_song")
            show_snackbar(self.page, "Canción actualizada exitosamente", "#00b894")
        else:
            self.app.add_song(
                self.title_field.value.strip(),
                key=key_value,
                character=characters_str,
                tempo=tempo_value
            )
            show_snackbar(self.page, "Canción agregada exitosamente", "#00b894")

        self.clear_form()
        main_view.search_handler(None)
        self.page.go("/")

    def refresh_character_options(self):
        """Actualiza las opciones de caracteres en el dropdown"""
        # ✅ Mantener el placeholder al inicio
        options = [ft.dropdown.Option(self.PLACEHOLDER_CARACTER)]
        options.extend([ft.dropdown.Option(char) for char in self.app.get_characters()])
        self.character_dropdown.options = options

    def build(self, main_view, extra_buttons=None):
        """Construye la vista del formulario"""
        colors = get_theme_colors(self.page)

        self.refresh_theme()

        right_buttons = []

        if extra_buttons:
            right_buttons.extend(extra_buttons)

        header = create_header(
            self.page,
            self.title,
            self.header_colors,
            left_button=ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color="#ffffff",
                icon_size=26,
                on_click=lambda e: self.page.go("/"),
                tooltip="Volver"
            ),
            right_buttons=right_buttons
        )
        editing_song = self.page.session.get("editing_song")

        save_button = ft.ElevatedButton(
            text="Guardar cambios" if editing_song else "Añadir canción",
            icon=ft.Icons.SAVE if editing_song else ft.Icons.ADD,
            on_click=lambda e: self.save_song_handler(main_view),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
                padding=ft.padding.symmetric(horizontal=20, vertical=20),
            ),
        )

        # ✅ Botón de limpieza para Tono
        clear_key_button = ft.IconButton(
            icon=ft.Icons.CLEAR,
            icon_size=20,
            icon_color="#ff7675",
            tooltip="Limpiar tono",
            on_click=self._clear_key_dropdown,
        )

        # ✅ Botón de limpieza para Caracteres
        clear_characters_button = ft.IconButton(
            icon=ft.Icons.CLEAR,
            icon_size=20,
            icon_color="#ff7675",
            tooltip="Limpiar todos los caracteres",
            on_click=self._clear_all_characters,
        )

        # ✅ Botón de limpieza para Tempo
        clear_tempo_button = ft.IconButton(
            icon=ft.Icons.CLEAR,
            icon_size=20,
            icon_color="#ff7675",
            tooltip="Limpiar tempo",
            on_click=self._clear_tempo_dropdown,
        )

        form = ft.Container(
            content=ft.Column([
                ft.Container(content=self.title_field, expand=True),
                ft.Container(height=8),
                # ✅ TONO CON BOTÓN DE LIMPIEZA
                ft.Row([
                    ft.Container(content=self.key_dropdown, expand=True),
                    clear_key_button,
                ], spacing=8),
                ft.Container(height=8),
                # ✅ SELECTOR DE CARACTERES MÚLTIPLES CON BOTÓN DE LIMPIEZA
                ft.Column([
                    ft.Row([
                        ft.Container(content=self.character_dropdown, expand=True),
                        clear_characters_button,
                    ], spacing=8),
                    ft.Container(height=8),
                    self.character_chips_row,  # Chips de caracteres seleccionados
                ], spacing=0),
                ft.Container(height=8),
                # ✅ TEMPO CON BOTÓN DE LIMPIEZA
                ft.Row([
                    ft.Container(content=self.tempo_dropdown, expand=True),
                    clear_tempo_button,
                ], spacing=8),
                ft.Container(height=22),
                ft.Row(
                    [
                        ft.Container(
                            content=save_button,
                            width=240,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ], spacing=8),
            padding=16,
        )

        return ft.View(
            self.route,
            [header, form],
            bgcolor=colors["bg_primary"],
            padding=0,
        )