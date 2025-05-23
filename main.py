import logging
from users.user_manager import UserManager
from core.context_manager import ContextManager
from core.version_control import VersionControl
from utils import file_ops
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
        print("4. Quitar permiso")
        print("5. Cambiar de usuario (contexto)")
        print("6. Commit")
        print("7. Update desde otro usuario")
        print("8. Listar versiones")
        print("9. Recuperar versión completa")
        print("10. Recuperar archivo específico")
        print("11. Crear archivo")
        print("12. Listar archivos")
        print("13. Ver archivo")
        print("14. Editar archivo")
        print("15. Eliminar archivo")
        print("16. Salir")

        opcion = input("Seleccione una opción: ").strip()
        os.system('cls' if os.name == 'nt' else 'clear')
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
            from_user = input("¿De quién es el repositorio?: ").strip()
            to_user = input("¿A qué usuario deseas quitarle el permiso?: ").strip()
            permiso = input("¿Qué permiso deseas quitar (read/write)?: ").strip().lower()
            user_manager.remove_permission(from_user, to_user, permiso)

        elif opcion == "5":
            user_manager.list_users()
            usuario_actual = input("¿Quién eres tú (usuario actual)? ").strip()
            usuario_destino = input("¿A qué usuario deseas acceder (dueño de carpeta)?: ").strip()

            if usuario_actual not in user_manager.load_users() or usuario_destino not in user_manager.load_users():
                print("Uno de los usuarios no existe.")
                continue

            if usuario_actual not in user_manager.load_users() or usuario_destino not in user_manager.load_users():
                print("Uno de los usuarios no existe.")
                continue

            if usuario_actual != usuario_destino and not user_manager.has_any_permission(usuario_actual, usuario_destino):
                print(f"No tienes permisos para acceder al repositorio de {usuario_destino}.")
                continue

            context_manager.set_context(usuario_actual, usuario_destino)

        elif opcion == "6":
            version_control.update()

        elif opcion == "8":
            version_control.list_versions()

        elif opcion == "9":
            versions = version_control.list_versions()
            if versions:
                index = input("Seleccione número de versión a recuperar: ").strip()
                if index.isdigit() and 1 <= int(index) <= len(versions):
                    version_control.recover(versions[int(index) - 1], None)
                else:
                    print("Índice inválido.")

        elif opcion == "10":
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

        elif opcion == "11":
            ctx = context_manager.get_context()
            if not ctx:
                print("No hay contexto seleccionado.")
                continue
            current_user = ctx["usuario_actual"]
            target_user = ctx["usuario_destino"]
            if not user_manager.has_write_permission(current_user, target_user):
                print("No tienes permiso de escritura.")
                continue
            filename = input("Nombre del archivo: ")
            file_ops.create_file(ctx["path"], filename)

        elif opcion == "12":
            ctx = context_manager.get_context()
            if not ctx:
                print("No hay contexto seleccionado.")
                continue
            current_user = ctx["usuario_actual"]
            target_user = ctx["usuario_destino"]
            if not user_manager.has_read_permission(current_user, target_user):
                print("No tienes permiso de lectura.")
                continue
            file_ops.list_files(ctx["path"])

        elif opcion == "13":
            ctx = context_manager.get_context()
            if not ctx:
                print("No hay contexto seleccionado.")
                continue
            current_user = ctx["usuario_actual"]
            target_user = ctx["usuario_destino"]
            if not user_manager.has_read_permission(current_user, target_user):
                print("No tienes permiso de lectura.")
                continue
            file_ops.list_files(ctx["path"])
            filename = input("Archivo a leer: ")
            content = file_ops.read_file(ctx["path"], filename)
            if content:
                print("\n--- Contenido del archivo ---\n")
                print(content)

        elif opcion == "14":
            ctx = context_manager.get_context()
            if not ctx:
                print("No hay contexto seleccionado.")
                continue
            current_user = ctx["usuario_actual"]
            target_user = ctx["usuario_destino"]
            if not user_manager.has_write_permission(current_user, target_user):
                print("No tienes permiso de escritura.")
                continue
            file_ops.list_files(ctx["path"])
            filename = input("Archivo a editar: ")
            content = input("Nuevo contenido: ")
            file_ops.update_file(ctx["path"], filename, content)

        elif opcion == "15":
            ctx = context_manager.get_context()
            if not ctx:
                print("No hay contexto seleccionado.")
                continue
            current_user = ctx["usuario_actual"]
            target_user = ctx["usuario_destino"]
            if not user_manager.has_write_permission(current_user, target_user):
                print("No tienes permiso de escritura para eliminar archivos.")
                continue
            filename = input("Archivo a eliminar: ")
            file_ops.delete_file(ctx["path"], filename)

        elif opcion == "16":
            logging.info("Aplicación finalizada.")
            break

        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
