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
        ctx = self.ctx.get_context()
        if not ctx:
            print("No hay contexto activo.")
            logging.warning("Commit fallido: sin contexto válido.")
            return

        usuario_actual = ctx["usuario_actual"]
        usuario_proyecto = ctx["usuario_proyecto"]
        proyecto = ctx["proyecto"]
        rama = ctx["rama"]
        base_path = ctx["path"]

        temp_path = os.path.join(base_path, "temporal")
        perm_path = os.path.join(base_path, "permanente")
        version_path = os.path.join(base_path, "versiones")

        if not os.path.exists(temp_path):
            print(f"No se encontró la carpeta temporal en: {temp_path}")
            logging.error(f"Commit fallido: carpeta temporal no existe en {temp_path}")
            return

        if os.path.exists(perm_path):
            shutil.rmtree(perm_path)
        os.makedirs(version_path, exist_ok=True)

        shutil.copytree(temp_path, perm_path)

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        version_dir = os.path.join(version_path, f"v_{timestamp}")
        shutil.copytree(perm_path, version_dir)

        logging.info(
            f"Commit realizado por {usuario_actual} en {usuario_proyecto}/{proyecto}/{rama}. Version: v_{timestamp}")
        print(f"Commit exitoso. Versión guardada: v_{timestamp}")

    def update(self):
        ctx = self.ctx.get_context()
        if not ctx:
            print("No hay contexto activo.")
            logging.warning("Update fallido: sin contexto válido.")
            return

        usuario_actual = ctx["usuario_actual"]
        usuario_proyecto = ctx["usuario_proyecto"]
        proyecto = ctx["proyecto"]
        rama = ctx["rama"]
        base_path = ctx["path"]

        temp_path = os.path.join(base_path, "temporal")
        perm_path = os.path.join(self.base_repo, usuario_proyecto, proyecto, "branches", rama, "permanente")

        if not os.path.exists(perm_path):
            print(f"No se encontró la carpeta permanente en: {perm_path}")
            logging.error(f"Update fallido: carpeta permanente no existe en {perm_path}")
            return

        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)

        shutil.copytree(perm_path, temp_path)

        logging.info(f"Update realizado por {usuario_actual} desde {usuario_proyecto}/{proyecto}/{rama}.")
        print("Update exitoso: contenido copiado desde permanente a temporal.")

    def list_versions(self):
        ctx = self.ctx.get_context()
        if not ctx:
            print("No hay contexto activo.")
            return []

        usuario_proyecto = ctx["usuario_proyecto"]
        proyecto = ctx["proyecto"]
        rama = ctx["rama"]

        version_path = os.path.join(self.base_repo, usuario_proyecto, proyecto, "branches", rama, "versiones")

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
        ctx = self.ctx.get_context()
        if not ctx:
            print("No hay contexto activo.")
            logging.warning("Recuperación fallida: sin contexto válido.")
            return

        usuario_actual = ctx["usuario_actual"]
        usuario_proyecto = ctx["usuario_proyecto"]
        proyecto = ctx["proyecto"]
        rama = ctx["rama"]
        base_path = ctx["path"]

        version_dir = os.path.join(self.base_repo, usuario_proyecto, proyecto, "branches", rama, "versiones", version)
        temp_path = os.path.join(base_path, "temporal")

        if not os.path.exists(version_dir):
            print("La versión seleccionada no existe.")
            logging.error(f"Recuperación fallida: versión {version} no encontrada.")
            return

        if is_file:
            src_file = os.path.join(version_dir, path_relativa)
            dst_file = os.path.join(temp_path, path_relativa)

            if not os.path.exists(src_file):
                print("El archivo no existe en esa versión.")
                logging.error(f"Recuperación fallida: archivo {src_file} no existe.")
                return

            if os.path.exists(dst_file):
                confirm = input(f"El archivo ya existe en temporal. ¿Sobrescribir '{path_relativa}'? (s/n): ").lower()
                if confirm != 's':
                    print("Recuperación cancelada.")
                    return

            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copy2(src_file, dst_file)
            print("Archivo recuperado con éxito.")
            logging.info(f"Archivo {path_relativa} recuperado de versión {version} por {usuario_actual}.")

        else:
            if os.path.exists(temp_path):
                confirm = input(
                    "La carpeta temporal será reemplazada por la versión seleccionada. ¿Continuar? (s/n): ").lower()
                if confirm != 's':
                    print("Recuperación cancelada.")
                    return
                shutil.rmtree(temp_path)

            shutil.copytree(version_dir, temp_path)
            print("Carpeta completa recuperada con éxito.")
            logging.info(f"Carpeta recuperada de versión {version} por {usuario_actual}.")

    def list_files_in_version(self, version):
        ctx = self.ctx.get_context()
        if not ctx:
            print("No hay contexto activo.")
            return []

        usuario_proyecto = ctx["usuario_proyecto"]
        proyecto = ctx["proyecto"]
        rama = ctx["rama"]

        version_dir = os.path.join(self.base_repo, usuario_proyecto, proyecto, "branches", rama, "versiones", version)
        if not os.path.exists(version_dir):
            print("La versión no existe.")
            return []

        archivos = []
        for root, _, files in os.walk(version_dir):
            for f in files:
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, version_dir)
                archivos.append(rel_path)
        return archivos
