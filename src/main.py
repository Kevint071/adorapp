import flet as ft
from models import SongApp
from views import CharacterSettingsView, SettingsView, SongFormView, EditView, MainView


def main(page: ft.Page):
    """Función principal de la aplicación"""
    # Configuración de la página
    page.title = "Gestor de Canciones"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0a0e27"
    page.padding = 0

    # Inicializar modelo de datos
    app = SongApp()

    # Inicializar vistas
    main_view = MainView(page, app)
    page.session.set("main_view", main_view)

    add_view = SongFormView(page, app, "/add", "Agregar Canción", ["#00b894", "#55efc4"])
    edit_view = EditView(page, app)
    settings_view = SettingsView(page, app)
    character_settings_view = CharacterSettingsView(page, app)

    def apply_theme():
        mode = page.session.get("theme_mode") or "dark"
        page.theme_mode = ft.ThemeMode.LIGHT if mode == "light" else ft.ThemeMode.DARK
        page.bgcolor = "#f5f6fa" if mode == "light" else "#0a0e27"

    def route_change(e):
        """Maneja los cambios de ruta"""
        apply_theme()
        page.views.clear()

        if page.route == "/":
            page.views.append(main_view.build())

        elif page.route == "/add":
            add_view.clear_form()
            add_view.refresh_character_options()
            page.views.append(add_view.build(main_view))

        elif page.route == "/edit":
            editing_song = page.session.get("editing_song")
            if editing_song:
                edit_view.load_song_data(editing_song)
                edit_view.refresh_character_options()
            page.views.append(edit_view.build(main_view))

        elif page.route == "/settings":
            page.views.append(settings_view.build(main_view))
        elif page.route == "/settings/characters":
            character_settings_view.refresh_characters_list()
            page.views.append(character_settings_view.build(main_view))

        page.update()

    # Asignar manejadores de eventos
    page.on_route_change = route_change
    # ✅ REMOVIDO: page.on_view_pop ya que no lo usas

    # Iniciar en vista principal
    page.go("/")
    main_view.search_handler(None)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
