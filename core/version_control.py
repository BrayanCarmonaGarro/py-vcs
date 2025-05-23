import os
import shutil
import datetime
import logging
from core.context_manager import ContextManager
from users.user_manager import UserManager

class VersionControl:
    def __init__(self):
        self.ctx = ContextManager()
        self.um = UserManager()
        self.base_repo = "repo_root"

    def commit(self):
        ctx = self.ctx.get_context()
        if not ctx:
            print("No hay contexto activo.")
            return

        usuario_actual = ctx["usuario_actual"]
        usuario_destino = ctx["usuario_destino"]
        temp_path = ctx["path"]

        users = self.um.load_users()
        if usuario_destino not in users:
            print(f"El usuario destino '{usuario_destino}' no existe.")
            return

        permisos = users[usuario_destino].get("permisos", {})
        permiso = permisos.get(usuario_actual)
        if usuario_actual != usuario_destino and permiso != "write":
            print(f"No tienes permisos de escritura sobre el usuario '{usuario_destino}'.")
            return

        perm_path = os.path.join(self.base_repo, usuario_destino, "permanente")
        version_path = os.path.join(self.base_repo, usuario_destino, "versiones")

        if not os.path.exists(temp_path):
            print(f"No se encontró la carpeta temporal de trabajo: {temp_path}")
            return

        os.makedirs(perm_path, exist_ok=True)
        os.makedirs(version_path, exist_ok=True)

        if os.path.exists(perm_path):
            shutil.rmtree(perm_path)
        shutil.copytree(temp_path, perm_path)

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        version_dir = os.path.join(version_path, f"v_{timestamp}")
        shutil.copytree(perm_path, version_dir)

        print(f"Commit realizado sobre {usuario_destino}. Versión guardada: v_{timestamp}")


    def update(self):
        ctx = self.ctx.get_context()
        if not ctx:
            print("No hay contexto activo.")
            return

        current_user = ctx["usuario_actual"]
        target_user = ctx["usuario_destino"]

        if not current_user or not target_user:
            print("Falta información del contexto.")
            return

        # Verificar permisos
        users = self.um.load_users()
        if target_user not in users:
            print(f"El usuario destino '{target_user}' no existe.")
            return

        permisos = users[target_user].get("permisos", {})
        permiso = permisos.get(current_user)
        if current_user != target_user and permiso not in ["read", "write"]:
            print(f"No tienes permisos sobre el usuario '{target_user}'.")
            return

        perm_path = os.path.join(self.base_repo, target_user, "permanente")
        temp_dest = os.path.join(
            self.base_repo,
            target_user,
            f"temp_{current_user}" if current_user != target_user else "temporal"
        )

        if not os.path.exists(perm_path):
            print("No hay carpeta permanente para copiar.")
            return

        if os.path.exists(temp_dest):
            shutil.rmtree(temp_dest)
        shutil.copytree(perm_path, temp_dest)

        print(f"Update realizado desde '{perm_path}' hacia '{temp_dest}'.")

    def list_versions(self):
        ctx = self.ctx.get_context()
        if not ctx:
            print("No hay contexto activo.")
            return []

        usuario_destino = ctx["usuario_destino"]
        version_dir = os.path.join(self.base_repo, usuario_destino, "versiones")

        if not os.path.exists(version_dir):
            print("No hay versiones.")
            return []

        versions = sorted(os.listdir(version_dir))
        if not versions:
            print("No hay versiones registradas.")
            return []

        print("\n--- Versiones disponibles ---")
        for i, v in enumerate(versions, 1):
            print(f"{i}. {v}")
        return versions
    
    def list_files_in_version(self, version_name):
        ctx = self.ctx.get_context()
        if not ctx:
            print("No hay contexto activo.")
            return []

        usuario_destino = ctx["usuario_destino"]
        version_dir = os.path.join(self.base_repo, usuario_destino, "versiones", version_name)

        if not os.path.exists(version_dir):
            print("La versión no existe.")
            return []

        files = []
        for root, _, filenames in os.walk(version_dir):
            for f in filenames:
                rel_path = os.path.relpath(os.path.join(root, f), version_dir)
                files.append(rel_path)

        return files


    def recover(self, version_name, file_name=None, is_file=False):
        ctx = self.ctx.get_context()
        if not ctx:
            print("No hay contexto activo.")
            return

        usuario_destino = ctx["usuario_destino"]
        temp_path = ctx["path"] 

        version_dir = os.path.join(self.base_repo, usuario_destino, "versiones", version_name)
        if not os.path.exists(version_dir):
            print("Versión no encontrada.")
            return

        if is_file and file_name:
            source = os.path.join(version_dir, file_name)
            dest = os.path.join(temp_path, file_name)
            if not os.path.exists(source):
                print("Archivo no existe en la versión.")
                return
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(source, dest)
            print(f"Archivo '{file_name}' recuperado en temporal.")
        else:
            shutil.rmtree(temp_path, ignore_errors=True)
            shutil.copytree(version_dir, temp_path)
            print(f"Versión '{version_name}' restaurada completamente en temporal.")
