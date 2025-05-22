#Contiene la clase UserManager, que se encarga de gestionar los usuarios
#Contiene la clase UserManager, que se encarga de gestionar los usuarios

import os
import json
import logging

# Configurar logging
logging.basicConfig(
    filename='logfile.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

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
            logging.warning(f"Intento de crear usuario existente: {username}")
            print(f"El usuario '{username}' ya existe.")
            return
        users[username] = {
            "permisos": {},
        }
        user_path = os.path.join(REPO_ROOT, username)
        os.makedirs(user_path, exist_ok=True)
        self.save_users(users)
        logging.info(f"Usuario creado: {username}")
        print(f"Usuario '{username}' creado con exito.")

    def list_users(self):
        users = self.load_users()
        print("Usuarios registrados:")
        for u in users:
            print(f"- {u}")
        logging.info("Listado de usuarios mostrado.")

    def assign_permission(self, from_user, to_user, permiso):
        users = self.load_users()

        if from_user not in users or to_user not in users:
            logging.warning(f"Permiso fallido: {from_user} -> {to_user} (usuarios no encontrados)")
            print("Uno o ambos usuarios no existen.")
            return

        if permiso not in ["read", "write"]:
            print("Permiso inválido. Solo se permite 'read' o 'write'.")
            return
        permisos_actuales = users[from_user]["permisos"].get(to_user, [])
        
        if permiso not in permisos_actuales:
            permisos_actuales.append(permiso)
        users[from_user]["permisos"][to_user] = permisos_actuales
        self.save_users(users)

        #Crear carpeta shared_{from_user} en el repo del dueño del proyecto
        if from_user != to_user:
            shared_path = os.path.join("repo_root", to_user, f"shared_{from_user}")
            os.makedirs(shared_path, exist_ok=True)
            print(f"Carpeta compartida creada: {shared_path}")

        logging.info(f"Permiso asignado: {from_user} -> {to_user} : {permiso}")
        print(f"Permiso '{permiso}' otorgado de {from_user} a {to_user}.")

