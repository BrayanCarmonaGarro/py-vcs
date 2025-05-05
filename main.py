import logging
from users.user_manager import UserManager
from projects.project_manager import ProjectManager
from core.context_manager import ContextManager
from core.version_control import VersionControl

# Configuracion de logging para guardar logs en un archivo y poder ver el flujo de la aplicacion y errores
logging.basicConfig(
    filename='logfile.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def main():
    logging.info("Aplicacion iniciada.")
    user_manager = UserManager()
    project_manager = ProjectManager()
    context_manager = ContextManager()
    version_control = VersionControl()
    
    while True:
        print("\n--- Menu Principal ---")
        print("1. Crear usuario")
        print("2. Listar usuarios")
        print("3. Asignar permisos")
        print("4. Crear proyecto")
        print("5. Listar proyectos")
        print("6. Cambiar contexto")
        print("7. Commit")
        print("8. Update")
        print("9. Listar versiones")
        print("10. Recuperar carpeta desde una version")
        print("11. Recuperar archivo desde una version")
        print("12. Salir")

        opcion = input("Seleccione una opcion: ")
        logging.info(f"Opcion seleccionada: {opcion}")

        if opcion == "1":
            username = input("Nombre de usuario: ")
            user_manager.create_user(username)

        elif opcion == "2":
            user_manager.list_users()

        elif opcion == "3":
            user_from = input("Usuario que otorga permisos: ")
            user_to = input("Usuario que recibe permisos: ")
            perm = input("Permiso (read/write): ")
            user_manager.assign_permission(user_from, user_to, perm)

        elif opcion == "4":
            username = input("Nombre de usuario: ")
            project_name = input("Nombre del proyecto: ")
            project_manager.create_project(username, project_name)

        elif opcion == "5":
            username = input("Nombre de usuario: ")
            project_manager.list_projects(username)

        elif opcion == "6":
            print("\n-- Cambiar Contexto --")
            user_manager.list_users()
            usuario = input("Selecciona el usuario: ")

            proyectos = project_manager.list_projects(usuario, silent=True)
            if not proyectos:
                print(f"El usuario '{usuario}' no tiene proyectos.")
                continue

            print("Proyectos disponibles:")
            for p in proyectos:
                print(f"- {p}")
            proyecto = input("Selecciona el proyecto: ")

            ramas = project_manager.list_branches(usuario, proyecto)
            if not ramas:
                print(f"El proyecto '{proyecto}' no tiene ramas.")
                continue

            print("Ramas disponibles:")
            for r in ramas:
                print(f"- {r}")
            rama = input("Selecciona la rama: ")

            context_manager.set_context(usuario, proyecto, rama)

        elif opcion == "7":
            version_control.commit()

        elif opcion == "8":
            version_control.update()

        elif opcion == "9":
            version_control.list_versions()

        elif opcion == "10":
            versions = version_control.list_versions()
            if versions:
                index = int(input("Seleccione la version a recuperar (numero): ")) - 1
                if 0 <= index < len(versions):
                    version_control.recover(versions[index], "", is_file=False)
                else:
                    print("indice invalido.")

        elif opcion == "11":
            versions = version_control.list_versions()
            if versions:
                index = int(input("Seleccione la version a recuperar (numero): ")) - 1
                if 0 <= index < len(versions):
                    version = versions[index]
                    archivos = version_control.list_files_in_version(version)
                    if not archivos:
                        print("No hay archivos en esta version.")
                        continue
                    print("\nArchivos disponibles en esa version:")
                    for i, archivo in enumerate(archivos):
                        print(f"{i + 1}. {archivo}")
                    try:
                        archivo_index = int(input("Seleccione el archivo a recuperar (numero): ")) - 1
                        if 0 <= archivo_index < len(archivos):
                            version_control.recover(version, archivos[archivo_index], is_file=True)
                        else:
                            print("indice invalido.")
                    except ValueError:
                        print("Entrada invalida.")
                else:
                    print("indice invalido.")


        elif opcion == "12":
            logging.info("Aplicacion finalizada por el usuario.")
            break

        else:
            print("Opcion invalida.")
            logging.warning(f"Opcion invalida seleccionada: {opcion}")

if __name__ == "__main__":
    main()
