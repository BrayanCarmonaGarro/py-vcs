import os
import json

PROJECTS_FILE = "data/projects.json"
REPO_ROOT = "repo_root"

class ProjectManager:
    def __init__(self):
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
        projects = self.load_projects()
        if username not in projects:
            projects[username] = []
        if project_name in projects[username]:
            print(f"El proyecto '{project_name}' ya existe para el usuario {username}.")
            return
        
        #Estructura de carpetas para el proyecto con rama "main" por defecto
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
