import json
import os
import shutil

# Constantes
MUSICAL_KEYS = [
    "Do", "Do Menor",
    "Do#", "Do# Menor",
    "Re", "Re Menor",
    "Re#", "Re# Menor",
    "Mi", "Mi Menor",
    "Fa", "Fa Menor",
    "Fa#", "Fa# Menor",
    "Sol", "Sol Menor",
    "Sol#", "Sol# Menor",
    "La", "La Menor",
    "La#", "La# Menor",
    "Si", "Si Menor"
]
DEFAULT_CHARACTERS = ["Misionero", "Oración", "Evangelístico", "Alabanza", "Adoración"]


class SongApp:
    """Gestiona la lógica de negocio de canciones y caracteres"""
    
    def __init__(self):
        # ✅ Obtener el directorio de datos de la aplicación (escribible)
        self.data_dir = self._get_data_directory()
        self.data_file = os.path.join(self.data_dir, "user_data.json")
        
        # ✅ Archivo inicial (solo lectura, en assets)
        self.initial_data_file = "./storage/data/user_data.json"
        
        # ✅ Asegurar que existe el archivo de datos
        self._ensure_data_file()
        
        self.user_data = self.load_user_data()

    def _get_data_directory(self):
        """
        Obtiene el directorio de datos apropiado según la plataforma.
        En Android: /data/data/com.kevintorrecilla.grupos_canciones/files/
        En escritorio: ./storage/data/
        """
        try:
            # Intentar obtener el directorio de la app en Android/iOS
            # Flet proporciona una variable de entorno para el directorio de datos
            if os.getenv("FLET_APP_STORAGE_DATA"):
                data_dir = os.getenv("FLET_APP_STORAGE_DATA", "./storage/data")
                print(data_dir)
            else:
                data_dir = "./storage/data"
            
            # Crear directorio si no existe
            os.makedirs(data_dir, exist_ok=True)
            return data_dir
            
        except Exception as e:
            print(f"Error obteniendo directorio de datos: {e}")
            # Fallback a directorio local
            data_dir = "./storage/data"
            os.makedirs(data_dir, exist_ok=True)
            return data_dir

    def _ensure_data_file(self):
        """
        Asegura que exista el archivo de datos en el directorio escribible.
        Si no existe, copia el archivo inicial desde assets.
        """
        if not os.path.exists(self.data_file):
            # ✅ Si existe el archivo inicial, copiarlo
            if os.path.exists(self.initial_data_file):
                try:
                    # Crear directorio si no existe
                    os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
                    # Copiar archivo inicial
                    shutil.copy2(self.initial_data_file, self.data_file)
                    print(f"✅ Archivo inicial copiado a: {self.data_file}")
                except Exception as e:
                    print(f"Error copiando archivo inicial: {e}")
                    self._create_default_data_file()
            else:
                # ✅ Si no existe archivo inicial, crear uno por defecto
                self._create_default_data_file()

    def _create_default_data_file(self):
        """Crea un archivo de datos por defecto"""
        default_data = {
            "songs": [],
            "characters": DEFAULT_CHARACTERS.copy()
        }
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(default_data, f, ensure_ascii=False, indent=2)
            print(f"✅ Archivo de datos creado: {self.data_file}")
        except Exception as e:
            print(f"Error creando archivo de datos: {e}")

    def load_user_data(self):
        """Carga datos del usuario desde el archivo JSON"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "characters" not in data:
                        data["characters"] = DEFAULT_CHARACTERS.copy()
                    if "songs" not in data:
                        data["songs"] = []
                    return data
        except Exception as e:
            print(f"Error cargando datos: {e}")
        
        # Fallback a datos por defecto
        return {"songs": [], "characters": DEFAULT_CHARACTERS.copy()}

    def save_user_data(self):
        """Guarda datos del usuario en el archivo JSON"""
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.user_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error guardando datos: {e}")

    # ===== GESTIÓN DE CARACTERES =====
    
    def get_characters(self):
        """Obtiene la lista de caracteres disponibles"""
        self.user_data = self.load_user_data()
        return self.user_data.get("characters", DEFAULT_CHARACTERS.copy())

    def add_character(self, character):
        """Agrega un nuevo carácter"""
        if character and character not in self.user_data["characters"]:
            self.user_data["characters"].append(character)
            self.save_user_data()
            self.user_data = self.load_user_data()
            return True
        return False

    def remove_character(self, character):
        """Elimina un carácter"""
        if character in self.user_data["characters"]:
            self.user_data["characters"].remove(character)
            self.save_user_data()
            self.user_data = self.load_user_data()
            return True
        return False

    # ===== GESTIÓN DE CANCIONES =====
    
    def get_all_songs(self):
        """Obtiene todas las canciones"""
        return self.user_data.get("songs", [])

    def add_song(self, title, key, character, tempo):
        """Agrega una nueva canción"""
        new_id = max([s["id"] for s in self.user_data["songs"]], default=0) + 1
        new_song = {
            "id": new_id,
            "title": title,
            "key": key,
            "character": character,  # String con comas: "Adoración,Alabanza"
            "tempo": tempo
        }
        self.user_data["songs"].append(new_song)
        self.save_user_data()
        return new_song

    def update_song(self, song_id, title=None, key=None, character=None, tempo=None):
        """Actualiza una canción existente"""
        for song in self.user_data["songs"]:
            if song["id"] == song_id:
                if title is not None:
                    song["title"] = title
                if key is not None:
                    song["key"] = key
                if character is not None:
                    song["character"] = character
                if tempo is not None:
                    song["tempo"] = tempo
                self.save_user_data()
                return True
        return False

    def delete_song(self, song_id):
        """Elimina una canción"""
        self.user_data["songs"] = [s for s in self.user_data["songs"] if s["id"] != song_id]
        self.save_user_data()

    def search_songs(self, query="", key="", character="", tempo=""):
        """
        Busca canciones con filtros.
        ✅ Soporta múltiples caracteres por canción.
        """
        songs = self.get_all_songs()

        # Filtro de texto (búsqueda por título)
        if query:
            query_lower = query.lower()
            songs = [s for s in songs if query_lower in s["title"].lower()]

        # Filtro de tono
        if key:
            songs = [s for s in songs if s.get("key") == key]

        # ✅ Filtro de carácter (verifica si el carácter está en la lista)
        if character:
            filtered_songs = []
            for song in songs:
                song_characters = song.get("character", "")
                # Convertir string separado por comas en lista
                char_list = [c.strip() for c in song_characters.split(",") if c.strip()]
                # Si el carácter buscado está en la lista, incluir la canción
                if character in char_list:
                    filtered_songs.append(song)
            songs = filtered_songs

        # Filtro de tempo
        if tempo:
            songs = [s for s in songs if s.get("tempo") == tempo]

        return songs