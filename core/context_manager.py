import json
import os
import logging

CONTEXT_FILE = "data/context.json"

class ContextManager:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(CONTEXT_FILE):
            with open(CONTEXT_FILE, "w") as f:
                json.dump({}, f)

    def load_context(self):
        try:
            with open(CONTEXT_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logging.error("El archivo de contexto esta dañado. Se reiniciara.")
            return {}

    def save_context(self, context):
        with open(CONTEXT_FILE, "w") as f:
            json.dump(context, f, indent=2)

    def set_context(self, username, project, branch):
        context = {
            "usuario": username,
            "proyecto": project,
            "rama": branch
        }
        self.save_context(context)
        print(f"Contexto actualizado: Usuario: {username}, Proyecto: {project}, Rama: {branch}")
        logging.info(f"Contexto cambiado a: {context}")

    def get_context(self):
        ctx = self.load_context()
        if not all(k in ctx for k in ("usuario", "proyecto", "rama")):
            return None
        path = os.path.join("repo_root", ctx["usuario"], ctx["proyecto"], "branches", ctx["rama"])
        return {
            "usuario": ctx["usuario"],
            "proyecto": ctx["proyecto"],
            "rama": ctx["rama"],
            "path": path
        }

    def get_user(self):
        return self.load_context().get("usuario")

    def get_project(self):
        return self.load_context().get("proyecto")

    def get_branch(self):
        return self.load_context().get("rama")
