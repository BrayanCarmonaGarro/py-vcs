import os

def get_temp_path(base_path, filename):
    return os.path.join(base_path, filename)

def create_file(path, filename):
    ruta = os.path.join(path, filename)
    if os.path.exists(ruta):
        print("El archivo ya existe.")
        return
    with open(ruta, "w", encoding="utf-8") as f:
        pass
    print("Archivo creado correctamente.")


def read_file(base_path, filename):
    path = get_temp_path(base_path, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        print("Archivo no encontrado.")
        return None

def update_file(base_path, filename, content):
    path = get_temp_path(base_path, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Archivo '{filename}' actualizado.")

def delete_file(base_path, filename):
    path = get_temp_path(base_path, filename)
    if os.path.exists(path):
        os.remove(path)
        print(f"Archivo '{filename}' eliminado.")
    else:
        print("Archivo no encontrado.")
def list_files(base_path):
    if not os.path.exists(base_path):
        print("La carpeta de trabajo no existe.")
        return []

    archivos = [f for f in os.listdir(base_path) if os.path.isfile(os.path.join(base_path, f))]
    if not archivos:
        print("No hay archivos en esta carpeta.")
    else:
        print("Archivos disponibles:")
        for i, archivo in enumerate(archivos, 1):
            print(f"{i}. {archivo}")
    return archivos
