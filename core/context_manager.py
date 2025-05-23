import json
import os

CONTEXT_FILE = "data/context.json"

class ContextManager:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(CONTEXT_FILE):
            with open(CONTEXT_FILE, "w") as f:
                json.dump({}, f)

    def load_context(self):
        with open(CONTEXT_FILE, "r") as f:
            return json.load(f)

    def save_context(self, context):
        with open(CONTEXT_FILE, "w") as f:
            json.dump(context, f, indent=2)

    def set_context(self, username):
        context = {"usuario": username}
        self.save_context(context)
        print(f"Contexto actualizado: Usuario: {username}")

    def get_user(self):
        context = self.load_context()
        return context.get("usuario")
