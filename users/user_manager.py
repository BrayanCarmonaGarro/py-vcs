import os
import json
import logging

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
