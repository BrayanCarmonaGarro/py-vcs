import json
import os

DATA_FILE = "data/users.json"

def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def has_read_permission(current_user, target_user):
    if current_user == target_user:
        return True  # puede leerse a sí mismo

    users = load_users()
    permisos = users.get(current_user, {}).get("permisos", {})
    lista = permisos.get(target_user, [])
    return "read" in lista

def has_write_permission(current_user, target_user):
    if current_user == target_user:
        return True  # puede escribirse a sí mismo

    users = load_users()
    permisos = users.get(current_user, {}).get("permisos", {})
    lista = permisos.get(target_user, [])
    return "write" in lista
