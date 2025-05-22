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

    def set_context(self, usuario_actual, usuario_proyecto, proyecto, rama):
        context = {
            "usuario_actual": usuario_actual,
            "usuario_proyecto": usuario_proyecto,
            "proyecto": proyecto,
            "rama": rama
        }
        self.save_context(context)
        print(
            f"Contexto actualizado: Usuario actual: {usuario_actual}, Proyecto de: {usuario_proyecto}, Proyecto: {proyecto}, Rama: {rama}")
        logging.info(f"Contexto cambiado a: {context}")

    def get_context(self):
        ctx = self.load_context()
        if not all(k in ctx for k in ("usuario_actual", "usuario_proyecto", "proyecto", "rama")):
            return None
        if ctx["usuario_actual"] == ctx["usuario_proyecto"]:
            path = os.path.join("repo_root", ctx["usuario_actual"], ctx["proyecto"], "branches", ctx["rama"])
        else:
            path = os.path.join("repo_root", ctx["usuario_actual"], f"shared_{ctx['usuario_proyecto']}",
                                ctx["proyecto"], "branches", ctx["rama"])
        return {
            "usuario_actual": ctx["usuario_actual"],
            "usuario_proyecto": ctx["usuario_proyecto"],
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
