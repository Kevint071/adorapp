"""
Vista de edición de canciones
"""
import flet as ft
from components import show_confirmation_dialog, show_snackbar
from .song_form_view import SongFormView


class EditView(SongFormView):
    """Vista de edición de canciones"""
    
    def __init__(self, page, app):
        super().__init__(page, app, "/edit", "Editar Canción", ["#74b9ff", "#a29bfe"])
    
    def delete_from_edit(self, main_view):
        editing_song = self.page.session.get("editing_song")
        if not editing_song:
            return

        def on_confirm():
            try:
                song_id = editing_song["id"]
                
                # ✅ Eliminar la canción
                self.app.delete_song(song_id)
                
                # ✅ Limpiar sesión
                self.page.session.remove("editing_song")
                
                # ✅ Limpiar formulario
                self.clear_form()
                
                # ✅ CRÍTICO: Navegar de forma segura sin limpiar views
                self.page.go("/")
                
                # ✅ Pequeño delay para asegurar que la navegación se complete
                import time
                time.sleep(0.05)
                
                # ✅ Refrescar búsqueda después de navegar
                if main_view:
                    main_view.search_handler(None)
                
                # ✅ Mostrar confirmación
                show_snackbar(self.page, "Canción eliminada exitosamente", "#ff7675")
                
                self.page.update()

            except Exception as ex:
                print("ERROR al eliminar canción:", ex)
                show_snackbar(self.page, "Error al eliminar la canción", "#ff7675")

        show_confirmation_dialog(
            self.page,
            "Confirmar eliminación",
            "¿Estás seguro de que deseas eliminar esta canción?",
            on_confirm
        )
    
    def build(self, main_view, extra_buttons=None):
        """Construye la vista de edición con botón de eliminar"""
        # ✅ Cargar datos de la canción al construir la vista
        editing_song = self.page.session.get("editing_song")
        if editing_song:
            # ✅ CRÍTICO: Crear una COPIA del diccionario para evitar mutación
            song_copy = {
                "id": editing_song["id"],
                "title": editing_song["title"],
                "key": editing_song.get("key", ""),
                "character": editing_song.get("character", ""),
                "tempo": editing_song.get("tempo", "")
            }
            self.load_song_data(song_copy)
        
        is_light = self.page.session.get("theme_mode") == "light"
        
        delete_button = ft.Container(
            content=ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINE,
                icon_color="#ffffff" if is_light else "#0a0e27",
                icon_size=26,
                on_click=lambda e: self.delete_from_edit(main_view),
                tooltip="Eliminar"
            ),
            bgcolor="#ff7675",
            border_radius=10,
            padding=2,
        )
        return super().build(main_view, extra_buttons=[delete_button])