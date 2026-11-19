import json
import sys


ESPERADAS = {
    "module.portal.terraform_data.ficha",
    "module.ayuda.terraform_data.ficha",
}
ENTORNOS_ADMITIDOS = {"desarrollo", "pruebas", "integracion"}


def rechazar(motivo):
    print("POLÍTICA RECHAZADA: " + motivo)
    raise SystemExit(1)


def contiene_marcador(valor):
    if valor is True:
        return True
    if isinstance(valor, dict):
        return any(contiene_marcador(elemento) for elemento in valor.values())
    if isinstance(valor, list):
        return any(contiene_marcador(elemento) for elemento in valor)
    return False


try:
    plan = json.load(sys.stdin)
except (json.JSONDecodeError, UnicodeDecodeError):
    rechazar("el plan JSON no es válido")

if not isinstance(plan, dict) or "resource_changes" not in plan:
    rechazar("el plan JSON no contiene resource_changes")

cambios = plan["resource_changes"]
if not isinstance(cambios, list):
    rechazar("resource_changes debe ser una lista")

if len(cambios) != 2:
    rechazar("se esperan exactamente dos fichas ficticias")

direcciones = [cambio.get("address") for cambio in cambios if isinstance(cambio, dict)]
if set(direcciones) != ESPERADAS or len(direcciones) != 2:
    rechazar("las direcciones deben ser module.portal.terraform_data.ficha y module.ayuda.terraform_data.ficha")

fichas = {}
for cambio in cambios:
    direccion = cambio.get("address")

    if cambio.get("mode") != "managed":
        rechazar("solo se permiten recursos administrados")
    if cambio.get("type") != "terraform_data":
        rechazar("solo se permite el tipo terraform_data")

    change = cambio.get("change")
    if not isinstance(change, dict):
        rechazar("falta change en " + direccion)
    if change.get("actions") != ["create"]:
        rechazar("solo se permite la acción create en " + direccion)

    after = change.get("after")
    if not isinstance(after, dict) or not isinstance(after.get("input"), dict):
        rechazar("faltan los valores previstos en " + direccion)

    entrada = after["input"]
    if set(entrada) != {"nombre", "entorno"}:
        rechazar("se permiten únicamente nombre y entorno en " + direccion)

    nombre = entrada.get("nombre")
    entorno = entrada.get("entorno")
    if not isinstance(nombre, str) or not isinstance(entorno, str):
        rechazar("nombre y entorno deben ser cadenas en " + direccion)

    sensitive = change.get("after_sensitive")
    if contiene_marcador(sensitive):
        rechazar("las entradas de " + direccion + " no pueden estar marcadas como sensibles")

    fichas[direccion] = (nombre, entorno)

portal_nombre, portal_entorno = fichas["module.portal.terraform_data.ficha"]
ayuda_nombre, ayuda_entorno = fichas["module.ayuda.terraform_data.ficha"]

if not portal_nombre.startswith("portal-"):
    rechazar("el nombre del portal debe empezar por portal-")
if ayuda_nombre != "portal-ayuda":
    rechazar("la ficha de ayuda debe llamarse portal-ayuda")
if portal_entorno not in ENTORNOS_ADMITIDOS:
    rechazar("el entorno del portal no está admitido")
if ayuda_entorno not in ENTORNOS_ADMITIDOS:
    rechazar("el entorno de la ayuda no está admitido")
if portal_entorno != ayuda_entorno:
    rechazar("portal y ayuda deben pertenecer al mismo entorno")

print("POLÍTICA APROBADA: dos fichas ficticias, mismo entorno y sin operaciones reales")
