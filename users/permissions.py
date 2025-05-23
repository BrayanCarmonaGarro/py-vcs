import json

DATA_FILE = "data/users.json"

def load_users():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def has_read_permission(usuario_actual, usuario_destino):
    if usuario_actual == usuario_destino:
        return True
    users = load_users()
    permisos = users.get(usuario_destino, {}).get("permisos", {})
    return permisos.get(usuario_actual) in ("read", "write")

def has_write_permission(usuario_actual, usuario_destino):
    if usuario_actual == usuario_destino:
        return True
    users = load_users()
    permisos = users.get(usuario_destino, {}).get("permisos", {})
    return permisos.get(usuario_actual) == "write"
