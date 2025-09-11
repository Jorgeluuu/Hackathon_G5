import os
from server.services.resource_processor import (
    process_festividades_madrid,
    process_links_interes,
    process_madrid_destino,
    process_transporte_publico_madrid
)

class ResourceLoader:
    def __init__(self, resources_path: str):
        self.resources_path = resources_path
        self.festividades_data = None
        self.links_data = None
        self.madrid_destino_data = None
        self.transporte_data = None

    def _read_file_content(self, filename: str) -> str:
        file_path = os.path.join(self.resources_path, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: El archivo {filename} no se encontró en {self.resources_path}")
            return ""
        except Exception as e:
            print(f"Error al leer el archivo {filename}: {e}")
            return ""

    def load_all_resources(self):
        print("Cargando recursos de Festividades_Madrid.txt...")
        festividades_content = self._read_file_content("Festividades_Madrid.txt")
        if festividades_content:
            self.festividades_data = process_festividades_madrid(festividades_content)
            print("Festividades_Madrid.txt cargado y procesado.")

        print("Cargando recursos de Links_Interes.txt...")
        links_content = self._read_file_content("Links_Interes.txt")
        if links_content:
            self.links_data = process_links_interes(links_content)
            print("Links_Interes.txt cargado y procesado.")

        print("Cargando recursos de MadridDestino_.txt...")
        madrid_destino_content = self._read_file_content("MadridDestino_.txt")
        if madrid_destino_content:
            self.madrid_destino_data = process_madrid_destino(madrid_destino_content)
            print("MadridDestino_.txt cargado y procesado.")

        print("Cargando recursos de Transporte_publico_Madrid.txt...")
        transporte_content = self._read_file_content("Transporte_publico_Madrid.txt")
        if transporte_content:
            self.transporte_data = process_transporte_publico_madrid(transporte_content)
            print("Transporte_publico_Madrid.txt cargado y procesado.")

    def get_festividades_data(self):
        return self.festividades_data

    def get_links_data(self):
        return self.links_data

    def get_madrid_destino_data(self):
        return self.madrid_destino_data

    def get_transporte_data(self):
        return self.transporte_data