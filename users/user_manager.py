import os
import json
import logging
import shutil

DATA_FILE = "data/users.json"
REPO_ROOT = "repo_root"

class UserManager:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        os.makedirs(REPO_ROOT, exist_ok=True)
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump({}, f)
        logging.info("Inicializado UserManager con estructura de carpetas.")

    def load_users(self):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logging.error(f"Error cargando usuarios: {e}")
            return {}

    def save_users(self, users):
        with open(DATA_FILE, "w") as f:
            json.dump(users, f, indent=2)
        logging.info("Usuarios guardados exitosamente.")

    def create_user(self, username):
        users = self.load_users()
        if username in users:
            print(f"El usuario '{username}' ya existe.")
            return

        users[username] = {
            "permisos": {}
        }

        base_path = os.path.join(REPO_ROOT, username)
        os.makedirs(os.path.join(base_path, "permanente"), exist_ok=True)
        os.makedirs(os.path.join(base_path, "temporal"), exist_ok=True)
        os.makedirs(os.path.join(base_path, "versiones"), exist_ok=True)

        self.save_users(users)
        print(f"Usuario '{username}' creado con éxito.")

    def list_users(self):
        users = self.load_users()
        print("Usuarios registrados:")
        for u in users:
            print(f"- {u}")

    def assign_permission(self, from_user, to_user, permiso):
        users = self.load_users()
        if from_user not in users or to_user not in users:
            print("Uno o ambos usuarios no existen.")
            return
        if from_user == to_user:
            print("No puedes asignarte permisos a ti mismo.")
            return
        if permiso not in ["read", "write"]:
            print("Permiso inválido. Use 'read' o 'write'.")
            return

        users[from_user]["permisos"][to_user] = permiso
        self.save_users(users)

        # Crear carpeta temporal compartida
        temp_folder = os.path.join(REPO_ROOT, from_user, f"temp_{to_user}")
        os.makedirs(temp_folder, exist_ok=True)

        print(f"Permiso '{permiso}' otorgado de {from_user} a {to_user}.")

    def remove_permission(self, from_user, to_user, permiso):
        users = self.load_users()

        # Validaciones básicas
        if from_user not in users:
            print(f"El usuario '{from_user}' no existe.")
            return
        if to_user not in users:
            print(f"El usuario '{to_user}' no existe.")
            return
        if permiso not in ("read", "write"):
            print("Permiso inválido. Use 'read' o 'write'.")
            return

        current_perm = users[from_user]["permisos"].get(to_user)
        if not current_perm:
            print(f"{to_user} no tiene permisos sobre el repositorio de {from_user}.")
            return

        # Si tiene el permiso que se quiere quitar
        if current_perm == permiso:
            del users[from_user]["permisos"][to_user]
            self.save_users(users)
            print(f"Permiso '{permiso}' eliminado correctamente de {to_user} sobre {from_user}.")

            # Eliminar carpeta temporal si ya no tiene permisos
            temp_path = os.path.join("repo_root", from_user, f"temp_{to_user}")
            if os.path.exists(temp_path):
                try:
                    shutil.rmtree(temp_path)
                    print(f"Carpeta temporal '{temp_path}' eliminada.")
                except Exception as e:
                    print(f"No se pudo eliminar la carpeta: {e}")
        else:
            print(f"{to_user} tiene permiso '{current_perm}', no coincide con '{permiso}' indicado.")

    def has_write_permission(self, current_user, target_user):
        users = self.load_users()
        if current_user == target_user:
            return True
        return users.get(target_user, {}).get("permisos", {}).get(current_user) == "write"

    def has_read_permission(self, current_user, target_user):
        users = self.load_users()
        if current_user == target_user:
            return True
        return users.get(target_user, {}).get("permisos", {}).get(current_user) in ("read", "write")

    def has_any_permission(self, current_user, target_user):
        users = self.load_users()
        if current_user == target_user:
            return True
        return current_user in users.get(target_user, {}).get("permisos", {})

