import os

def get_temp_path(base_path, filename):
    return os.path.join(base_path, filename)

def create_file(base_path, filename, content=""):
    path = get_temp_path(base_path, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Archivo '{filename}' creado.")

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
