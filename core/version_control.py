import os
import shutil
import datetime
import logging
from core.context_manager import ContextManager

class VersionControl:
    def __init__(self):
        self.ctx = ContextManager()
        self.base_repo = "repo_root"

    def commit(self):
        user = self.ctx.get_user()
        project = self.ctx.get_project()
        branch = self.ctx.get_branch()

        if not user or not project or not branch:
            print("No hay contexto activo. Seleccione usuario, proyecto y rama.")
            logging.warning("Intento de commit sin contexto valido.")
            return

        user_path = os.path.join(self.base_repo, user)
        project_path = os.path.join(user_path, project)
        branch_path = os.path.join(project_path, "branches", branch)
        temp_path = os.path.join(branch_path, "temporal")
        perm_path = os.path.join(branch_path, "permanente")
        version_path = os.path.join(branch_path, "versiones")

        if not os.path.exists(temp_path):
            print(f"No se encontro la carpeta temporal en: {temp_path}")
            logging.error(f"Commit fallido: carpeta temporal no existe en {temp_path}")
            return

        os.makedirs(perm_path, exist_ok=True)
        os.makedirs(version_path, exist_ok=True)

        if os.path.exists(perm_path):
            shutil.rmtree(perm_path)
        
        shutil.copytree(temp_path, perm_path)

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        version_dir = os.path.join(version_path, f"v_{timestamp}")
        shutil.copytree(perm_path, version_dir)

        logging.info(f"Commit realizado por {user} en {project}/{branch}. Version: v_{timestamp}")
        print(f"Commit realizado con éxito. Version guardada: v_{timestamp}")

    def update(self):
        user = self.ctx.get_user()
        project = self.ctx.get_project()
        branch = self.ctx.get_branch()

        if not user or not project or not branch:
            print("No hay contexto activo. Seleccione usuario, proyecto y rama.")
            logging.warning("Intento de update sin contexto valido.")
            return
        
        user_path = os.path.join(self.base_repo, user)
        project_path = os.path.join(user_path, project)
        branch_path = os.path.join(project_path, "branches", branch)
        temp_path = os.path.join(branch_path, "temporal")
        perm_path = os.path.join(branch_path, "permanente")

        if not os.path.exists(perm_path):
            print(f"No se encontro la carpeta permanente en: {perm_path}")
            logging.error(f"Update fallido: carpeta permanente no existe en {perm_path}")
            return

        os.makedirs(temp_path, exist_ok=True)

        # Borrar los archivos en la carpeta temporal antes de hacer el update
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)

        # Copiar los archivos desde permanente a temporal
        shutil.copytree(perm_path, temp_path)

        logging.info(f"Update realizado por {user} en {project}/{branch}.")
        print(f"Update realizado con éxito. Los archivos de la carpeta permanente han sido copiados a temporal.")


    def list_versions(self):
        user = self.ctx.get_user()
        project = self.ctx.get_project()
        branch = self.ctx.get_branch()

        if not user or not project or not branch:
            print("No hay contexto activo. Seleccione usuario, proyecto y rama.")
            return []

        version_path = os.path.join(self.base_repo, user, project, "branches", branch, "versiones")

        if not os.path.exists(version_path):
            print("No hay versiones disponibles.")
            return []

        versions = sorted(os.listdir(version_path))
        if not versions:
            print("No hay versiones disponibles.")
            return []

        print("Versiones disponibles:")
        for i, version in enumerate(versions, 1):
            print(f"{i}. {version}")
        return versions

    def recover(self, version, path_relativa="", is_file=True):
        user = self.ctx.get_user()
        project = self.ctx.get_project()
        branch = self.ctx.get_branch()

        if not user or not project or not branch:
            print("No hay contexto activo.")
            logging.warning("Recuperacion fallida: sin contexto valido.")
            return

        base = os.path.join(self.base_repo, user, project, "branches", branch)
        version_dir = os.path.join(base, "versiones", version)
        temp_path = os.path.join(base, "temporal")

        if not os.path.exists(version_dir):
            print("La version seleccionada no existe.")
            logging.error(f"Recuperacion fallida: version {version} no encontrada.")
            return

        if is_file:
            src_file = os.path.join(version_dir, path_relativa)
            dst_file = os.path.join(temp_path, path_relativa)

            if not os.path.exists(src_file):
                print("El archivo no existe en esa version.")
                logging.error(f"Recuperacion fallida: archivo {src_file} no existe.")
                return

            if os.path.exists(dst_file):
                confirm = input(f"El archivo ya existe en temporal. ¿Sobrescribir '{path_relativa}'? (s/n): ").lower()
                if confirm != 's':
                    print("Recuperacion cancelada.")
                    return

            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copy2(src_file, dst_file)
            print("Archivo recuperado con éxito.")
            logging.info(f"Archivo {path_relativa} recuperado de version {version} por {user}.")
        
        else:
            if os.path.exists(temp_path):
                confirm = input("La carpeta temporal sera reemplazada por la version seleccionada. ¿Continuar? (s/n): ").lower()
                if confirm != 's':
                    print("Recuperacion cancelada.")
                    return
                shutil.rmtree(temp_path)

            shutil.copytree(version_dir, temp_path)
            print("Carpeta completa recuperada con éxito.")
            logging.info(f"Carpeta recuperada de version {version} por {user}.")

    def list_files_in_version(self, version):
        user = self.ctx.get_user()
        project = self.ctx.get_project()
        branch = self.ctx.get_branch()

        if not user or not project or not branch:
            print("No hay contexto activo.")
            return []

        version_dir = os.path.join(self.base_repo, user, project, "branches", branch, "versiones", version)
        if not os.path.exists(version_dir):
            print("La version no existe.")
            return []

        archivos = []
        for root, _, files in os.walk(version_dir):
            for f in files:
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, version_dir)
                archivos.append(rel_path)
        return archivos

