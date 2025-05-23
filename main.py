import logging
from users.user_manager import UserManager
from core.context_manager import ContextManager
from core.version_control import VersionControl
from utils import file_ops
from users import permissions
import os

# Configuración de logging
logging.basicConfig(
    filename='logfile.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def main():
    user_manager = UserManager()
    context_manager = ContextManager()
    version_control = VersionControl()

    while True:
        print("\n--- Menú Principal ---")
        print("1. Crear usuario")
        print("2. Listar usuarios")
        print("3. Asignar permisos")
        print("4. Cambiar de usuario (contexto)")
        print("5. Commit")
        print("6. Update desde otro usuario")
        print("7. Listar versiones")
        print("8. Recuperar versión completa")
        print("9. Recuperar archivo específico")
        print("10. Crear archivo")
        print("11. Ver archivo")
        print("12. Editar archivo")
        print("13. Eliminar archivo")
        print("14. Salir")

        opcion = input("Seleccione una opción: ").strip()
        logging.info(f"Opción seleccionada: {opcion}")

        if opcion == "1":
            username = input("Ingrese nombre del nuevo usuario: ").strip()
            user_manager.create_user(username)

        elif opcion == "2":
            user_manager.list_users()

        elif opcion == "3":
            from_user = input("Usuario que otorga permiso: ").strip()
            to_user = input("Usuario que recibirá permiso: ").strip()
            permiso = input("Permiso a otorgar (read/write): ").strip().lower()
            user_manager.assign_permission(from_user, to_user, permiso)

        elif opcion == "4":
            user_manager.list_users()
            usuario_actual = input("¿Quién eres tú (usuario actual)? ").strip()
            usuario_proyecto = input("¿A qué usuario deseas acceder (dueño de carpeta)?: ").strip()

            if usuario_actual not in user_manager.load_users() or usuario_proyecto not in user_manager.load_users():
                print("Uno de los usuarios no existe.")
                continue

            if usuario_actual == usuario_proyecto:
                path = os.path.join("repo_root", usuario_actual, "temporal")
            else:
                permisos = user_manager.load_users().get(usuario_proyecto, {}).get("permisos", {})
                if usuario_actual not in permisos:
                    print(f"No tienes permisos para acceder al repositorio de {usuario_proyecto}.")
                    continue
                path = os.path.join("repo_root", usuario_proyecto, f"temp_{usuario_actual}")

            context_manager.set_context({
                "usuario_actual": usuario_actual,
                "usuario_proyecto": usuario_proyecto,
                "path": path
            })

        elif opcion == "5":
            version_control.commit()

        elif opcion == "6":
            target_user = input("¿Desde qué usuario deseas hacer update?: ").strip()
            version_control.update(target_user)

        elif opcion == "7":
            version_control.list_versions()

        elif opcion == "8":
            versions = version_control.list_versions()
            if versions:
                index = input("Seleccione número de versión a recuperar: ").strip()
                if index.isdigit() and 1 <= int(index) <= len(versions):
                    version_control.recover(versions[int(index) - 1], None)
                else:
                    print("Índice inválido.")

        elif opcion == "9":
            versions = version_control.list_versions()
            if versions:
                index = input("Seleccione número de versión: ").strip()
                if index.isdigit() and 1 <= int(index) <= len(versions):
                    version = versions[int(index) - 1]
                    archivos = version_control.list_files_in_version(version)
                    if not archivos:
                        print("No hay archivos en esta versión.")
                        continue
                    print("\nArchivos disponibles en esa versión:")
                    for i, archivo in enumerate(archivos):
                        print(f"{i + 1}. {archivo}")
                    archivo_index = input("Seleccione archivo (número): ").strip()
                    if archivo_index.isdigit() and 1 <= int(archivo_index) <= len(archivos):
                        version_control.recover(version, archivos[int(archivo_index) - 1], is_file=True)
                    else:
                        print("Índice de archivo inválido.")
                else:
                    print("Índice de versión inválido.")

        elif opcion == "10":
            ctx = context_manager.get_context()
            if not ctx:
                print("No hay contexto seleccionado.")
                continue
            current_user = ctx["usuario_actual"]
            target_user = ctx["usuario_proyecto"]
            if not permissions.has_write_permission(current_user, target_user):
                print("No tienes permiso de escritura.")
                continue
            filename = input("Nombre del archivo: ")
            content = input("Contenido inicial: ")
            file_ops.create_file(ctx["path"], filename, content)

        elif opcion == "11":
            ctx = context_manager.get_context()
            if not ctx:
                print("No hay contexto seleccionado.")
                continue
            current_user = ctx["usuario_actual"]
            target_user = ctx["usuario_proyecto"]
            if not permissions.has_read_permission(current_user, target_user):
                print("No tienes permiso de lectura.")
                continue
            filename = input("Archivo a leer: ")
            content = file_ops.read_file(ctx["path"], filename)
            if content:
                print("\n--- Contenido del archivo ---\n")
                print(content)

        elif opcion == "12":
            ctx = context_manager.get_context()
            if not ctx:
                print("No hay contexto seleccionado.")
                continue
            current_user = ctx["usuario_actual"]
            target_user = ctx["usuario_proyecto"]
            if not permissions.has_write_permission(current_user, target_user):
                print("No tienes permiso de escritura.")
                continue
            filename = input("Archivo a editar: ")
            content = input("Nuevo contenido: ")
            file_ops.update_file(ctx["path"], filename, content)

        elif opcion == "13":
            ctx = context_manager.get_context()
            if not ctx:
                print("No hay contexto seleccionado.")
                continue
            current_user = ctx["usuario_actual"]
            target_user = ctx["usuario_proyecto"]
            if not permissions.has_write_permission(current_user, target_user):
                print("No tienes permiso de escritura para eliminar archivos.")
                continue
            filename = input("Archivo a eliminar: ")
            file_ops.delete_file(ctx["path"], filename)

        elif opcion == "14":
            logging.info("Aplicación finalizada.")
            break

        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
