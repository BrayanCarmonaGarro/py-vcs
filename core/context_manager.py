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
            logging.error("El archivo de contexto está dañado. Se reiniciará.")
            return {}

    def save_context(self, context):
        with open(CONTEXT_FILE, "w") as f:
            json.dump(context, f, indent=2)

    def set_context(self, usuario_actual, usuario_destino):
        if not usuario_actual or not usuario_destino:
            print("Faltan datos de contexto.")
            return

        if usuario_actual == usuario_destino:
            path = os.path.join("repo_root", usuario_actual, "temporal")
        else:
            path = os.path.join("repo_root", usuario_destino, f"temp_{usuario_actual}")

        context = {
            "usuario_actual": usuario_actual,
            "usuario_destino": usuario_destino,
            "path": path
        }

        self.save_context(context)
        logging.info(f"Contexto cambiado a: {context}")

    def get_context(self):
        ctx = self.load_context()
        if not all(k in ctx for k in ("usuario_actual", "usuario_destino", "path")):
            return None
        return ctx

    def get_user(self):
        ctx = self.get_context()
        return ctx["usuario_actual"] if ctx else None
