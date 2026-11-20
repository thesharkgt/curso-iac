import json
import sys


ESPERADAS = {
    'module.fichas["portal"].terraform_data.ficha',
    'module.fichas["ayuda"].terraform_data.ficha',
}
ENTORNOS_ADMITIDOS = {"desarrollo", "pruebas", "integracion"}
RESPONSABLES_POR_ENTORNO = {
    "desarrollo": "equipo-lab",
    "pruebas": "equipo-lab",
    "integracion": "equipo-integracion",
}


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
    rechazar("se esperan exactamente las fichas portal y ayuda")

direcciones = [cambio.get("address") for cambio in cambios if isinstance(cambio, dict)]
if set(direcciones) != ESPERADAS or len(direcciones) != 2:
    rechazar(
        'las direcciones deben ser module.fichas["portal"].terraform_data.ficha '
        'y module.fichas["ayuda"].terraform_data.ficha'
    )

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
    if set(entrada) != {"nombre", "entorno", "etiquetas"}:
        rechazar("se permiten únicamente nombre, entorno y etiquetas en " + direccion)

    nombre = entrada.get("nombre")
    entorno = entrada.get("entorno")
    etiquetas = entrada.get("etiquetas")
    if not isinstance(nombre, str) or not isinstance(entorno, str):
        rechazar("nombre y entorno deben ser cadenas en " + direccion)
    if not isinstance(etiquetas, dict):
        rechazar("etiquetas debe ser un mapa en " + direccion)
    if set(etiquetas) != {"proyecto", "entorno", "responsable"}:
        rechazar("etiquetas debe contener proyecto, entorno y responsable en " + direccion)
    if any(not isinstance(etiquetas.get(clave), str) for clave in etiquetas):
        rechazar("los valores de etiquetas deben ser cadenas en " + direccion)

    unknown = change.get("after_unknown")
    if isinstance(unknown, dict) and contiene_marcador(unknown.get("input")):
        rechazar("las entradas de " + direccion + " contienen valores desconocidos")

    sensitive = change.get("after_sensitive")
    if isinstance(sensitive, dict) and contiene_marcador(sensitive.get("input")):
        rechazar("las entradas de " + direccion + " no pueden estar marcadas como sensibles")

    fichas[direccion] = (nombre, entorno, etiquetas)

portal_nombre, portal_entorno, portal_etiquetas = fichas[
    'module.fichas["portal"].terraform_data.ficha'
]
ayuda_nombre, ayuda_entorno, ayuda_etiquetas = fichas[
    'module.fichas["ayuda"].terraform_data.ficha'
]

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

for direccion, entorno, etiquetas in (
    ('module.fichas["portal"].terraform_data.ficha', portal_entorno, portal_etiquetas),
    ('module.fichas["ayuda"].terraform_data.ficha', ayuda_entorno, ayuda_etiquetas),
):
    if etiquetas["proyecto"] != "nexo-portal":
        rechazar("el proyecto de " + direccion + " debe ser nexo-portal")
    if etiquetas["entorno"] != entorno:
        rechazar("la etiqueta entorno debe coincidir con el entorno de " + direccion)
    if etiquetas["responsable"] != RESPONSABLES_POR_ENTORNO[entorno]:
        rechazar("responsable no aprobado para " + entorno)

print("POLÍTICA APROBADA: dos fichas con etiquetas y responsable ficticios correctos")
