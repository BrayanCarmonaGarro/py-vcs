import os
import json
import re
from core.context_manager import ContextManager

PROJECTS_FILE = "data/projects.json"
REPO_ROOT = "repo_root"

class ProjectManager:
    def __init__(self, user_manager=None):
        self.user_manager = user_manager
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(PROJECTS_FILE):
            with open(PROJECTS_FILE, "w") as f:
                json.dump({}, f)

    def load_projects(self):
        with open(PROJECTS_FILE, "r") as f:
            return json.load(f)

    def save_projects(self, projects):
        with open(PROJECTS_FILE, "w") as f:
            json.dump(projects, f, indent=2)

    def create_project(self, username, project_name):
        if self.user_manager:
            users = self.user_manager.load_users()
            if username not in users:
                print(f"El usuario '{username}' no existe. No se puede crear el proyecto.")
                return

        projects = self.load_projects()
        if username not in projects:
            projects[username] = []
        if project_name in projects[username]:
            print(f"El proyecto '{project_name}' ya existe para el usuario {username}.")
            return

        base_path = f"{REPO_ROOT}/{username}/{project_name}/branches/main"
        os.makedirs(f"{base_path}/temporal", exist_ok=True)
        os.makedirs(f"{base_path}/permanente", exist_ok=True)
        projects[username].append(project_name)
        self.save_projects(projects)
        print(f"Proyecto '{project_name}' creado con éxito para el usuario {username}.")

    def list_projects(self, username, silent=False):
        projects = self.load_projects()
        if username not in projects:
            if not silent:
                print(f"No hay proyectos para el usuario {username}.")
            return []
        if not silent:
            print(f"Proyectos de {username}:")
            for p in projects[username]:
                print(f"- {p}")
        return projects[username]

    def list_branches(self, username, project_name):
        branches_dir = f"{REPO_ROOT}/{username}/{project_name}/branches"
        if not os.path.exists(branches_dir):
            print(f"No se encontro la ruta del proyecto '{project_name}' para el usuario '{username}'.")
            return []
        return [name for name in os.listdir(branches_dir) if os.path.isdir(os.path.join(branches_dir, name))]

    def crear_rama(self):
        ctx_manager = ContextManager()
        ctx = ctx_manager.get_context()

        if not ctx:
            print("Debe seleccionar primero un contexto válido (usuario actual y proyecto).")
            return

        usuario_actual = ctx["usuario_actual"]
        usuario_proyecto = ctx["usuario_proyecto"]
        proyecto = ctx["proyecto"]

        if not usuario_actual or not usuario_proyecto or not proyecto:
            print("Contexto incompleto.")
            return

        projects = self.load_projects()
        if usuario_proyecto not in projects or proyecto not in projects[usuario_proyecto]:
            print(f"El proyecto '{proyecto}' no existe para el usuario '{usuario_proyecto}'.")
            return

        # Validación de permisos
        if usuario_actual != usuario_proyecto:
            users = self.user_manager.load_users()
            permisos = users[usuario_proyecto].get("permisos", {})
            permisos_lista = permisos.get(usuario_actual, [])
            if "write" not in permisos_lista:
                print(
                    f"El usuario '{usuario_actual}' no tiene permisos de escritura en el proyecto '{proyecto}' de '{usuario_proyecto}'.")
                return

        branch_name = input("Ingrese el nombre de la nueva rama: ").strip()

        if not branch_name:
            print("El nombre de la rama no puede estar vacío.")
            return
        if "/" in branch_name or "\\" in branch_name:
            print("El nombre de la rama no puede contener '/' ni '\\'.")
            return
        if not re.match(r'^[\w\-]+$', branch_name):
            print("El nombre de la rama solo puede contener letras, números, guiones y guiones bajos.")
            return

        # Ruta según contexto
        if usuario_actual == usuario_proyecto:
            branch_path = os.path.join(REPO_ROOT, usuario_actual, proyecto, "branches", branch_name)
        else:
            branch_path = os.path.join(REPO_ROOT, usuario_proyecto, f"shared_{usuario_actual}", proyecto, "branches",
                                       branch_name)

        if os.path.exists(branch_path):
            print(f"La rama '{branch_name}' ya existe.")
            return

        os.makedirs(os.path.join(branch_path, "temporal"), exist_ok=True)
        os.makedirs(os.path.join(branch_path, "permanente"), exist_ok=True)

        print(
            f"Rama '{branch_name}' creada exitosamente en el proyecto '{proyecto}' de '{usuario_proyecto}' por '{usuario_actual}'.")
